import json
import pytest
from pathlib import Path
from playwright.sync_api import expect
from login_page import LoginPage
from products_page import ProductsPage

# 从 JSON 文件加载测试数据
DATA_FILE = Path(__file__).parent / "data" / "test_data.json"
with open(DATA_FILE, encoding="utf-8") as f:
    _data = json.load(f)

shopping_data = _data["shopping_flow"]


@pytest.mark.parametrize(
    "username, password, product_test_id, expected_cart_count",
    [
        (d["username"], d["password"], d["product_test_id"], d["expected_cart_count"])
        for d in shopping_data
    ],
    ids=[d["case_name"] for d in shopping_data],
)
def test_add_to_cart_flow(page, username, password, product_test_id, expected_cart_count):
    print(f"\n--- 测试开始：电商核心购物链路 ({product_test_id}) ---")

    # 【接力第一棒：登录页】
    login_page = LoginPage(page)
    login_page.navigate()
    print("1. 执行登录...")
    login_page.login(username, password)

    # 【接力第二棒：商品页】
    products_page = ProductsPage(page)

    print(f"2. 正在将商品 {product_test_id} 加入购物车...")
    add_button = page.locator(f'[data-test="add-to-cart-{product_test_id}"]')
    add_button.click()

    print("3. 开始终极断言检查...")
    assert products_page.get_cart_item_count() == expected_cart_count, "❌ 购物车数量错误！添加失败！"
    print("✅ 断言通过！商品已成功加入购物车！")
