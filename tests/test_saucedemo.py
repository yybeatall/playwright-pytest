import pytest
import re
from playwright.sync_api import Page, expect
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutPage
from tests.test_data import (
    VALID_USERNAME, VALID_PASSWORD, INVALID_USERNAME, INVALID_PASSWORD,
    EMPTY_USERNAME, EMPTY_PASSWORD, INVALID_CREDENTIALS_ERROR,
    EMPTY_USERNAME_ERROR, EMPTY_PASSWORD_ERROR, EMPTY_FIRST_NAME_ERROR,
    PRODUCT_NAME, SORT_OPTIONS, FIRST_NAME, LAST_NAME, POSTAL_CODE
)

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """登录页面对象fixture"""
    return LoginPage(page)

@pytest.fixture(scope="function")
def inventory_page(page: Page) -> InventoryPage:
    """商品列表页面对象fixture"""
    return InventoryPage(page)

@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    """购物车页面对象fixture"""
    return CartPage(page)

@pytest.fixture(scope="function")
def checkout_page(page: Page) -> CheckoutPage:
    """结算页面对象fixture"""
    return CheckoutPage(page)

@pytest.fixture(scope="function")
def authenticated_session(login_page: LoginPage, inventory_page: InventoryPage):
    """已认证的会话fixture"""
    login_page.load()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    return inventory_page

def test_successful_login(login_page: LoginPage, inventory_page: InventoryPage):
    """测试成功登录"""
    login_page.load()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    expect(inventory_page.page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_failed_login_with_invalid_credentials(login_page: LoginPage):
    """测试使用无效凭据登录失败"""
    login_page.load()
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)
    login_page.verify_error_message(INVALID_CREDENTIALS_ERROR)

def test_failed_login_with_empty_username(login_page: LoginPage):
    """测试用户名为空时登录失败"""
    login_page.load()
    login_page.login(EMPTY_USERNAME, VALID_PASSWORD)
    login_page.verify_error_message(EMPTY_USERNAME_ERROR)

def test_failed_login_with_empty_password(login_page: LoginPage):
    """测试密码为空时登录失败"""
    login_page.load()
    login_page.login(VALID_USERNAME, EMPTY_PASSWORD)
    login_page.verify_error_message(EMPTY_PASSWORD_ERROR)

def test_browse_and_sort_products(authenticated_session: InventoryPage):
    """测试浏览和排序商品"""
    inventory_page = authenticated_session
    
    # 按名称升序排序
    inventory_page.sort_products(SORT_OPTIONS["az"])
    names = inventory_page.get_product_names()
    assert names == sorted(names), "商品名称未按升序排序"
    
    # 按价格降序排序
    inventory_page.sort_products(SORT_OPTIONS["hilo"])
    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices, reverse=True), "商品价格未按降序排序"

def test_view_product_details(authenticated_session: InventoryPage):
    """测试查看商品详情"""
    inventory_page = authenticated_session
    
    # 点击第一个商品
    inventory_page.click(".inventory_item_img")
    
    # 验证进入商品详情页
    expect(inventory_page.page).to_have_url(re.compile(r"https://www\.saucedemo\.com/inventory-item\.html\?id=\d+"))
    expect(inventory_page.page.locator(".inventory_details_name")).to_be_visible()

def test_add_product_to_cart_from_list(authenticated_session: InventoryPage, cart_page: CartPage):
    """测试从商品列表页添加商品到购物车"""
    inventory_page = authenticated_session
    
    # 添加商品到购物车
    inventory_page.add_product_to_cart(PRODUCT_NAME)
    
    # 验证购物车图标显示1个商品
    inventory_page.verify_cart_count(1)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 验证购物车中有1个商品
    cart_page.verify_cart_items_count(1)
    expect(cart_page.page.locator(".inventory_item_name")).to_have_text(PRODUCT_NAME)

def test_add_product_to_cart_from_details(authenticated_session: InventoryPage, cart_page: CartPage):
    """测试从商品详情页添加商品到购物车"""
    inventory_page = authenticated_session
    
    # 进入商品详情页
    inventory_page.click(".inventory_item_img")
    
    # 添加商品到购物车
    inventory_page.click("[data-test='add-to-cart']")
    
    # 验证购物车图标显示1个商品
    inventory_page.verify_cart_count(1)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 验证购物车中有1个商品
    cart_page.verify_cart_items_count(1)

