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
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.test_data import LOGIN_DATA, PRODUCTS, SORT_OPTIONS, CHECKOUT_DATA, ERROR_MESSAGES, SUCCESS_MESSAGES


@pytest.fixture(scope="function")
def login_page(page: Page):
    """登录页面对象fixture"""
    return LoginPage(page)


@pytest.fixture(scope="function")
def inventory_page(page: Page):
    """商品列表页面对象fixture"""
    return InventoryPage(page)


@pytest.fixture(scope="function")
def cart_page(page: Page):
    """购物车页面对象fixture"""
    return CartPage(page)


@pytest.fixture(scope="function")
def checkout_page(page: Page):
    """结算页面对象fixture"""
    return CheckoutPage(page)


def test_successful_login(login_page: LoginPage, inventory_page: InventoryPage):
    """测试成功登录"""
    # 登录流程
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 验证登录成功，进入商品列表页
    inventory_page.expect_url(inventory_page.URL)
    inventory_page.expect_element_visible(inventory_page.INVENTORY_CONTAINER)


def test_failed_login(login_page: LoginPage):
    """测试登录失败场景"""
    login_page.load()
    login_page.login(LOGIN_DATA["invalid_user"]["username"], LOGIN_DATA["invalid_user"]["password"])
    
    # 验证登录失败，显示错误信息
    login_page.expect_element_visible(login_page.ERROR_MESSAGE)
    login_page.expect_element_contain_text(login_page.ERROR_MESSAGE, ERROR_MESSAGES["invalid_credentials"])


def test_empty_username_login(login_page: LoginPage):
    """测试空用户名登录"""
    login_page.load()
    login_page.enter_password(LOGIN_DATA["valid_user"]["password"])
    login_page.click_login()
    
    # 验证显示错误信息
    login_page.expect_element_visible(login_page.ERROR_MESSAGE)
    login_page.expect_element_contain_text(login_page.ERROR_MESSAGE, ERROR_MESSAGES["username_required"])


def test_empty_password_login(login_page: LoginPage):
    """测试空密码登录"""
    login_page.load()
    login_page.enter_username(LOGIN_DATA["valid_user"]["username"])
    login_page.click_login()
    
    # 验证显示错误信息
    login_page.expect_element_visible(login_page.ERROR_MESSAGE)
    login_page.expect_element_contain_text(login_page.ERROR_MESSAGE, ERROR_MESSAGES["password_required"])


def test_product_browsing_and_sorting(login_page: LoginPage, inventory_page: InventoryPage):
    """测试商品浏览和排序功能"""
    # 先登录
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 验证商品列表显示
    inventory_page.expect_element_visible(inventory_page.INVENTORY_CONTAINER)
    
    # 测试按名称A到Z排序
    inventory_page.sort_products("az")
    first_product_name = inventory_page.get_first_product_name()
    assert first_product_name == PRODUCTS["backpack"]
    
    # 测试按名称Z到A排序
    inventory_page.sort_products("za")
    first_product_name = inventory_page.get_first_product_name()
    assert first_product_name == PRODUCTS["red_t_shirt"]
    
    # 测试按价格从低到高排序
    inventory_page.sort_products("lohi")
    first_product_price = inventory_page.get_first_product_price()
    assert first_product_price == "$7.99"
    
    # 测试按价格从高到低排序
    inventory_page.sort_products("hilo")
    first_product_price = inventory_page.get_first_product_price()
    assert first_product_price == "$49.99"


def test_product_details(login_page: LoginPage, inventory_page: InventoryPage):
    """测试商品详情页"""
    # 先登录
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 点击第一个商品（使用page对象的first定位器）
    inventory_page.page.locator(inventory_page.INVENTORY_ITEM_NAME).first.click()
    
    # 验证进入详情页
    inventory_page.expect_url("regex:https://www.saucedemo.com/inventory-item.html\?id=\\d+")
    inventory_page.expect_element_visible(".inventory_item_container")
    inventory_page.expect_element_visible("#back-to-products")


def test_add_to_cart(login_page: LoginPage, inventory_page: InventoryPage):
    """测试添加商品到购物车"""
    # 先登录
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 从列表页添加第一个商品
    inventory_page.add_to_cart(PRODUCTS["backpack"])
    inventory_page.expect_element_contain_text(inventory_page.SHOPPING_CART_BADGE, "1")
    
    # 从列表页添加第二个商品
    inventory_page.add_to_cart(PRODUCTS["bike_light"])
    inventory_page.expect_element_contain_text(inventory_page.SHOPPING_CART_BADGE, "2")


