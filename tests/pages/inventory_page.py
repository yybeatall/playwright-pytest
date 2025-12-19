# 商品列表页面对象
from playwright.sync_api import Page
from tests.data.test_data import TestData


class InventoryPage:
    """商品列表页面对象模型"""

    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.page_title = ".title"
        self.product_sort_container = "[data-test='product-sort-container']"
        self.inventory_items = ".inventory_item"
        self.inventory_item_names = ".inventory_item_name"
        self.inventory_item_prices = ".inventory_item_price"
        self.add_to_cart_buttons = ".btn_inventory"
        self.shopping_cart_badge = ".shopping_cart_badge"
        self.shopping_cart_link = ".shopping_cart_link"

    def is_page_loaded(self) -> bool:
        """检查商品列表页是否加载完成"""
        self.page.wait_for_selector(self.page_title, timeout=TestData.TIMEOUT)
        return self.page.locator(self.page_title).text_content() == "Products"

    def get_product_names(self) -> list:
        """获取所有商品名称"""
        return [item.text_content() for item in self.page.locator(self.inventory_item_names).all()]

    def get_product_prices(self) -> list:
        """获取所有商品价格"""
        return [
            float(item.text_content().replace("$", ""))
            for item in self.page.locator(self.inventory_item_prices).all()
        ]

    def sort_products(self, sort_option: str):
        """按指定条件排序商品"""
        self.page.select_option(self.product_sort_container, sort_option)
        self.page.wait_for_selector(self.inventory_items)  # 等待排序完成

    def add_product_to_cart(self, product_index: int = 0):
        """添加商品到购物车"""
        self.page.locator(self.add_to_cart_buttons).nth(product_index).click()

    def get_shopping_cart_badge_count(self) -> str:
        """获取购物车徽章数量"""
        return self.page.locator(self.shopping_cart_badge).text_content()

    def click_shopping_cart(self):
        """点击购物车图标"""
        self.page.click(self.shopping_cart_link)

    def click_product(self, product_index: int = 0):
        """点击商品进入详情页"""
        self.page.locator(self.inventory_item_names).nth(product_index).click()
