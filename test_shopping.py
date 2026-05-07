import json
import re
import pytest
from pathlib import Path
from playwright.sync_api import expect
from login_page import LoginPage
from products_page import ProductsPage
from cart_page import CartPage

DATA_FILE = Path(__file__).parent / "data" / "test_data.json"
with open(DATA_FILE, encoding="utf-8") as f:
    _data = json.load(f)

shopping_data = _data["shopping_flow"]


@pytest.mark.parametrize(
    "username, password, search_keyword, expected_product_name, unit_price, quantity, expected_total_price",
    [
        (
            d["username"],
            d["password"],
            d["search_keyword"],
            d["expected_product_name"],
            d["unit_price"],
            d["quantity"],
            d["expected_total_price"],
        )
        for d in shopping_data
    ],
    ids=[d["case_name"] for d in shopping_data],
)
def test_shopping_flow(
    page,
    username,
    password,
    search_keyword,
    expected_product_name,
    unit_price,
    quantity,
    expected_total_price,
):
    print(f"\n--- E2E 购物全链路测试: {expected_product_name} x{quantity} ---")

    # ========== 第一步：登录系统 ==========
    login_page = LoginPage(page)
    login_page.navigate()
    print("1. 执行登录...")
    login_page.login(username, password)
    expect(page.locator(".title")).to_have_text("Products", timeout=10000)
    print("   登录成功，已进入商品列表页。")

    # ========== 第二步：搜索商品 ==========
    products_page = ProductsPage(page)
    print(f"2. 搜索商品: '{search_keyword}' ...")
    products_page.search_product(search_keyword)

    # ========== 第三步：进入商品详情并设置数量 ==========
    print(f"3. 点击进入商品详情: {expected_product_name} ...")
    products_page.click_product_by_name(expected_product_name)

    detail_name = page.locator(".inventory_details_name")
    expect(detail_name).to_be_visible(timeout=5000)
    expect(detail_name).to_contain_text(expected_product_name)

    print(f"   设置购买数量: {quantity} ...")
    products_page.set_quantity(quantity)

    # ========== 第四步：加入购物车 ==========
    print("4. 点击加入购物车...")
    products_page.add_to_cart()

    # ========== 第五步：进入购物车页面 ==========
    print("5. 进入购物车页面...")
    products_page.go_to_cart()
    expect(page).to_have_url(re.compile(r".*cart\.html"), timeout=5000)

    # ========== 第六步：断言验证 ==========
    print("6. 开始断言验证...")
    cart_page = CartPage(page)

    # 断言 1：商品名称是否正确
    actual_name = cart_page.get_product_name(0)
    print(f"   购物车商品名称: {actual_name}")
    assert actual_name == expected_product_name, (
        f"商品名称不匹配！期望: {expected_product_name}，实际: {actual_name}"
    )
    print(f"   [OK] 商品名称验证通过")

    # 断言 2：单价是否正确
    actual_price = cart_page.get_unit_price(0)
    print(f"   商品单价: ${actual_price}")
    assert actual_price == unit_price, (
        f"单价不匹配！期望: ${unit_price}，实际: ${actual_price}"
    )
    print(f"   [OK] 单价验证通过")

    # 断言 3：数量是否正确
    actual_qty = cart_page.get_quantity(0)
    print(f"   购买数量: {actual_qty}")
    assert actual_qty == quantity, (
        f"数量不匹配！期望: {quantity}，实际: {actual_qty}"
    )
    print(f"   [OK] 数量验证通过")

    # 断言 4：总价是否等于 单价 * 数量
    actual_total = cart_page.get_total_price(0)
    calculated_total = round(unit_price * quantity, 2)
    print(f"   总价: ${actual_total} (计算期望: ${unit_price} x {quantity} = ${calculated_total})")
    assert actual_total == calculated_total, (
        f"总价计算错误！期望: ${calculated_total}，实际: ${actual_total}"
    )
    assert actual_total == expected_total_price, (
        f"总价与预期数据不匹配！预期: ${expected_total_price}，实际: ${actual_total}"
    )
    print(f"   [OK] 总价验证通过: ${actual_total}")

    print(f"\n{'='*50}")
    print(f"  ALL ASSERTIONS PASSED")
    print(f"  商品: {actual_name}")
    print(f"  单价: ${actual_price}")
    print(f"  数量: {actual_qty}")
    print(f"  总价: ${actual_total}")
    print(f"{'='*50}")
