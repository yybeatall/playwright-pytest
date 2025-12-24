# 测试数据配置

# 登录测试数据
LOGIN_DATA = {
    "valid_user": {
        "username": "standard_user",
        "password": "secret_sauce"
    },
    "invalid_user": {
        "username": "invalid_user",
        "password": "invalid_password"
    },
    "locked_out_user": {
        "username": "locked_out_user",
        "password": "secret_sauce"
    },
    "problem_user": {
        "username": "problem_user",
        "password": "secret_sauce"
    },
    "performance_glitch_user": {
        "username": "performance_glitch_user",
        "password": "secret_sauce"
    }
}

# 商品测试数据
PRODUCTS = {
    "backpack": "Sauce Labs Backpack",
    "bike_light": "Sauce Labs Bike Light",
    "bolt_t_shirt": "Sauce Labs Bolt T-Shirt",
    "fleece_jacket": "Sauce Labs Fleece Jacket",
    "onesie": "Sauce Labs Onesie",
    "red_t_shirt": "Test.allTheThings() T-Shirt (Red)"
}

# 排序选项
SORT_OPTIONS = {
    "az": "Name (A to Z)",
    "za": "Name (Z to A)",
    "lohi": "Price (low to high)",
    "hilo": "Price (high to low)"
}

# 结算测试数据
CHECKOUT_DATA = {
    "valid_info": {
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "12345"
    },
    "empty_info": {
        "first_name": "",
        "last_name": "",
        "postal_code": ""
    },
    "partial_info": {
        "first_name": "John",
        "last_name": "",
        "postal_code": ""
    }
}

# 错误消息
ERROR_MESSAGES = {
    "invalid_credentials": "Epic sadface: Username and password do not match any user in this service",
    "username_required": "Epic sadface: Username is required",
    "password_required": "Epic sadface: Password is required",
    "first_name_required": "Error: First Name is required",
    "last_name_required": "Error: Last Name is required",
    "postal_code_required": "Error: Postal Code is required"
}

# 成功消息
SUCCESS_MESSAGES = {
    "order_complete": "Thank you for your order!"
}