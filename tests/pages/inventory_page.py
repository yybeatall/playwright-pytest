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


class InventoryPage(BasePage):
    """商品列表页面类，封装商品列表页面的所有操作和元素定位"""

    # 元素定位器
    TITLE = ".title"
    SORT_SELECT = "[data-test='product-sort-container']"
    INVENTORY_ITEMS = ".inventory_item"
    ADD_TO_CART_BUTTON = "[data-test^='add-to-cart']"
    CART_BADGE = "[data-test='shopping-cart-badge']"
    CART_LINK = "[data-test='shopping-cart-link']"

    def get_title(self) -> str:
        """获取页面标题"""
        return self.get_text_content(self.TITLE)

    def sort_products(self, sort_option: str) -> None:
        """按指定选项排序商品"""
        self.select_option(self.SORT_SELECT, sort_option)

    def get_product_count(self) -> int:
        """获取商品数量"""
        return self.get_count(self.INVENTORY_ITEMS)

    def add_to_cart(self, index: int = 0) -> None:
        """添加指定索引的商品到购物车"""
        self.click(f"{self.INVENTORY_ITEMS} >> nth={index} >> {self.ADD_TO_CART_BUTTON}")

    def get_cart_badge_count(self) -> int:
        """获取购物车徽章中的商品数量"""
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text_content(self.CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        """导航到购物车页面"""
        self.click(self.CART_LINK)

    def go_to_product_detail(self, index: int = 0) -> None:
        """导航到指定索引商品的详情页面"""
        self.click(f"{self.INVENTORY_ITEMS} >> nth={index} >> a")
