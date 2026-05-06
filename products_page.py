class ProductsPage:
    def __init__(self, page):
        self.page = page
        # 1. 定位元素：找到“Sauce Labs Backpack(背包)”的加入购物车按钮
        self.add_backpack_button = page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')
        # 2. 定位元素：找到右上角的购物车图标上的“数字角标”
        self.cart_badge = page.locator(".shopping_cart_badge")

    # 动作 1：点击加入购物车
    def add_backpack_to_cart(self):
        self.add_backpack_button.click()

    # 动作 2：获取购物车里的商品数量（用来做断言）
    def get_cart_item_count(self):
        # 如果角标可见，返回里面的数字文本，否则返回 "0"
        if self.cart_badge.is_visible():
            return self.cart_badge.inner_text()
        return "0"