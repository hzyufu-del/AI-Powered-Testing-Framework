from playwright.sync_api import expect
from login_page import LoginPage  # 引入第一页说明书
from products_page import ProductsPage  # 引入第二页说明书
import time


def test_add_to_cart_flow(page):
    print("\n--- 测试开始：电商核心购物链路 ---")

    # 【接力第一棒：登录页】
    login_page = LoginPage(page)
    login_page.navigate()
    print("1. 执行登录...")
    login_page.login("standard_user", "secret_sauce")

    # 【接力第二棒：商品页】
    # 登录成功后，页面其实已经跳转了，我们立刻拿出第二本说明书
    products_page = ProductsPage(page)

    print("2. 正在将背包加入购物车...")
    products_page.add_backpack_to_cart()

    print("3. 开始终极断言检查...")
    # 断言：检查右上角购物车的数字是不是变成了 "1"
    # 面试官最喜欢看这种严谨的业务断言！
    assert products_page.get_cart_item_count() == "1", "❌ 购物车数量错误！添加失败！"
    print("✅ 断言通过！商品已成功加入购物车！")

    time.sleep(2)