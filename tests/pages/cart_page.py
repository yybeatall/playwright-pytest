# 购物车页面对象
from playwright.sync_api import Page
from tests.data.test_data import TestData


class CartPage:
    """购物车页面对象模型"""

    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.page_title = ".title"
        self.cart_items = ".cart_item"
        self.remove_buttons = ".cart_button"
        self.checkout_button = "#checkout"
        self.continue_shopping_button = "#continue-shopping"

    def is_page_loaded(self) -> bool:
        """检查购物车页是否加载完成"""
        self.page.wait_for_selector(self.page_title, timeout=TestData.TIMEOUT)
        return self.page.locator(self.page_title).text_content() == "Your Cart"

    def get_cart_item_count(self) -> int:
        """获取购物车商品数量"""
        # 不等待元素，直接计数，因为商品可能被移除
        return self.page.locator(self.cart_items).count()

    def remove_product_from_cart(self, product_index: int = 0):
        """从购物车移除商品"""
        self.page.wait_for_selector(self.remove_buttons, timeout=TestData.TIMEOUT)
        self.page.locator(self.remove_buttons).nth(product_index).click()

    def click_checkout(self):
        """点击结算按钮"""
        self.page.wait_for_selector(self.checkout_button, timeout=TestData.TIMEOUT)
        self.page.click(self.checkout_button)

    def click_continue_shopping(self):
        """点击继续购物按钮"""
        self.page.wait_for_selector(self.continue_shopping_button, timeout=TestData.TIMEOUT)
        self.page.click(self.continue_shopping_button)
