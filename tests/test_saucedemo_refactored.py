# 重构后的 saucedemo 测试脚本
import pytest
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.product_details_page import ProductDetailsPage
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutPage
from tests.data.test_data import TestData


class TestSauceDemoRefactored:
    """重构后的 saucedemo 测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置条件"""
        self.page = page
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.product_details_page = ProductDetailsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.login_page.navigate()

    # 1. 访问与登录功能测试
    def test_login_success(self):
        """测试成功登录场景"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        assert self.inventory_page.is_page_loaded()

    def test_login_failure_with_wrong_password(self):
        """测试使用错误密码登录的失败场景"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.INVALID_PASSWORD)
        assert self.login_page.is_error_message_visible()
        assert TestData.INVALID_CREDENTIALS_ERROR in self.login_page.get_error_message()

    def test_login_failure_with_empty_username(self):
        """测试空用户名登录的失败场景"""
        self.login_page.login(TestData.EMPTY_USERNAME, TestData.VALID_PASSWORD)
        assert self.login_page.is_error_message_visible()
        assert TestData.EMPTY_USERNAME_ERROR in self.login_page.get_error_message()

    # 2. 浏览与筛选商品功能测试
    def test_browse_products(self):
        """测试浏览商品列表"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        assert self.inventory_page.is_page_loaded()
        assert len(self.inventory_page.get_product_names()) > 0

    def test_sort_products_by_name_az(self):
        """测试按商品名称从 A 到 Z 排序"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.sort_products(TestData.SORT_NAME_AZ)
        product_names = self.inventory_page.get_product_names()
        assert product_names == sorted(product_names)

    def test_sort_products_by_price_low_to_high(self):
        """测试按商品价格从低到高排序"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.sort_products(TestData.SORT_PRICE_LOW_TO_HIGH)
        product_prices = self.inventory_page.get_product_prices()
        assert product_prices == sorted(product_prices)

    # 3. 查看商品详情功能测试
    def test_view_product_details(self):
        """测试查看商品详情"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        first_product_name = self.inventory_page.get_product_names()[0]
        self.inventory_page.click_product()
        assert self.product_details_page.is_page_loaded()
        assert self.product_details_page.get_product_name() == first_product_name

    # 4. 添加商品功能测试
    def test_add_product_from_list_page(self):
        """测试从商品列表页添加商品到购物车"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.add_product_to_cart()
        assert self.inventory_page.get_shopping_cart_badge_count() == "1"

    def test_add_product_from_details_page(self):
        """测试从商品详情页添加商品到购物车"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.click_product()
        self.product_details_page.add_to_cart()
        assert self.product_details_page.get_shopping_cart_badge_count() == "1"

    # 5. 查看与编辑购物车功能测试
    def test_view_cart(self):
        """测试查看购物车"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.add_product_to_cart()
        self.inventory_page.click_shopping_cart()
        assert self.cart_page.is_page_loaded()
        assert self.cart_page.get_cart_item_count() == 1

    def test_remove_product_from_cart(self):
        """测试从购物车移除商品"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.add_product_to_cart()
        self.inventory_page.click_shopping_cart()
        self.cart_page.remove_product_from_cart()
        assert self.cart_page.get_cart_item_count() == 0

    # 6. 结算下单功能测试
    def test_checkout_flow(self):
        """测试完整的结算下单流程"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.add_product_to_cart()
        self.inventory_page.click_shopping_cart()
        self.cart_page.click_checkout()
        self.checkout_page.fill_shipping_information(
            TestData.FIRST_NAME, TestData.LAST_NAME, TestData.POSTAL_CODE
        )
        self.checkout_page.click_continue()
        self.checkout_page.click_finish()
        assert self.checkout_page.is_order_complete()

    def test_checkout_failure_with_empty_information(self):
        """测试空信息结算的失败场景"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.add_product_to_cart()
        self.inventory_page.click_shopping_cart()
        self.cart_page.click_checkout()
        self.checkout_page.click_continue()  # 不填写任何信息
        assert self.checkout_page.is_error_message_visible()
        assert TestData.EMPTY_FIRST_NAME_ERROR in self.checkout_page.get_error_message()

    def test_cancel_checkout(self):
        """测试取消下单场景"""
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.inventory_page.add_product_to_cart()
        self.inventory_page.click_shopping_cart()
        self.cart_page.click_checkout()
        self.checkout_page.fill_shipping_information(
            TestData.FIRST_NAME, TestData.LAST_NAME, TestData.POSTAL_CODE
        )
        self.checkout_page.click_continue()
        self.checkout_page.click_cancel()
        assert self.inventory_page.is_page_loaded()

    def test_locked_user_login(self):
        """测试锁定用户登录场景"""
        self.login_page.login(TestData.LOCKED_USERNAME, TestData.VALID_PASSWORD)
        assert self.login_page.is_error_message_visible()
        assert TestData.LOCKED_USER_ERROR in self.login_page.get_error_message()
