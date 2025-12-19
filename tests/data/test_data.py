# 测试数据集中管理

class TestData:
    """测试数据类"""

    # 常量配置
    TIMEOUT = 30000  # 超时时间（毫秒）

    # 登录测试数据
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    INVALID_PASSWORD = "wrong_password"
    EMPTY_USERNAME = ""
    LOCKED_USERNAME = "locked_out_user"

    # 登录错误信息
    INVALID_CREDENTIALS_ERROR = "Username and password do not match any user in this service"
    EMPTY_USERNAME_ERROR = "Username is required"
    EMPTY_FIRST_NAME_ERROR = "First Name is required"
    LOCKED_USER_ERROR = "Epic sadface: Sorry, this user has been locked out."

    # 商品排序选项
    SORT_NAME_AZ = "az"
    SORT_NAME_ZA = "za"
    SORT_PRICE_LOW_TO_HIGH = "lohi"
    SORT_PRICE_HIGH_TO_LOW = "hilo"

    # 收货信息
    FIRST_NAME = "John"
    LAST_NAME = "Doe"
    POSTAL_CODE = "12345"
