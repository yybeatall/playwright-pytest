# 基于 pytest-playwright 的 saucedemo.com UI 自动化测试脚本
import pytest
from playwright.sync_api import Page


class TestSauceDemo:
    """测试 saucedemo.com 网站的完整购物流程"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置条件：访问 saucedemo.com 网站"""
        self.page = page
        self.page.goto("https://www.saucedemo.com/")

    # 1. 访问与登录功能测试
    def test_login_success(self):
        """测试成功登录场景"""
        # 输入用户名和密码
        self.page.fill("#user-name", "standard_user")
        self.page.fill("#password", "secret_sauce")
        # 点击登录按钮
        self.page.click("#login-button")
        # 验证登录成功：页面跳转至商品列表页
        assert self.page.url == "https://www.saucedemo.com/inventory.html"
        assert self.page.locator(".title").text_content() == "Products"

    def test_login_failure_with_wrong_password(self):
        """测试使用错误密码登录的失败场景"""
        # 输入正确用户名和错误密码
        self.page.fill("#user-name", "standard_user")
        self.page.fill("#password", "wrong_password")
        # 点击登录按钮
        self.page.click("#login-button")
        # 验证登录失败：显示错误信息
        error_message = self.page.locator(".error-message-container.error")
        assert error_message.is_visible()
        assert "Epic sadface: Username and password do not match any user in this service" in error_message.text_content()

    def test_login_failure_with_empty_username(self):
        """测试空用户名登录的失败场景"""
        # 输入空用户名和正确密码
        self.page.fill("#user-name", "")
        self.page.fill("#password", "secret_sauce")
        # 点击登录按钮
        self.page.click("#login-button")
        # 验证登录失败：显示错误信息
        error_message = self.page.locator(".error-message-container.error")
        assert error_message.is_visible()
        assert "Epic sadface: Username is required" in error_message.text_content()

    # 2. 浏览与筛选商品功能测试
    def test_browse_products(self):
        """测试浏览商品列表"""
        # 先登录
        self.test_login_success()
        # 验证商品列表中有商品
        products = self.page.locator(".inventory_item")
        assert products.count() > 0

    def test_sort_products_by_name_az(self):
        """测试按商品名称从 A 到 Z 排序"""
        # 先登录
        self.test_login_success()
        # 选择按名称 A 到 Z 排序
        self.page.select_option("[data-test='product-sort-container']", "az")
        # 等待排序完成
        self.page.wait_for_selector(".inventory_item")
        # 获取排序后的商品名称
        product_names = [item.text_content() for item in self.page.locator(".inventory_item_name").all()]
        # 验证商品按名称升序排列
        assert product_names == sorted(product_names)

    def test_sort_products_by_price_low_to_high(self):
        """测试按商品价格从低到高排序"""
        # 先登录
        self.test_login_success()
        # 选择按价格从低到高排序
        self.page.select_option("[data-test='product-sort-container']", "lohi")
        # 等待排序完成
        self.page.wait_for_selector(".inventory_item")
        # 获取排序后的商品价格
        product_prices = [
            float(item.text_content().replace("$", "")) 
            for item in self.page.locator(".inventory_item_price").all()
        ]
        # 验证商品按价格升序排列
        assert product_prices == sorted(product_prices)

    # 3. 查看商品详情功能测试
    def test_view_product_details(self):
        """测试查看商品详情"""
        # 先登录
        self.test_login_success()
        # 获取第一个商品的名称
        first_product_name = self.page.locator(".inventory_item_name").first.text_content()
        # 点击第一个商品
        self.page.locator(".inventory_item_name").first.click()
        # 等待页面加载完成
        self.page.wait_for_selector(".inventory_details_name")
        # 验证商品名称一致
        assert self.page.locator(".inventory_details_name.large_size").text_content() == first_product_name

    # 4. 添加商品功能测试
    def test_add_product_from_list_page(self):
        """测试从商品列表页添加商品到购物车"""
        # 先登录
        self.test_login_success()
        # 点击第一个商品的 "Add to cart" 按钮
        self.page.locator(".btn_inventory").first.click()
        # 验证购物车图标显示商品数量为 1
        assert self.page.locator(".shopping_cart_badge").text_content() == "1"

    def test_add_product_from_details_page(self):
        """测试从商品详情页添加商品到购物车"""
        # 先登录并进入商品详情页
        self.test_login_success()
        self.page.locator(".inventory_item_name").first.click()
        # 等待页面加载完成
        self.page.wait_for_selector(".inventory_details_name")
        # 点击 "Add to cart" 按钮
        self.page.locator(".btn_inventory").click()
        # 验证购物车图标显示商品数量为 1
        assert self.page.locator(".shopping_cart_badge").text_content() == "1"

    # 5. 查看与编辑购物车功能测试
    def test_view_cart(self):
        """测试查看购物车"""
        # 先登录并添加商品
        self.test_login_success()
        self.page.locator(".btn_inventory").first.click()
        # 点击购物车图标
        self.page.click(".shopping_cart_link")
        # 验证页面跳转至购物车页
        assert self.page.url == "https://www.saucedemo.com/cart.html"
        # 验证购物车中有一个商品
        assert self.page.locator(".cart_item").count() == 1

    def test_remove_product_from_cart(self):
        """测试从购物车移除商品"""
        # 先登录、添加商品并进入购物车
        self.test_login_success()
        self.page.locator(".btn_inventory").first.click()
        self.page.click(".shopping_cart_link")
        # 点击 "Remove" 按钮
        self.page.click(".cart_button")
        # 验证购物车中没有商品
        assert self.page.locator(".cart_item").count() == 0
        # 验证购物车图标不再显示商品数量
        assert not self.page.locator(".shopping_cart_badge").is_visible()

    # 6. 结算下单功能测试
    def test_checkout_flow(self):
        """测试完整的结算下单流程"""
        # 先登录并添加商品
        self.test_login_success()
        self.page.locator(".btn_inventory").first.click()
        self.page.click(".shopping_cart_link")
        # 点击 "Checkout" 按钮
        self.page.click("#checkout")
        # 填写个人信息
        self.page.fill("#first-name", "John")
        self.page.fill("#last-name", "Doe")
        self.page.fill("#postal-code", "12345")
        # 点击 "Continue" 按钮
        self.page.click("#continue")
        # 验证进入订单预览页
        assert self.page.url == "https://www.saucedemo.com/checkout-step-two.html"
        # 点击 "Finish" 按钮完成订单
        self.page.click("#finish")
        # 验证订单完成
        assert self.page.url == "https://www.saucedemo.com/checkout-complete.html"
        assert self.page.locator(".complete-header").text_content() == "Thank you for your order!"

    def test_checkout_failure_with_empty_information(self):
        """测试空信息结算的失败场景"""
        # 先登录并添加商品
        self.test_login_success()
        self.page.locator(".btn_inventory").first.click()
        self.page.click(".shopping_cart_link")
        # 点击 "Checkout" 按钮
        self.page.click("#checkout")
        # 不填写任何信息，直接点击 "Continue" 按钮
        self.page.click("#continue")
        # 验证结算失败：显示错误信息
        error_message = self.page.locator(".error-message-container.error")
        assert error_message.is_visible()
        assert "First Name is required" in error_message.text_content()
