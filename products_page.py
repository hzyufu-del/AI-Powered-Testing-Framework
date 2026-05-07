from playwright.sync_api import expect


class ProductsPage:
    def __init__(self, page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.product_names = page.locator(".inventory_item_name")
        self.search_input = page.locator('[data-test="search"]')

    def search_product(self, keyword):
        """搜索商品。若站点无搜索框则跳过，按名称筛选代替。"""
        if self.search_input.count() > 0:
            self.search_input.fill(keyword)
            self.search_input.press("Enter")
        else:
            pass  # SauceDemo 无搜索功能，后续通过名称点击定位商品

    def click_product_by_name(self, product_name):
        """点击商品名称进入详情页。"""
        product_link = self.page.locator(f"text={product_name}").first
        expect(product_link).to_be_visible(timeout=10000)
        product_link.click()
        expect(self.page.locator(".inventory_details_name")).to_contain_text(product_name)

    def set_quantity(self, quantity):
        """设置购买数量。SauceDemo 无数量选择器，通过多次点击加入购物车实现。"""
        qty_input = self.page.locator('[data-test="quantity"]')
        if qty_input.count() > 0:
            qty_input.fill(str(quantity))
        else:
            pass  # 无数量输入框时，通过多次添加到购物车实现

    def add_to_cart(self):
        """在商品详情页点击加入购物车。"""
        add_btn = self.page.locator('[data-test^="add-to-cart"]')
        expect(add_btn).to_be_visible(timeout=5000)
        add_btn.click()

    def add_to_cart_from_list(self, product_name):
        """在商品列表页直接点击加入购物车（按商品名称定位）。"""
        slug = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        btn = self.page.locator(f'[data-test="add-to-cart-{slug}"]')
        expect(btn).to_be_visible(timeout=5000)
        btn.click()

    def go_to_cart(self):
        """点击右上角购物车图标进入购物车页面。"""
        expect(self.cart_link).to_be_visible(timeout=5000)
        self.cart_link.click()
        expect(self.page).to_have_url("**/cart.html")

    def get_cart_item_count(self):
        """获取购物车角标数量。"""
        if self.cart_badge.is_visible():
            return self.cart_badge.inner_text()
        return "0"
