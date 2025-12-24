from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """商品列表页面对象"""
    
    URL = "https://www.saucedemo.com/inventory.html"
    
    # 元素定位器
    INVENTORY_CONTAINER = ".inventory_container"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    SHOPPING_CART_BADGE = "#shopping_cart_container .shopping_cart_badge"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def sort_products(self, sort_option: str):
        """按指定选项排序商品"""
        self.page.select_option(self.SORT_DROPDOWN, sort_option)
    
    def add_to_cart(self, product_name: str):
        """将指定商品加入购物车"""
        self.page.click(f"[data-test='add-to-cart-{product_name.lower().replace(' ', '-')}']")
    
    def click_product(self, product_name: str):
        """点击指定商品进入详情页"""
        self.page.click(f"[data-test='item-title-link'][data-test*='{product_name.lower().replace(' ', '-')}']")
    
    def get_first_product_name(self):
        """获取第一个商品的名称"""
        return self.page.locator(self.INVENTORY_ITEM_NAME).first.text_content()
    
    def get_first_product_price(self):
        """获取第一个商品的价格"""
        return self.page.locator(self.INVENTORY_ITEM_PRICE).first.text_content()