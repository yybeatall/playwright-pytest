from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage

class LoginPage(BasePage):
    """登录页面对象类"""
    
    # 元素定位器
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        
    def load(self):
        """加载登录页面"""
        self.navigate("https://www.saucedemo.com/")
        
    def login(self, username: str, password: str):
        """执行登录操作"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        
    def verify_error_message(self, expected_message: str):
        """验证错误消息"""
        expect(self.page.locator(self.ERROR_MESSAGE)).to_have_text(expected_message)