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


class TestSauceDemo:
    """测试 saucedemo.com 网站的完整购物流程"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前的准备工作"""
        self.page = page
        self.base_url = "https://www.saucedemo.com/"
        self.valid_username = "standard_user"
        self.valid_password = "secret_sauce"

    # 1. 访问与登录
    def test_successful_login(self):
        """测试使用有效凭证成功登录"""
        self.page.goto(self.base_url)
        self.page.fill("#user-name", self.valid_username)
        self.page.fill("#password", self.valid_password)
        self.page.click("#login-button")
        assert self.page.url == "https://www.saucedemo.com/inventory.html"
        assert self.page.locator(".title").text_content() == "Products"

    def test_login_with_invalid_username(self):
        """测试使用无效用户名登录"""
        self.page.goto(self.base_url)
        self.page.fill("#user-name", "invalid_user")
        self.page.fill("#password", self.valid_password)
        self.page.click("#login-button")
        error_message = self.page.locator("[data-test='error']").text_content()
        assert "Epic sadface: Username and password do not match any user in this service" in error_message

    def test_login_with_invalid_password(self):
        """测试使用无效密码登录"""
        self.page.goto(self.base_url)
        self.page.fill("#user-name", self.valid_username)
        self.page.fill("#password", "invalid_password")
        self.page.click("#login-button")
        error_message = self.page.locator("[data-test='error']").text_content()
        assert "Epic sadface: Username and password do not match any user in this service" in error_message

    def test_login_with_empty_credentials(self):
        """测试使用空凭证登录"""
        self.page.goto(self.base_url)
        self.page.click("#login-button")
        error_message = self.page.locator("[data-test='error']").text_content()
        assert "Epic sadface: Username is required" in error_message

    # 2. 浏览与筛选商品
    def test_browse_products(self):
        """测试浏览所有商品"""
        self.test_successful_login()
        products = self.page.locator(".inventory_item")
        assert products.count() == 6

    def test_sort_products_by_name_az(self):
        """测试按商品名称从 A 到 Z 排序"""
        self.test_successful_login()
        self.page.select_option("[data-test='product-sort-container']", "az")
        product_names = [item.text_content() for item in self.page.locator(".inventory_item_name").all()]
        assert product_names == sorted(product_names)

    def test_sort_products_by_name_za(self):
        """测试按商品名称从 Z 到 A 排序"""
        self.test_successful_login()
        self.page.select_option("[data-test='product-sort-container']", "za")
        product_names = [item.text_content() for item in self.page.locator(".inventory_item_name").all()]
        assert product_names == sorted(product_names, reverse=True)

    def test_sort_products_by_price_low_to_high(self):
        """测试按商品价格从低到高排序"""
        self.test_successful_login()
        self.page.select_option("[data-test='product-sort-container']", "lohi")
        product_prices = [float(item.text_content().replace("$", "")) for item in self.page.locator(".inventory_item_price").all()]
        assert product_prices == sorted(product_prices)

    def test_sort_products_by_price_high_to_low(self):
        """测试按商品价格从高到低排序"""
        self.test_successful_login()
        self.page.select_option("[data-test='product-sort-container']", "hilo")
        product_prices = [float(item.text_content().replace("$", "")) for item in self.page.locator(".inventory_item_price").all()]
        assert product_prices == sorted(product_prices, reverse=True)

    # 3. 查看商品详情
    def test_view_product_details(self):
        """测试查看商品详情"""
        self.test_successful_login()
        first_product_name = self.page.locator(".inventory_item_name").first.text_content()
        self.page.locator(".inventory_item_name").first.click()
        assert self.page.locator(".inventory_details_name").text_content() == first_product_name
        assert self.page.url.startswith("https://www.saucedemo.com/inventory-item.html")

    # 4. 添加商品
    def test_add_product_from_list_page(self):
        """测试从商品列表页添加商品到购物车"""
        self.test_successful_login()
        self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
        assert self.page.locator("[data-test='shopping-cart-badge']").text_content() == "1"

    def test_add_product_from_details_page(self):
        """测试从商品详情页添加商品到购物车"""
        self.test_successful_login()
        self.page.locator(".inventory_item_name").first.click()
        self.page.locator("[data-test='add-to-cart']").click()
        assert self.page.locator("[data-test='shopping-cart-badge']").text_content() == "1"

    # 5. 查看与编辑购物车
    def test_view_shopping_cart(self):
        """测试查看购物车"""
        self.test_successful_login()
        self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
        self.page.click("[data-test='shopping-cart-link']")
        assert self.page.url == "https://www.saucedemo.com/cart.html"
        assert self.page.locator(".cart_item").count() == 1

    def test_remove_product_from_cart(self):
        """测试从购物车移除商品"""
        self.test_successful_login()
        self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
        self.page.click("[data-test='shopping-cart-link']")
        self.page.locator("[data-test='remove-sauce-labs-backpack']").click()
        assert self.page.locator(".cart_item").count() == 0
        assert self.page.locator("[data-test='shopping-cart-badge']").is_hidden()

    # 6. 结算下单
    def test_complete_checkout_flow(self):
        """测试完整的结算流程"""
        self.test_successful_login()
        self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
        self.page.click("[data-test='shopping-cart-link']")
        self.page.click("[data-test='checkout']")
        self.page.fill("[data-test='firstName']", "John")
        self.page.fill("[data-test='lastName']", "Doe")
        self.page.fill("[data-test='postalCode']", "12345")
        self.page.click("[data-test='continue']")
        assert self.page.locator(".title").text_content() == "Checkout: Overview"
        self.page.click("[data-test='finish']")
        assert self.page.locator(".title").text_content() == "Checkout: Complete!"
        assert self.page.locator(".complete-header").text_content() == "Thank you for your order!"

    def test_checkout_without_shipping_info(self):
        """测试未填写配送信息就继续结算"""
        self.test_successful_login()
        self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
        self.page.click("[data-test='shopping-cart-link']")
        self.page.click("[data-test='checkout']")
        self.page.click("[data-test='continue']")
        error_message = self.page.locator("[data-test='error']").text_content()
        assert "First Name is required" in error_message
