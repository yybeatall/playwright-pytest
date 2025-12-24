from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """登录页面对象"""
    
    URL = "https://www.saucedemo.com/"
    
    # 元素定位器
    USER_NAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def load(self):
        """加载登录页面"""
        self.navigate(self.URL)
    
    def enter_username(self, username: str):
        """输入用户名"""
        self.page.fill(self.USER_NAME_INPUT, username)
    
    def enter_password(self, password: str):
        """输入密码"""
        self.page.fill(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """点击登录按钮"""
        self.page.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str):
        """完整登录流程"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()