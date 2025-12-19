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

from tests.pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """商品详情页面类，封装商品详情页面的所有操作和元素定位"""

    # 元素定位器
    PRODUCT_NAME = ".inventory_details_name"
    PRODUCT_PRICE = ".inventory_details_price"
    ADD_TO_CART_BUTTON = "[data-test^='add-to-cart']"
    BACK_BUTTON = "[data-test='back-to-products']"
    CART_LINK = "[data-test='shopping-cart-link']"

    def get_product_name(self) -> str:
        """获取商品名称"""
        return self.get_text_content(self.PRODUCT_NAME)

    def get_product_price(self) -> str:
        """获取商品价格"""
        return self.get_text_content(self.PRODUCT_PRICE)

    def add_to_cart(self) -> None:
        """添加当前商品到购物车"""
        self.click(self.ADD_TO_CART_BUTTON)

    def go_back_to_inventory(self) -> None:
        """返回商品列表页面"""
        self.click(self.BACK_BUTTON)

    def go_to_cart(self) -> None:
        """导航到购物车页面"""
        self.click(self.CART_LINK)
