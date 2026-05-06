# 多引入了一个 expect，专门用来做断言检查
from playwright.sync_api import sync_playwright, expect
import time


def run_automation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("1. 正在打开网站...")
        page.goto("https://www.saucedemo.com/")

        print("2. 正在输入账号和密码...")
        page.locator('[data-test="username"]').fill("standard_user")
        page.locator('[data-test="password"]').fill("secret_sauce")

        print("3. 点击登录！")
        page.locator('[data-test="login-button"]').click()

        # -----------------------------------------
        # 🌟 这里是重点：断言（判断测试是否真正成功）
        # -----------------------------------------
        print("4. 开始检查是否登录成功...")

        # 找到登录成功后，页面左上角的标题栏元素
        title_element = page.locator(".title")

        # 断言：期望这个标题栏里的文字包含 "Products"
        expect(title_element).to_have_text("Products")

        print("✅ 断言通过！系统确认已成功进入商品列表页！")
        # -----------------------------------------

        time.sleep(3)
        browser.close()


if __name__ == "__main__":
    run_automation()