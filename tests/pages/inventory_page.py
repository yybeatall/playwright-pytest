from playwright.sync_api import Page, expect
from tests.pages.base_page import BasePage

class InventoryPage(BasePage):
    """商品列表页面对象类"""
    
    # 元素定位器
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    PRODUCT_ITEM = ".inventory_item"
    PRODUCT_NAME = ".inventory_item_name"
    PRODUCT_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "[data-test='add-to-cart-sauce-labs-backpack']"
    CART_ICON = ".shopping_cart_link"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        
    def sort_products(self, sort_option: str):
        """对商品进行排序"""
        self.page.select_option(self.SORT_DROPDOWN, value=sort_option)
        
    def get_product_names(self) -> list:
        """获取所有商品名称"""
        return [name.text_content() for name in self.page.locator(self.PRODUCT_NAME).all()]
        
    def get_product_prices(self) -> list:
        """获取所有商品价格"""
        return [float(price.text_content().replace('$', '')) for price in self.page.locator(self.PRODUCT_PRICE).all()]
        
    def add_product_to_cart(self, product_name: str):
        """将指定商品添加到购物车"""
        button_selector = f"[data-test='add-to-cart-{product_name.lower().replace(' ', '-')}']"
        self.click(button_selector)
        
    def go_to_cart(self):
        """进入购物车页面"""
        self.click(self.CART_ICON)
        
    def verify_cart_count(self, count: int):
        """验证购物车商品数量"""
        expect(self.page.locator(".shopping_cart_badge")).to_have_text(str(count))