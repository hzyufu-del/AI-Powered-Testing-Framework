import pytest  # 引入 Pytest 核心库
from playwright.sync_api import expect
from login_page import LoginPage
import time

# 🌟 这里就是我们的“弹夹”（测试数据池）
# 我们准备了两个 Sauce Demo 官方提供的有效测试账号
test_data = [
    ("standard_user", "secret_sauce"),  # 第一组数据：标准用户
    ("visual_user", "secret_sauce")  # 第二组数据：视觉测试用户
]


# 🌟 给测试用例戴上“魔法帽子”，告诉它：请从 test_data 里一行一行取数据，分别塞给 username 和 password
@pytest.mark.parametrize("username, password", test_data)
def test_data_driven_login(page, username, password):
    print(f"\n--- 正在使用账号进行测试: {username} ---")

    login_page = LoginPage(page)
    login_page.navigate()

    # 这里不再写死具体的账号，而是使用传进来的变量！
    login_page.login(username, password)

    print("开始断言检查...")
    expect(login_page.title_element).to_have_text("Products")
    print(f"✅ 账号 {username} 登录测试通过！")

