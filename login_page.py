class LoginPage:
    # 初始化：把页面元素都存起来
    def __init__(self, page):
        self.page = page
        # 集中管理元素定位（以后网站改版，只改这里就行了！）
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.title_element = page.locator(".title")

    # 动作 1：打开网页
    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    # 动作 2：执行登录
    def login(self, username, password):
        self.page.wait_for_selector('#user-name', state='visible', timeout=10000)
        self.page.locator('#user-name').fill(username)
        self.page.wait_for_selector('#password', state='visible', timeout=10000)
        self.page.locator('#password').fill(password)
        self.page.wait_for_selector('#login-button', state='visible', timeout=10000)
        self.page.locator('#login-button').click()