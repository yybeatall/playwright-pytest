# 结算页面对象
from playwright.sync_api import Page
from tests.data.test_data import TestData


class CheckoutPage:
    """结算页面对象模型"""

    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.first_name_input = "#first-name"
        self.last_name_input = "#last-name"
        self.postal_code_input = "#postal-code"
        self.continue_button = "#continue"
        self.finish_button = "#finish"
        self.cancel_button = "#cancel"
        self.error_message = ".error-message-container.error"
        self.complete_header = ".complete-header"

    def fill_shipping_information(self, first_name: str, last_name: str, postal_code: str):
        """填写收货信息"""
        self.page.fill(self.first_name_input, first_name)
        self.page.fill(self.last_name_input, last_name)
        self.page.fill(self.postal_code_input, postal_code)

    def click_continue(self):
        """点击继续按钮"""
        self.page.click(self.continue_button)

    def click_finish(self):
        """点击完成按钮"""
        self.page.click(self.finish_button)

    def click_cancel(self):
        """点击取消按钮"""
        self.page.click(self.cancel_button)

    def get_error_message(self) -> str:
        """获取错误信息"""
        self.page.wait_for_selector(self.error_message, timeout=TestData.TIMEOUT)
        return self.page.locator(self.error_message).text_content()

    def is_error_message_visible(self) -> bool:
        """检查错误信息是否可见"""
        return self.page.locator(self.error_message).is_visible(timeout=TestData.TIMEOUT)

    def is_order_complete(self) -> bool:
        """检查订单是否完成"""
        self.page.wait_for_selector(self.complete_header, timeout=TestData.TIMEOUT)
        return self.page.locator(self.complete_header).text_content() == "Thank you for your order!"
