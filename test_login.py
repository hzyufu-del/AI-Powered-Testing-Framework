import json
import pytest
from pathlib import Path
from playwright.sync_api import expect
from login_page import LoginPage

# 从 JSON 文件加载测试数据
DATA_FILE = Path(__file__).parent / "data" / "test_data.json"
with open(DATA_FILE, encoding="utf-8") as f:
    _data = json.load(f)

login_success_data = _data["login_success"]
login_failure_data = _data["login_failure"]


@pytest.mark.parametrize(
    "username, password, expected_title",
    [(d["username"], d["password"], d["expected_title"]) for d in login_success_data],
    ids=[d["case_name"] for d in login_success_data],
)
def test_login_success(page, username, password, expected_title):
    print(f"\n--- 正在使用账号进行测试: {username} ---")
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)
    print("开始断言检查...")
    expect(login_page.title_element).to_have_text(expected_title)
    print(f"✅ 账号 {username} 登录测试通过！")


@pytest.mark.parametrize(
    "username, password, expected_error",
    [(d["username"], d["password"], d["expected_error"]) for d in login_failure_data],
    ids=[d["case_name"] for d in login_failure_data],
)
def test_login_failure(page, username, password, expected_error):
    print(f"\n--- 正在测试登录失败场景: {username or '(空)'} ---")
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)
    error_element = page.locator('[data-test="error"]')
    expect(error_element).to_be_visible()
    expect(error_element).to_contain_text(expected_error)
    print(f"✅ 登录失败场景验证通过！")
