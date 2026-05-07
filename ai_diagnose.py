"""
大模型智能错误诊断模块

功能：
  1. 自动捕获 Pytest 运行的错误日志 / traceback
  2. 调用 ANTHROPIC_BASE_URL + ANTHROPIC_API_KEY 对应的大模型接口
  3. 让大模型分析报错原因，并给出修复建议

使用方式：
  # 先跑测试，把输出重定向到日志文件
  pytest --tb=long 2>&1 | tee test_output.log

  # 然后用本脚本诊断
  python ai_diagnose.py                     # 默认读 test_output.log
  python ai_diagnose.py my_error.log        # 指定日志文件
  python ai_diagnose.py --pytest            # 直接调用 pytest 并捕获输出
"""

import os
import sys
import subprocess
import requests
import json
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


# ──────────────────────────────────────────────
# 配置区
# ──────────────────────────────────────────────

# 默认日志文件名（pytest 输出重定向的目标）
DEFAULT_LOG_FILE = "test_output.log"

# 调用 pytest 时的额外参数（仅 --pytest 模式生效）
PYTEST_ARGS = ["--tb=long", "-v"]

# 大模型接口配置（从环境变量读取）
API_BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# 诊断用的 system prompt
SYSTEM_PROMPT = """你是一位资深的 Python 自动化测试工程师，精通 Playwright + Pytest 技术栈。
请根据用户提供的测试报错信息，完成以下分析：

1. **错误定位**：指出报错的核心原因（哪一行、哪个操作出了问题）。
2. **根因分析**：分析导致该错误的深层原因（如元素定位失败、超时、页面状态异常等）。
3. **修复建议**：给出具体的代码修改方案或排查步骤，尽量附带示例代码。
4. **预防措施**：建议如何避免同类问题再次发生。

请用中文回答，语言简洁专业。"""


# ──────────────────────────────────────────────
# 核心函数
# ──────────────────────────────────────────────

def read_log_file(file_path: str) -> str:
    """读取日志文件内容，提取包含错误信息的关键段落。"""
    if not os.path.exists(file_path):
        print(f"[错误] 日志文件不存在: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print("[错误] 日志文件为空，没有可分析的内容。")
        sys.exit(1)

    return content


def extract_error_sections(full_log: str) -> str:
    """
    从完整的 pytest 输出中，提取与错误相关的关键段落。
    优先提取短摘要（short test summary）和 traceback 部分，
    如果没找到则返回完整日志。
    """
    lines = full_log.splitlines()
    error_sections = []
    capture = False

    for line in lines:
        # Pytest 的短摘要区域以 "SHORT TEST SUMMARY INFO" 开头
        if "SHORT TEST SUMMARY INFO" in line:
            capture = True
        # Pytest 的详细错误区域以 "FAILURES" 或 "ERRORS" 开头
        if any(marker in line for marker in ["== FAILURES ==", "== ERRORS =="]):
            capture = True

        if capture:
            error_sections.append(line)

    # 如果成功提取到错误段落，就用精简版；否则用完整日志
    if error_sections:
        extracted = "\n".join(error_sections)
        # 限制长度，避免超出大模型 token 限制
        if len(extracted) > 8000:
            extracted = extracted[:8000] + "\n... (日志过长，已截断)"
        return extracted

    # fallback: 截取日志末尾部分（通常错误信息在最后）
    if len(full_log) > 8000:
        return "... (前文已省略) ...\n" + full_log[-8000:]
    return full_log


def run_pytest_and_capture() -> str:
    """直接调用 pytest 运行测试，捕获输出。"""
    print("[信息] 正在运行 pytest 执行测试...")
    cmd = [sys.executable, "-m", "pytest"] + PYTEST_ARGS

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=os.getcwd(),
    )

    # 合并 stdout 和 stderr
    output = result.stdout
    if result.stderr:
        output += "\n--- stderr ---\n" + result.stderr

    if result.returncode == 0:
        print("[信息] 所有测试均通过，无需诊断。")
        sys.exit(0)

    return output


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout)),
    reraise=True,
)
def _call_api(url: str, headers: dict, payload: dict) -> dict:
    """调用大模型 API，遇到网络/超时错误自动重试（最多 3 次，间隔 2 秒）。"""
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def call_llm_diagnosis(error_log: str) -> str | None:
    """
    调用大模型接口进行错误诊断。
    使用 ANTHROPIC_BASE_URL 和 ANTHROPIC_API_KEY 环境变量。
    遵循 Anthropic Messages API 格式。

    重试 3 次后仍失败则返回 None（优雅降级，不崩溃）。
    """
    if not API_BASE_URL:
        print("[错误] 环境变量 ANTHROPIC_BASE_URL 未设置，请配置大模型接口地址。")
        return None
    if not API_KEY:
        print("[错误] 环境变量 ANTHROPIC_API_KEY 未设置，请配置 API 密钥。")
        return None

    model = os.environ.get("ANTHROPIC_MODEL", "")
    if not model:
        print("[错误] 环境变量 ANTHROPIC_MODEL 未设置，请配置模型名称。")
        return None

    # 构造请求 —— Anthropic Messages API 格式
    url = f"{API_BASE_URL.rstrip('/')}/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": 2000,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"以下是 Pytest 运行后捕获的错误日志，请帮我诊断：\n\n```\n{error_log}\n```"},
        ],
    }

    print(f"[信息] 正在调用大模型接口: {url}")
    print("[信息] 请稍候，模型分析中...\n")

    try:
        data = _call_api(url, headers, payload)
        diagnosis = data["content"][0]["text"]
        return diagnosis

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print(f"\n⚠️  AI 诊断服务暂时不可用（网络连接失败: {e}），已为您保留本地错误日志。")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"\n⚠️  AI 诊断服务暂时不可用（HTTP 错误: {e}），已为您保留本地错误日志。")
        return None
    except (KeyError, IndexError):
        print("\n⚠️  AI 诊断服务暂时不可用（响应格式异常），已为您保留本地错误日志。")
        return None


def print_report(diagnosis: str):
    """格式化输出诊断报告。"""
    separator = "=" * 60
    print(separator)
    print("  大模型智能错误诊断报告")
    print(separator)
    print()
    print(diagnosis)
    print()
    print(separator)


# ──────────────────────────────────────────────
# 入口
# ──────────────────────────────────────────────

def main():
    # 支持 --pytest 参数：直接运行 pytest 并捕获输出
    if "--pytest" in sys.argv:
        full_log = run_pytest_and_capture()
    else:
        # 从命令行参数或默认文件名获取日志路径
        log_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOG_FILE
        full_log = read_log_file(log_file)

    # 提取错误关键段落
    error_log = extract_error_sections(full_log)
    print(f"[信息] 已提取错误日志（{len(error_log)} 字符）")

    # 调用大模型诊断
    diagnosis = call_llm_diagnosis(error_log)

    # 输出报告（诊断失败时给出友好提示）
    if diagnosis:
        print_report(diagnosis)
    else:
        print("\n[信息] 错误日志已保存，可稍后重试或手动分析。")


if __name__ == "__main__":
    main()