def test_shopping_cart(login_page: LoginPage, inventory_page: InventoryPage, cart_page: CartPage):
    """测试购物车页面"""
    # 先登录并添加商品
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 添加商品到购物车
    inventory_page.add_to_cart(PRODUCTS["backpack"])
    inventory_page.add_to_cart(PRODUCTS["bike_light"])
    
    # 进入购物车页面
    inventory_page.page.click("#shopping_cart_container")
    cart_page.expect_url(cart_page.URL)
    
    # 验证购物车中的商品
    cart_page.expect_element_contain_text(f"{cart_page.CART_ITEM}:has-text('{PRODUCTS['backpack']}')", PRODUCTS["backpack"])
    cart_page.expect_element_contain_text(f"{cart_page.CART_ITEM}:has-text('{PRODUCTS['bike_light']}')", PRODUCTS["bike_light"])
    
    # 移除商品
    cart_page.remove_product(PRODUCTS["backpack"])
    cart_page.expect_element_count(cart_page.CART_ITEM, 1)
    cart_page.expect_element_contain_text(cart_page.CART_ITEM, PRODUCTS["bike_light"])


def test_checkout_flow(login_page: LoginPage, inventory_page: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试结算下单流程"""
    # 先登录并添加商品
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 添加商品到购物车
    inventory_page.add_to_cart(PRODUCTS["backpack"])
    
    # 进入购物车页面
    inventory_page.page.click("#shopping_cart_container")
    
    # 点击Checkout按钮
    cart_page.click_checkout()
    checkout_page.expect_url(checkout_page.URL_STEP_1)
    
    # 填写信息
    checkout_page.enter_personal_info(
        CHECKOUT_DATA["valid_info"]["first_name"],
        CHECKOUT_DATA["valid_info"]["last_name"],
        CHECKOUT_DATA["valid_info"]["postal_code"]
    )
    checkout_page.click_continue()
    
    # 验证订单预览页
    checkout_page.expect_url(checkout_page.URL_STEP_2)
    checkout_page.expect_element_visible(checkout_page.FINISH_BUTTON)
    
    # 点击Finish完成订单
    checkout_page.click_finish()
    checkout_page.expect_url(checkout_page.URL_COMPLETE)
    checkout_page.expect_element_visible(checkout_page.BACK_TO_PRODUCTS_BUTTON)
    checkout_page.expect_element_contain_text(checkout_page.COMPLETE_HEADER, SUCCESS_MESSAGES["order_complete"])


def test_checkout_empty_info(login_page: LoginPage, inventory_page: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试结算时信息为空的失败场景"""
    # 先登录并添加商品
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 添加商品到购物车
    inventory_page.add_to_cart(PRODUCTS["backpack"])
    
    # 进入购物车页面
    inventory_page.page.click("#shopping_cart_container")
    
    # 点击Checkout按钮
    cart_page.click_checkout()
    
    # 不填写信息直接点击Continue
    checkout_page.click_continue()
    
    # 验证错误信息
    checkout_page.expect_element_visible(checkout_page.ERROR_MESSAGE)
    checkout_page.expect_element_contain_text(checkout_page.ERROR_MESSAGE, ERROR_MESSAGES["first_name_required"])


def test_checkout_invalid_info(login_page: LoginPage, inventory_page: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试结算时信息无效的失败场景"""
    # 先登录并添加商品
    login_page.load()
    login_page.login(LOGIN_DATA["valid_user"]["username"], LOGIN_DATA["valid_user"]["password"])
    
    # 添加商品到购物车
    inventory_page.add_to_cart(PRODUCTS["backpack"])
    
    # 进入购物车页面
    inventory_page.page.click("#shopping_cart_container")
    
    # 点击Checkout按钮
    cart_page.click_checkout()
    
    # 填写部分信息
    checkout_page.enter_personal_info(
        CHECKOUT_DATA["partial_info"]["first_name"],
        CHECKOUT_DATA["partial_info"]["last_name"],
        CHECKOUT_DATA["partial_info"]["postal_code"]
    )
    checkout_page.click_continue()
    
    # 验证错误信息
    checkout_page.expect_element_visible(checkout_page.ERROR_MESSAGE)
    checkout_page.expect_element_contain_text(checkout_page.ERROR_MESSAGE, ERROR_MESSAGES["last_name_required"])