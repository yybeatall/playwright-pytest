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


class CheckoutPage(BasePage):
    """结算页面类，封装结算页面的所有操作和元素定位"""

    # 元素定位器（第一步：填写配送信息）
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"

    # 元素定位器（第二步：查看订单摘要）
    FINISH_BUTTON = "[data-test='finish']"

    # 元素定位器（第三步：订单完成）
    COMPLETE_HEADER = "[data-test='complete-header']"
    COMPLETE_TEXT = "[data-test='complete-text']"

    def fill_shipping_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """填写配送信息"""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_shipping(self) -> None:
        """继续到配送信息填写"""
        self.click(self.CONTINUE_BUTTON)

    def finish_checkout(self) -> None:
        """完成订单"""
        self.click(self.FINISH_BUTTON)

    def get_error_message(self) -> str:
        """获取错误信息"""
        return self.get_text_content(self.ERROR_MESSAGE)

    def get_complete_header(self) -> str:
        """获取订单完成页面的标题"""
        return self.get_text_content(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """获取订单完成页面的文本"""
        return self.get_text_content(self.COMPLETE_TEXT)
