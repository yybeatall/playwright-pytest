from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """结算页面对象"""
    
    URL_STEP_1 = "https://www.saucedemo.com/checkout-step-one.html"
    URL_STEP_2 = "https://www.saucedemo.com/checkout-step-two.html"
    URL_COMPLETE = "https://www.saucedemo.com/checkout-complete.html"
    
    # 元素定位器
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    FINISH_BUTTON = "#finish"
    BACK_TO_PRODUCTS_BUTTON = "#back-to-products"
    COMPLETE_HEADER = ".complete-header"
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def enter_personal_info(self, first_name: str, last_name: str, postal_code: str):
        """输入个人信息"""
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.POSTAL_CODE_INPUT, postal_code)
    
    def click_continue(self):
        """点击继续按钮"""
        self.page.click(self.CONTINUE_BUTTON)
    
    def click_finish(self):
        """点击完成按钮"""
        self.page.click(self.FINISH_BUTTON)
    
    def click_back_to_products(self):
        """点击返回商品列表按钮"""
        self.page.click(self.BACK_TO_PRODUCTS_BUTTON)