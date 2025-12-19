# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.product_detail_page import ProductDetailPage
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutPage
from tests.test_data import (
    BASE_URL,
    VALID_USER,
    LOCKED_USER,
    INVALID_USER,
    EMPTY_USER,
    SHIPPING_INFO,
    SORT_OPTIONS,
    ERROR_MESSAGES,
    TIMEOUTS
)


class TestSauceDemo:
    """SauceDemo 网站的完整 UI 自动化测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置条件：初始化页面对象并导航到测试网站"""
        self.page = page
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.product_detail_page = ProductDetailPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.login_page.goto(BASE_URL)

    def test_login_with_valid_credentials(self):
        """测试使用有效凭证登录"""
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        assert self.inventory_page.get_title() == "Products"
        assert self.inventory_page.get_product_count() > 0

    def test_login_with_invalid_credentials(self):
        """测试使用无效凭证登录（失败场景）"""
        self.login_page.login(INVALID_USER["username"], INVALID_USER["password"])
        assert self.login_page.is_error_message_visible()
        assert self.login_page.get_error_message() == ERROR_MESSAGES["invalid_credentials"]

    def test_login_with_empty_credentials(self):
        """测试使用空凭证登录（失败场景）"""
        self.login_page.login(EMPTY_USER["username"], EMPTY_USER["password"])
        assert self.login_page.is_error_message_visible()
        assert self.login_page.get_error_message() == ERROR_MESSAGES["empty_username"]

    def test_login_with_locked_user(self):
        """测试锁定用户登录（失败场景）"""
        self.login_page.login(LOCKED_USER["username"], LOCKED_USER["password"])
        assert self.login_page.is_error_message_visible()
        assert self.login_page.get_error_message() == ERROR_MESSAGES["locked_user"]

    def test_browse_and_filter_products(self):
        """测试浏览和筛选商品"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 验证商品列表显示
        assert self.inventory_page.get_product_count() > 0
        
        # 测试各种排序选项
        for sort_option in SORT_OPTIONS.values():
            self.inventory_page.sort_products(sort_option)
            # 验证排序后仍有商品
            assert self.inventory_page.get_product_count() > 0

    def test_view_product_details(self):
        """测试查看商品详情"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 进入第一个商品的详情页
        self.inventory_page.go_to_product_detail(0)
        
        # 验证商品详情信息
        assert self.product_detail_page.get_product_name() is not None
        assert self.product_detail_page.get_product_price() is not None
        assert "$" in self.product_detail_page.get_product_price()

    def test_add_product_from_list_page(self):
        """测试从商品列表页添加商品到购物车"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 添加商品到购物车
        self.inventory_page.add_to_cart(0)
        
        # 验证购物车中有商品
        assert self.inventory_page.get_cart_badge_count() == 1

    def test_add_product_from_detail_page(self):
        """测试从商品详情页添加商品到购物车"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 进入商品详情页
        self.inventory_page.go_to_product_detail(0)
        
        # 添加商品到购物车
        self.product_detail_page.add_to_cart()
        
        # 返回商品列表页
        self.product_detail_page.go_back_to_inventory()
        
        # 验证购物车中有商品
        assert self.inventory_page.get_cart_badge_count() == 1

    def test_view_and_edit_cart(self):
        """测试查看和编辑购物车"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 添加多个商品到购物车
        self.inventory_page.add_to_cart(0)
        self.inventory_page.add_to_cart(1)
        
        # 验证购物车中有 2 个商品
        assert self.inventory_page.get_cart_badge_count() == 2
        
        # 导航到购物车
        self.inventory_page.go_to_cart()
        
        # 验证购物车中有 2 个商品
        assert self.cart_page.get_cart_item_count() == 2
        
        # 移除一个商品
        self.cart_page.remove_item(0)
        
        # 验证购物车中剩余 1 个商品
        assert self.cart_page.get_cart_item_count() == 1

    def test_checkout_flow(self):
        """测试完整的结算流程"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 添加商品到购物车
        self.inventory_page.add_to_cart(0)
        
        # 导航到购物车
        self.inventory_page.go_to_cart()
        
        # 开始结算
        self.cart_page.checkout()
        
        # 填写配送信息
        self.checkout_page.fill_shipping_info(
            SHIPPING_INFO["first_name"],
            SHIPPING_INFO["last_name"],
            SHIPPING_INFO["postal_code"]
        )
        self.checkout_page.continue_to_shipping()
        
        # 完成订单
        self.checkout_page.finish_checkout()
        
        # 验证订单完成
        assert self.checkout_page.get_complete_header() == "Thank you for your order!"
        assert "Your order has been dispatched" in self.checkout_page.get_complete_text()

    def test_checkout_without_shipping_info(self):
        """测试未填写配送信息的结算（失败场景）"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 添加商品到购物车
        self.inventory_page.add_to_cart(0)
        
        # 导航到购物车
        self.inventory_page.go_to_cart()
        
        # 开始结算
        self.cart_page.checkout()
        
        # 直接继续，不填写配送信息
        self.checkout_page.continue_to_shipping()
        
        # 验证错误信息
        assert self.checkout_page.get_error_message() == ERROR_MESSAGES["first_name_required"]

    def test_cancel_checkout(self):
        """测试取消下单场景"""
        # 登录
        self.login_page.login(VALID_USER["username"], VALID_USER["password"])
        
        # 添加商品到购物车
        self.inventory_page.add_to_cart(0)
        
        # 导航到购物车
        self.inventory_page.go_to_cart()
        
        # 开始结算
        self.cart_page.checkout()
        
        # 填写配送信息
        self.checkout_page.fill_shipping_info(
            SHIPPING_INFO["first_name"],
            SHIPPING_INFO["last_name"],
            SHIPPING_INFO["postal_code"]
        )
        self.checkout_page.continue_to_shipping()
        
        # 验证订单摘要页面
        assert self.page.url == "https://www.saucedemo.com/checkout-step-two.html"
        
        # 取消下单
        self.page.click("[data-test='cancel']")
        
        # 验证是否返回商品列表页面
        assert self.inventory_page.get_title() == "Products"
        assert self.page.url == "https://www.saucedemo.com/inventory.html"
