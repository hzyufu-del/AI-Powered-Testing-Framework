from playwright.sync_api import expect


class CartPage:
    def __init__(self, page):
        self.page = page
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.item_quantities = page.locator(".cart_quantity")

    def get_product_name(self, index=0):
        """获取购物车中第 index 个商品的名称。"""
        locator = self.item_names.nth(index)
        expect(locator).to_be_visible(timeout=5000)
        return locator.inner_text()

    def get_unit_price(self, index=0):
        """获取购物车中第 index 个商品的单价（返回 float）。"""
        locator = self.item_prices.nth(index)
        expect(locator).to_be_visible(timeout=5000)
        price_text = locator.inner_text()  # "$29.99"
        return float(price_text.replace("$", ""))

    def get_quantity(self, index=0):
        """获取购物车中第 index 个商品的数量（返回 int）。"""
        locator = self.item_quantities.nth(index)
        expect(locator).to_be_visible(timeout=5000)
        return int(locator.inner_text())

    def get_total_price(self, index=0):
        """计算并返回购物车中第 index 个商品的总价（单价 * 数量）。"""
        return self.get_unit_price(index) * self.get_quantity(index)