def test_remove_product_from_cart(authenticated_session: InventoryPage, cart_page: CartPage):
    """测试从购物车移除商品"""
    inventory_page = authenticated_session
    
    # 添加商品到购物车
    inventory_page.add_product_to_cart(PRODUCT_NAME)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 验证购物车中有1个商品
    cart_page.verify_cart_items_count(1)
    
    # 移除商品
    cart_page.remove_product_from_cart(PRODUCT_NAME)
    
    # 验证购物车为空
    cart_page.verify_cart_items_count(0)
    expect(cart_page.page.locator(".shopping_cart_badge")).not_to_be_visible()

def test_checkout_with_valid_information(authenticated_session: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试使用有效信息结算下单"""
    inventory_page = authenticated_session
    
    # 添加商品到购物车
    inventory_page.add_product_to_cart(PRODUCT_NAME)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 进入结算页面
    cart_page.go_to_checkout()
    
    # 填写个人信息
    checkout_page.fill_personal_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    
    # 继续结算流程
    checkout_page.continue_to_checkout()
    
    # 验证进入订单预览页面
    expect(checkout_page.page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

def test_checkout_with_empty_information(authenticated_session: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试使用空信息结算下单失败"""
    inventory_page = authenticated_session
    
    # 添加商品到购物车
    inventory_page.add_product_to_cart(PRODUCT_NAME)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 进入结算页面
    cart_page.go_to_checkout()
    
    # 不填写信息直接点击继续
    checkout_page.continue_to_checkout()
    
    # 验证错误消息
    checkout_page.verify_error_message(EMPTY_FIRST_NAME_ERROR)

def test_checkout_with_empty_cart(authenticated_session: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试购物车为空时结算下单失败"""
    inventory_page = authenticated_session
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 验证购物车为空
    cart_page.verify_cart_items_count(0)
    
    # 点击结算按钮
    cart_page.go_to_checkout()
    
    # 验证进入结算信息页面
    expect(checkout_page.page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

def test_logout(authenticated_session: InventoryPage, login_page: LoginPage):
    """测试退出登录"""
    inventory_page = authenticated_session
    
    # 点击菜单按钮
    inventory_page.click("#react-burger-menu-btn")
    
    # 点击退出登录按钮
    inventory_page.click("#logout_sidebar_link")
    
    # 验证返回登录页面
    expect(login_page.page).to_have_url("https://www.saucedemo.com/")

def test_cancel_checkout(authenticated_session: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试取消结算"""
    inventory_page = authenticated_session
    
    # 添加商品到购物车
    inventory_page.add_product_to_cart(PRODUCT_NAME)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 进入结算页面
    cart_page.go_to_checkout()
    
    # 点击取消按钮
    checkout_page.cancel_checkout()
    
    # 验证返回购物车页面
    expect(cart_page.page).to_have_url("https://www.saucedemo.com/cart.html")

def test_cancel_order_preview(authenticated_session: InventoryPage, cart_page: CartPage, checkout_page: CheckoutPage):
    """测试取消订单预览"""
    inventory_page = authenticated_session
    
    # 添加商品到购物车
    inventory_page.add_product_to_cart(PRODUCT_NAME)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 进入结算页面
    cart_page.go_to_checkout()
    
    # 填写个人信息
    checkout_page.fill_personal_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    
    # 继续结算流程
    checkout_page.continue_to_checkout()
    
    # 验证进入订单预览页面
    expect(checkout_page.page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    
    # 点击取消按钮
    checkout_page.click("[data-test='cancel']")
    
    # 验证返回商品列表页
    expect(inventory_page.page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_add_multiple_products_to_cart(authenticated_session: InventoryPage, cart_page: CartPage):
    """测试添加多个商品到购物车"""
    inventory_page = authenticated_session
    
    # 添加多个商品到购物车
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")
    inventory_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
    
    # 验证购物车图标显示3个商品
    inventory_page.verify_cart_count(3)
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 验证购物车中有3个商品
    cart_page.verify_cart_items_count(3)

def test_remove_multiple_products_from_cart(authenticated_session: InventoryPage, cart_page: CartPage):
    """测试从购物车移除多个商品"""
    inventory_page = authenticated_session
    
    # 添加多个商品到购物车
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")
    inventory_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
    
    # 进入购物车页面
    inventory_page.go_to_cart()
    
    # 移除多个商品
    cart_page.remove_product_from_cart("Sauce Labs Backpack")
    cart_page.remove_product_from_cart("Sauce Labs Bike Light")
    
    # 验证购物车中有1个商品
    cart_page.verify_cart_items_count(1)
    expect(cart_page.page.locator(".shopping_cart_badge")).to_have_text("1")