from playwright.sync_api import Page, expect
import re


class BasePage:
    """基础页面对象，封装所有页面共有的方法"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        """导航到指定URL"""
        self.page.goto(url)
    
    def get_url(self):
        """获取当前页面URL"""
        return self.page.url
    
    def wait_for_selector(self, selector: str, timeout: int = 5000):
        """等待元素可见"""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def expect_url(self, url_pattern: str, timeout: int = 5000):
        """验证当前URL匹配指定模式"""
        if url_pattern.startswith("regex:"):
            pattern = re.compile(url_pattern[6:])
            expect(self.page).to_have_url(pattern, timeout=timeout)
        else:
            expect(self.page).to_have_url(url_pattern, timeout=timeout)
    
    def expect_element_visible(self, selector: str, timeout: int = 5000):
        """验证元素可见"""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)
    
    def expect_element_contain_text(self, selector: str, text: str, timeout: int = 5000):
        """验证元素包含指定文本"""
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)
    
    def expect_element_count(self, selector: str, count: int, timeout: int = 5000):
        """验证元素数量"""
        expect(self.page.locator(selector)).to_have_count(count, timeout=timeout)