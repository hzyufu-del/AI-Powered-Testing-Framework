# 🧪 Playwright + Pytest 自动化测试框架（AI 增强版）

# 🧪 Playwright + Pytest Automation Framework (AI-Enhanced)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-2EAD33.svg)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-8.x-0A9EDC.svg)](https://docs.pytest.org/)
[![AI](https://img.shields.io/badge/AI%20Diagnosis-Mimo%20v2.5-FF6B35.svg)](https://mimo.org)

> 一个基于 **Playwright + Pytest** 的 Web UI 自动化测试框架，集成 **大模型智能错误诊断模块**，测试失败时自动调用 AI 分析根因并给出修复建议。
>
> A **Web UI automation testing framework** built on Playwright + Pytest, featuring an **AI-powered error diagnosis module** that automatically analyzes test failures and provides fix suggestions using large language models.

---

## 📌 项目简介 | Overview

本项目是一个面向 Web 应用的端到端（E2E）自动化测试框架，以 [Sauce Demo](https://www.saucedemo.com/) 电商网站为测试对象，演示了：

- ✅ **POM 设计模式** — Page Object Model 让测试代码清晰、可维护
- ✅ **数据驱动测试** — 使用 `@pytest.mark.parametrize` 实现多组数据批量验证
- ✅ **业务链路测试** — 覆盖「登录 → 浏览商品 → 加入购物车」完整流程
- ✅ **AI 智能诊断** — 测试失败时，自动调用大模型分析错误并输出诊断报告

This project is an end-to-end (E2E) automation testing framework targeting the [Sauce Demo](https://www.saucedemo.com/) e-commerce site, demonstrating:

- ✅ **Page Object Model (POM)** — Clean, maintainable test code structure
- ✅ **Data-Driven Testing** — Batch validation with `@pytest.mark.parametrize`
- ✅ **Business Flow Testing** — Full coverage of "Login → Browse → Add to Cart"
- ✅ **AI-Powered Diagnosis** — Automatic root cause analysis via LLM on test failures

---

## 🏗️ 技术栈 | Tech Stack

| 类别 | 技术 | 说明 |
|:---:|:---:|:---|
| 🎭 浏览器自动化 | [Playwright](https://playwright.dev/python/) | 跨浏览器 E2E 测试引擎 |
| 🧪 测试框架 | [Pytest](https://docs.pytest.org/) | 灵活的 Python 测试框架 |
| 🤖 AI 诊断引擎 | Mimo v2.5 (Claude 3.5 Sonnet) | 大模型接口，智能分析测试失败原因 |
| 📄 报告 | pytest-html | HTML 格式测试报告 |
| 🔌 HTTP 客户端 | Requests | 调用大模型 API |

---

## 📁 项目结构 | Project Structure

```
student/
├── 🧪 测试用例层 (Test Cases)
│   ├── first_test.py          # 基础 Playwright 脚本（快速验证）
│   ├── test_login.py          # 登录功能 — 数据驱动测试
│   └── test_shopping.py       # 购物车功能 — 业务链路测试
│
├── 📖 页面对象层 (Page Objects)
│   ├── login_page.py          # 登录页 POM 封装
│   └── products_page.py       # 商品页 POM 封装
│
├── 🤖 AI 诊断模块
│   └── ai_diagnose.py         # 大模型智能错误诊断（核心亮点）
│
├── 📊 输出产物
│   └── report.html            # Pytest HTML 测试报告
│
├── ⚙️ 配置文件
│   ├── .gitignore             # Git 忽略规则
│   └── requirements.txt       # Python 依赖清单
│
└── 📝 README.md               # 本文件
```

---

## 🚀 快速开始 | Quick Start

### 1️⃣ 克隆项目 | Clone the Repository

```bash
git clone https://github.com/your-username/student.git
cd student
```

### 2️⃣ 创建虚拟环境 | Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3️⃣ 安装依赖 | Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 4️⃣ 配置环境变量 | Configure Environment Variables

创建 `.env` 文件（已在 `.gitignore` 中排除）：

Create a `.env` file (already excluded in `.gitignore`):

```ini
# 大模型接口地址 | LLM API Base URL
ANTHROPIC_BASE_URL=https://api.mimo.org

# API 密钥 | API Key
ANTHROPIC_API_KEY=your-api-key-here

# 模型名称 | Model Name
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

> ⚠️ **安全提示**：切勿将 `.env` 文件提交到版本控制系统。
>
> ⚠️ **Security**: Never commit your `.env` file to version control.

### 5️⃣ 运行测试 | Run Tests

```bash
# 运行全部测试
pytest -v

# 运行并生成 HTML 报告
pytest -v --html=report.html --self-contained-html

# 仅运行登录测试
pytest test_login.py -v

# 仅运行购物车测试
pytest test_shopping.py -v
```

---

## 🤖 AI 智能诊断 | AI-Powered Error Diagnosis

这是本框架的**核心亮点**——当测试用例失败时，无需人工排查，大模型自动帮你分析！

This is the **core highlight** — when tests fail, the LLM automatically analyzes the root cause for you!

### 工作原理 | How It Works

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Pytest 运行  │ ──▶ │ 捕获错误日志   │ ──▶ │ 调用 Mimo API  │ ──▶ │ 输出诊断报告       │
│  测试用例     │     │ & traceback  │     │ 大模型分析     │     │ (根因+修复建议)    │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────────┘
```

1. **捕获日志** — 自动提取 Pytest 输出中的 `SHORT TEST SUMMARY`、`FAILURES`、`ERRORS` 关键段落
2. **智能分析** — 将错误日志发送给 Mimo v2.5 (Claude 3.5 Sonnet)，由 AI 模型进行深度分析
3. **诊断报告** — 输出包含「错误定位 → 根因分析 → 修复建议 → 预防措施」的完整报告

### 使用方式 | Usage

```bash
# 方式一：先运行测试，再诊断日志
pytest --tb=long -v 2>&1 | tee test_output.log
python ai_diagnose.py                     # 默认读取 test_output.log

# 方式二：指定日志文件
python ai_diagnose.py my_error.log

# 方式三：一步到位（自动运行 pytest + 诊断）
python ai_diagnose.py --pytest
```

### 诊断报告示例 | Sample Diagnosis Output

```
============================================================
  大模型智能错误诊断报告
============================================================

1. **错误定位**：test_shopping.py 第 26 行断言失败
   期望购物车数量为 "1"，但实际角标未找到（元素不可见）

2. **根因分析**：addToCart 按钮点击后，页面跳转尚未完成，
   角标元素还未渲染，导致 is_visible() 返回 False

3. **修复建议**：在断言前添加等待机制...
   products_page.cart_badge.wait_for(state="visible", timeout=5000)

4. **预防措施**：建议在 POM 方法中封装智能等待，避免时序问题

============================================================
```

---

## 🔧 核心设计 | Core Design

### Page Object Model (POM)

每个页面封装为一个类，集中管理元素定位和操作：

Each page is encapsulated as a class with centralized element locators and actions:

```python
# login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.title_element = page.locator(".title")

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

### 数据驱动测试

使用 `@pytest.mark.parametrize` 实现同一测试逻辑、多组数据验证：

```python
test_data = [
    ("standard_user", "secret_sauce"),
    ("visual_user", "secret_sauce"),
]

@pytest.mark.parametrize("username, password", test_data)
def test_data_driven_login(page, username, password):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)
    expect(login_page.title_element).to_have_text("Products")
```

---

## 📋 依赖清单 | Dependencies

| 包名 | 版本 | 用途 |
|:---:|:---:|:---|
| `playwright` | >=1.40.0 | 浏览器自动化引擎 |
| `pytest` | >=8.0.0 | 测试框架 |
| `pytest-playwright` | >=0.4.0 | Playwright 的 Pytest 集成插件 |
| `pytest-html` | >=4.0.0 | HTML 测试报告生成 |
| `requests` | >=2.31.0 | HTTP 请求库（调用 AI API） |
| `python-dotenv` | >=1.0.0 | 环境变量管理 |

---

## 🤝 贡献指南 | Contributing

欢迎提交 Issue 和 Pull Request！

Contributions are welcome! Feel free to open issues and submit PRs.

---

## 📄 许可证 | License

本项目采用 [MIT License](LICENSE) 开源。

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using Playwright, Pytest & AI**

</div>
