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

from playwright.sync_api import Page


class BasePage:
    """基础页面类，封装通用的页面操作"""

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str) -> None:
        """导航到指定 URL"""
        self.page.goto(url)

    def click(self, locator: str) -> None:
        """点击指定元素"""
        self.page.click(locator)

    def fill(self, locator: str, value: str) -> None:
        """在指定输入框中填写内容"""
        self.page.fill(locator, value)

    def select_option(self, locator: str, value: str) -> None:
        """选择下拉菜单选项"""
        self.page.select_option(locator, value)

    def get_text_content(self, locator: str) -> str:
        """获取指定元素的文本内容"""
        return self.page.locator(locator).text_content()

    def get_count(self, locator: str) -> int:
        """获取符合定位器的元素数量"""
        return self.page.locator(locator).count()

    def is_visible(self, locator: str) -> bool:
        """检查元素是否可见"""
        return self.page.locator(locator).is_visible()

    def is_hidden(self, locator: str) -> bool:
        """检查元素是否隐藏"""
        return self.page.locator(locator).is_hidden()
