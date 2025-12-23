from playwright.sync_api import Page

class BasePage:
    """基础页面对象类，封装通用操作"""
    
    def __init__(self, page: Page):
        self.page = page
        
    def navigate(self, url: str):
        """导航到指定URL"""
        self.page.goto(url)
        
    def click(self, selector: str):
        """点击指定元素"""
        self.page.click(selector)
        
    def fill(self, selector: str, value: str):
        """填写输入框"""
        self.page.fill(selector, value)
        
    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        return self.page.locator(selector).text_content()
        
    def wait_for_url(self, url: str):
        """等待URL匹配"""
        self.page.wait_for_url(url)
        
    def wait_for_selector(self, selector: str):
        """等待元素出现"""
        self.page.wait_for_selector(selector)
        
    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        return self.page.locator(selector).is_visible()
        
    def get_count(self, selector: str) -> int:
        """获取元素数量"""
        return self.page.locator(selector).count()