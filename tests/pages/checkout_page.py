from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage

class CheckoutPage(BasePage):
    """结算页面对象类"""
    
    # 元素定位器
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        
    def fill_personal_info(self, first_name: str, last_name: str, postal_code: str):
        """填写个人信息"""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        
    def continue_to_checkout(self):
        """继续结算流程"""
        self.click(self.CONTINUE_BUTTON)
        
    def cancel_checkout(self):
        """取消结算流程"""
        self.click(self.CANCEL_BUTTON)
        
    def verify_error_message(self, expected_message: str):
        """验证错误消息"""
        expect(self.page.locator(self.ERROR_MESSAGE)).to_have_text(expected_message)