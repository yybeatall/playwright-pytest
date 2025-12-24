from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    """购物车页面对象"""
    
    URL = "https://www.saucedemo.com/cart.html"
    
    # 元素定位器
    CART_ITEM = ".cart_item"
    CHECKOUT_BUTTON = "#checkout"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def remove_product(self, product_name: str):
        """从购物车中移除指定商品"""
        self.page.click(f"[data-test='remove-{product_name.lower().replace(' ', '-')}']")
    
    def click_checkout(self):
        """点击结算按钮"""
        self.page.click(self.CHECKOUT_BUTTON)