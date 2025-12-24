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
import re
from playwright.sync_api import Page, expect


def test_successful_login(page: Page):
    """测试成功登录"""
    page.goto("https://www.saucedemo.com/")
    
    # 输入正确的用户名和密码
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 验证登录成功，进入商品列表页
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".inventory_container")).to_be_visible()


def test_failed_login(page: Page):
    """测试登录失败场景"""
    page.goto("https://www.saucedemo.com/")
    
    # 输入错误的用户名和密码
    page.fill("#user-name", "invalid_user")
    page.fill("#password", "invalid_password")
    page.click("#login-button")
    
    # 验证登录失败，显示错误信息
    expect(page.locator("[data-test='error']")).to_be_visible()
    expect(page.locator("[data-test='error']")).to_contain_text("Epic sadface: Username and password do not match any user in this service")


def test_empty_username_login(page: Page):
    """测试空用户名登录"""
    page.goto("https://www.saucedemo.com/")
    
    # 只输入密码
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 验证显示错误信息
    expect(page.locator("[data-test='error']")).to_be_visible()
    expect(page.locator("[data-test='error']")).to_contain_text("Epic sadface: Username is required")


def test_empty_password_login(page: Page):
    """测试空密码登录"""
    page.goto("https://www.saucedemo.com/")
    
    # 只输入用户名
    page.fill("#user-name", "standard_user")
    page.click("#login-button")
    
    # 验证显示错误信息
    expect(page.locator("[data-test='error']")).to_be_visible()
    expect(page.locator("[data-test='error']")).to_contain_text("Epic sadface: Password is required")


def test_product_browsing_and_sorting(page: Page):
    """测试商品浏览和排序功能"""
    # 先登录
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 验证商品列表显示
    expect(page.locator(".inventory_item").first).to_be_visible()
    
    # 测试按名称A到Z排序
    page.select_option("[data-test='product-sort-container']", "az")
    expect(page.locator(".inventory_item_name").first).to_contain_text("Sauce Labs Backpack")
    
    # 测试按名称Z到A排序
    page.select_option("[data-test='product-sort-container']", "za")
    expect(page.locator(".inventory_item_name").first).to_contain_text("Test.allTheThings() T-Shirt (Red)")
    
    # 测试按价格从低到高排序
    page.select_option("[data-test='product-sort-container']", "lohi")
    expect(page.locator(".inventory_item_price").first).to_contain_text("$7.99")
    
    # 测试按价格从高到低排序
    page.select_option("[data-test='product-sort-container']", "hilo")
    expect(page.locator(".inventory_item_price").first).to_contain_text("$49.99")


def test_product_details(page: Page):
    """测试商品详情页"""
    # 先登录
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 点击第一个商品
    page.click(".inventory_item_name")
    
    # 验证进入详情页
    expect(page).to_have_url(re.compile(r"https://www.saucedemo.com/inventory-item.html\?id=\d+"))
    expect(page.locator(".inventory_item_container")).to_be_visible()
    expect(page.locator("#back-to-products")).to_be_visible()


def test_add_to_cart(page: Page):
    """测试添加商品到购物车"""
    # 先登录
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 从列表页添加第一个商品
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    expect(page.locator("#shopping_cart_container .shopping_cart_badge")).to_contain_text("1")
    
    # 从列表页添加第二个商品
    page.click("[data-test='add-to-cart-sauce-labs-bike-light']")
    expect(page.locator("#shopping_cart_container .shopping_cart_badge")).to_contain_text("2")


def test_shopping_cart(page: Page):
    """测试购物车页面"""
    # 先登录并添加商品
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 添加商品到购物车
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("[data-test='add-to-cart-sauce-labs-bike-light']")
    
    # 进入购物车页面
    page.click("#shopping_cart_container")
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    
    # 验证购物车中的商品
    expect(page.locator(".cart_item").first).to_contain_text("Sauce Labs Backpack")
    expect(page.locator(".cart_item").nth(1)).to_contain_text("Sauce Labs Bike Light")
    
    # 移除商品
    page.click("[data-test='remove-sauce-labs-backpack']")
    expect(page.locator(".cart_item")).to_have_count(1)
    expect(page.locator(".cart_item").first).to_contain_text("Sauce Labs Bike Light")


def test_checkout_flow(page: Page):
    """测试结算下单流程"""
    # 先登录并添加商品
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 添加商品到购物车
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    
    # 进入购物车页面
    page.click("#shopping_cart_container")
    
    # 点击Checkout按钮
    page.click("#checkout")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
    
    # 填写信息
    page.fill("#first-name", "John")
    page.fill("#last-name", "Doe")
    page.fill("#postal-code", "12345")
    page.click("#continue")
    
    # 验证订单预览页
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    expect(page.locator("#finish")).to_be_visible()
    
    # 点击Finish完成订单
    page.click("#finish")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    expect(page.locator("#back-to-products")).to_be_visible()
    expect(page.locator(".complete-header")).to_contain_text("Thank you for your order!")


def test_checkout_empty_info(page: Page):
    """测试结算时信息为空的失败场景"""
    # 先登录并添加商品
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 添加商品到购物车
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    
    # 进入购物车页面
    page.click("#shopping_cart_container")
    
    # 点击Checkout按钮
    page.click("#checkout")
    
    # 不填写信息直接点击Continue
    page.click("#continue")
    
    # 验证错误信息
    expect(page.locator("[data-test='error']")).to_be_visible()
    expect(page.locator("[data-test='error']")).to_contain_text("Error: First Name is required")


def test_checkout_invalid_info(page: Page):
    """测试结算时信息无效的失败场景"""
    # 先登录并添加商品
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    
    # 添加商品到购物车
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    
    # 进入购物车页面
    page.click("#shopping_cart_container")
    
    # 点击Checkout按钮
    page.click("#checkout")
    
    # 填写部分信息
    page.fill("#first-name", "John")
    page.click("#continue")
    
    # 验证错误信息
    expect(page.locator("[data-test='error']")).to_be_visible()
    expect(page.locator("[data-test='error']")).to_contain_text("Error: Last Name is required")