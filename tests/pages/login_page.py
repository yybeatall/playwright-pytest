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


class LoginPage(BasePage):
    """登录页面类，封装登录页面的所有操作和元素定位"""

    # 元素定位器
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def login(self, username: str, password: str) -> None:
        """执行登录操作"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """获取错误信息文本"""
        return self.get_text_content(self.ERROR_MESSAGE)

    def is_error_message_visible(self) -> bool:
        """检查错误信息是否可见"""
        return self.is_visible(self.ERROR_MESSAGE)
