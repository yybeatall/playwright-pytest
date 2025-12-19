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

"""测试数据集中管理"""

# 测试网站 URL
BASE_URL = "https://www.saucedemo.com/"

# 常量配置
TIMEOUTS = {
    "page_load": 30000,
    "element_wait": 10000
}

# 用户凭证
VALID_USER = {
    "username": "standard_user",
    "password": "secret_sauce"
}

LOCKED_USER = {
    "username": "locked_out_user",
    "password": "secret_sauce"
}

INVALID_USER = {
    "username": "invalid_user",
    "password": "invalid_password"
}

EMPTY_USER = {
    "username": "",
    "password": ""
}

# 配送信息
SHIPPING_INFO = {
    "first_name": "John",
    "last_name": "Doe",
    "postal_code": "12345"
}

# 商品排序选项
SORT_OPTIONS = {
    "az": "az",
    "za": "za",
    "lohi": "lohi",
    "hilo": "hilo"
}

# 错误信息
ERROR_MESSAGES = {
    "invalid_credentials": "Epic sadface: Username and password do not match any user in this service",
    "empty_username": "Epic sadface: Username is required",
    "empty_password": "Epic sadface: Password is required",
    "first_name_required": "Error: First Name is required",
    "locked_user": "Epic sadface: Sorry, this user has been locked out."
}
