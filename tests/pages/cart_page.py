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


class CartPage(BasePage):
    """购物车页面类，封装购物车页面的所有操作和元素定位"""

    # 元素定位器
    CART_ITEMS = ".cart_item"
    REMOVE_BUTTON = "[data-test^='remove']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"

    def get_cart_item_count(self) -> int:
        """获取购物车中商品数量"""
        return self.get_count(self.CART_ITEMS)

    def remove_item(self, index: int = 0) -> None:
        """移除购物车中指定索引的商品"""
        self.click(f"{self.CART_ITEMS} >> nth={index} >> {self.REMOVE_BUTTON}")

    def checkout(self) -> None:
        """点击结算按钮"""
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """点击继续购物按钮"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
