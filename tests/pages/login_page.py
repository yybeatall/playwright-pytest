# 登录页面对象
from playwright.sync_api import Page
from tests.data.test_data import TestData


class LoginPage:
    """登录页面对象模型"""

    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = ".error-message-container.error"

    def navigate(self):
        """导航到登录页面"""
        self.page.goto("https://www.saucedemo.com/")
        self.page.wait_for_selector(self.username_input, timeout=TestData.TIMEOUT)  # 等待用户名输入框加载

    def login(self, username: str, password: str):
        """执行登录操作"""
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

    def get_error_message(self) -> str:
        """获取错误信息文本"""
        self.page.wait_for_selector(self.error_message, timeout=TestData.TIMEOUT)
        return self.page.locator(self.error_message).text_content()

    def is_error_message_visible(self) -> bool:
        """检查错误信息是否可见"""
        return self.page.locator(self.error_message).is_visible(timeout=TestData.TIMEOUT)
