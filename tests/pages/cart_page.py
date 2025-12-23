from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage

class CartPage(BasePage):
    """购物车页面对象类"""
    
    # 元素定位器
    CART_ITEM = ".cart_item"
    REMOVE_BUTTON = "[data-test='remove-sauce-labs-backpack']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        
    def verify_cart_items_count(self, count: int):
        """验证购物车商品数量"""
        expect(self.page.locator(self.CART_ITEM)).to_have_count(count)
        
    def remove_product_from_cart(self, product_name: str):
        """从购物车移除指定商品"""
        button_selector = f"[data-test='remove-{product_name.lower().replace(' ', '-')}']"
        self.click(button_selector)
        
    def go_to_checkout(self):
        """进入结算页面"""
        self.click(self.CHECKOUT_BUTTON)