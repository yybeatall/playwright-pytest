# 商品详情页面对象
from playwright.sync_api import Page
from tests.data.test_data import TestData


class ProductDetailsPage:
    """商品详情页面对象模型"""

    def __init__(self, page: Page):
        self.page = page
        # 元素定位器
        self.product_name = ".inventory_details_name.large_size"
        self.add_to_cart_button = ".btn_inventory"
        self.shopping_cart_badge = ".shopping_cart_badge"

    def is_page_loaded(self) -> bool:
        """检查商品详情页是否加载完成"""
        self.page.wait_for_selector(self.product_name, timeout=TestData.TIMEOUT)
        return self.page.locator(self.product_name).is_visible()

    def get_product_name(self) -> str:
        """获取商品名称"""
        self.page.wait_for_selector(self.product_name, timeout=TestData.TIMEOUT)
        return self.page.locator(self.product_name).text_content()

    def add_to_cart(self):
        """添加商品到购物车"""
        self.page.wait_for_selector(self.add_to_cart_button, timeout=TestData.TIMEOUT)
        self.page.click(self.add_to_cart_button)

    def get_shopping_cart_badge_count(self) -> str:
        """获取购物车徽章数量"""
        self.page.wait_for_selector(self.shopping_cart_badge, timeout=TestData.TIMEOUT)
        return self.page.locator(self.shopping_cart_badge).text_content()
