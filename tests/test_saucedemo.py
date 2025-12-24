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


@pytest.fixture(scope="function")
def setup(page: Page):
    """Test setup: navigate to the website and ensure we're on the login page"""
    page.goto("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")
    expect(page.locator("#login_button_container")).to_be_visible()
    return page


def test_successful_login(setup: Page):
    """Test successful login with valid credentials"""
    page = setup
    
    # Enter valid credentials
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Verify login success
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator("#inventory_container").first).to_be_visible()


def test_failed_login_invalid_credentials(setup: Page):
    """Test failed login with invalid credentials"""
    page = setup
    
    # Enter invalid credentials
    page.locator("#user-name").fill("invalid_user")
    page.locator("#password").fill("invalid_pass")
    page.locator("#login-button").click()
    
    # Verify error message
    error_msg = page.locator("[data-test='error']")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("Username and password do not match any user in this service")


def test_failed_login_empty_fields(setup: Page):
    """Test failed login with empty fields"""
    page = setup
    
    # Click login without entering credentials
    page.locator("#login-button").click()
    
    # Verify error message
    error_msg = page.locator("[data-test='error']")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("Username is required")


def test_failed_login_locked_user(setup: Page):
    """Test failed login with locked user account"""
    page = setup
    
    # Enter locked user credentials
    page.locator("#user-name").fill("locked_out_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Verify error message
    error_msg = page.locator("[data-test='error']")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("Sorry, this user has been locked out")


def test_browse_products(setup: Page):
    """Test browsing products on inventory page"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Verify inventory page and products
    expect(page.locator("#inventory_container").first).to_be_visible()
    expect(page.locator(".inventory_item").first).to_be_visible()
    
    # Verify number of products
    product_count = page.locator(".inventory_item").count()
    assert product_count == 6, f"Expected 6 products, found {product_count}"


def test_sort_products(setup: Page):
    """Test sorting products by different criteria"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Wait for inventory page to load completely
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator("#inventory_container").first).to_be_visible()
    
    # Test sorting by Name (A to Z)
    sort_container = page.locator("[data-test='product-sort-container']")
    expect(sort_container).to_be_visible()
    sort_container.select_option("az")
    first_product = page.locator(".inventory_item_name").first.inner_text()
    assert first_product == "Sauce Labs Backpack"
    
    # Test sorting by Name (Z to A)
    sort_container.select_option("za")
    first_product = page.locator(".inventory_item_name").first.inner_text()
    assert first_product == "Test.allTheThings() T-Shirt (Red)"
    
    # Test sorting by Price (low to high)
    sort_container.select_option("lohi")
    first_price = page.locator(".inventory_item_price").first.inner_text()
    assert first_price == "$7.99"
    
    # Test sorting by Price (high to low)
    sort_container.select_option("hilo")
    first_price = page.locator(".inventory_item_price").first.inner_text()
    assert first_price == "$49.99"


def test_view_product_details(setup: Page):
    """Test viewing product details from inventory page"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Click on first product
    page.locator(".inventory_item_name").first.click()
    
    # Verify product details page
    expect(page).to_have_url(re.compile(r"https://www.saucedemo.com/inventory-item.html\?id=\d+"))
    expect(page.locator("#inventory_item_container")).to_be_visible()
    
    # Verify product information
    expect(page.locator(".inventory_details_name")).to_contain_text("Sauce Labs Backpack")
    expect(page.locator(".inventory_details_price")).to_contain_text("$29.99")


def test_add_product_to_cart_from_inventory(setup: Page):
    """Test adding product to cart from inventory page"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    
    # Verify cart badge
    expect(page.locator(".shopping_cart_badge")).to_be_visible()
    expect(page.locator(".shopping_cart_badge")).to_contain_text("1")


def test_add_product_to_cart_from_details(setup: Page):
    """Test adding product to cart from product details page"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Go to product details
    page.locator(".inventory_item_name").first.click()
    
    # Add product to cart
    page.locator("[data-test='add-to-cart']").click()
    
    # Verify cart badge
    expect(page.locator(".shopping_cart_badge")).to_be_visible()
    expect(page.locator(".shopping_cart_badge")).to_contain_text("1")


def test_view_cart(setup: Page):
    """Test viewing cart contents"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    
    # Go to cart
    page.locator(".shopping_cart_link").click()
    
    # Verify cart page and product
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    expect(page.locator("#cart_contents_container")).to_be_visible()
    expect(page.locator(".inventory_item_name")).to_contain_text("Sauce Labs Backpack")


def test_remove_product_from_cart(setup: Page):
    """Test removing product from cart"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    
    # Go to cart
    page.locator(".shopping_cart_link").click()
    
    # Remove product
    page.locator("[data-test='remove-sauce-labs-backpack']").click()
    
    # Verify cart is empty
    expect(page.locator(".shopping_cart_badge")).not_to_be_visible()
    expect(page.locator(".cart_item")).not_to_be_visible()


def test_checkout_flow(setup: Page):
    """Test complete checkout flow"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    
    # Go to cart and checkout
    page.locator(".shopping_cart_link").click()
    page.locator("[data-test='checkout']").click()
    
    # Fill checkout information
    page.locator("[data-test='firstName']").fill("John")
    page.locator("[data-test='lastName']").fill("Doe")
    page.locator("[data-test='postalCode']").fill("12345")
    page.locator("[data-test='continue']").click()
    
    # Verify checkout overview
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    expect(page.locator("#checkout_summary_container")).to_be_visible()
    expect(page.locator(".summary_subtotal_label")).to_contain_text("$29.99")
    expect(page.locator(".summary_total_label")).to_contain_text("$32.39")
    
    # Complete checkout
    page.locator("[data-test='finish']").click()
    
    # Verify order completion
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    expect(page.locator("#checkout_complete_container")).to_be_visible()
    expect(page.locator(".complete-header")).to_contain_text("Thank you for your order!")


def test_checkout_empty_cart(setup: Page):
    """Test checkout with empty cart"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Go to cart and try to checkout
    page.locator(".shopping_cart_link").click()
    
    # Verify cart is empty
    expect(page.locator(".shopping_cart_badge")).not_to_be_visible()


def test_checkout_missing_information(setup: Page):
    """Test checkout with missing information"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Add product to cart
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    
    # Go to cart and checkout
    page.locator(".shopping_cart_link").click()
    page.locator("[data-test='checkout']").click()
    
    # Try to continue without filling information
    page.locator("[data-test='continue']").click()
    
    # Verify error message
    error_msg = page.locator("[data-test='error']")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("First Name is required")


def test_logout(setup: Page):
    """Test logout functionality"""
    page = setup
    
    # Login first
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    
    # Open menu and logout
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    
    # Verify logout success
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator("#login_button_container")).to_be_visible()