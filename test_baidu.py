# -*- coding:utf8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep


_SEARCH_KEY = "Image"
_VISIT_RESULT = 3
_TEST_URL = "https://www.baidu.com"

class TestBaidu:
    def setup_class(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        # options.add_argument("--headless")
        options.add_argument('window-size=1920x1080')

        service = webdriver.ChromeService(executable_path="./chromedriver")
        self.driver = webdriver.Chrome(options=options, service=service)

        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(_TEST_URL)

    def teardown_class(self):
        self.driver.quit()

    def test_search(self):
        # 找到输入框，输入Image
        self.driver.find_element(By.ID, "kw").send_keys(_SEARCH_KEY)
        # 找到<百度一下>按钮，点击
        self.driver.find_element(By.ID, "su").click()
        # 找到第三个结果，点击
        self.driver.find_element(By.XPATH, f'//div[@id="{_VISIT_RESULT}"]//span').click()
        # 切换到最新打开的窗口
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # 强制等待2秒，等UI绘制完成
        sleep(2)
        # 将最新打开的页面进行截图
        self.driver.save_screenshot("./search.png")
        # 将搜索内容与新页面的title进行匹配，这里将搜索内容小写处理
        assert _SEARCH_KEY.lower() in self.driver.title

if __name__ == '__main__':
    pytest.main()