from time import sleep

import pytest
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from hamcrest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Test_Xueqiu:
    def setup_class(self):
        #chromedriver使用path更可靠
        capabilities = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "appPackage": "com.xueqiu.android",
            "appActivity": ".view.WelcomeActivityAlias",
            "autoGrantPermissions": True,
            "noReset": True,
            "automationName": "UiAutomator2",
            "chromedriverExecutable": "/Users/liyang/liyang/chrome_driver/chrome_20",
        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        # cls.driver.find_element_by_id("image_cancel").click()

        def click_cancel():
            size = len(self.driver.find_element_by_id("image_cancel").is_displayed())
            if size >= 1:
                self.driver.find_element_by_id("image_cancel").click()
            else:
                print("no displayed")
        #等待20s 每次1秒进行循环
        # WebDriverWait(self.driver, 20, 1).until(click_cancel)

        self.driver.find_element_by_id("user_profile_icon")

    def teardown_class(self):
        sleep(5)
        self.driver.quit()

    # def setup(self):
    #     pass
    #
    # def teardown(self):
    #     self.driver.find_element_by_id("action_close").click()

    #代替setup与teardown
    @pytest.fixture()
    def search_fixture(self):
        # pass
        yield
        self.driver.find_element_by_id("action_close").click()

    #alibaba xiaomi google
    @pytest.mark.parametrize(("keyword, stock_type, expect_price"),[
        ("alibaba", "BABA", 180),
        ("xiaomi", "01810", 9),
        ("google", "GOOGL", 1200)
    ])
    def test_search(self, search_fixture, keyword, stock_type, expect_price):
        self.driver.find_element_by_id("tv_search").click()
        self.driver.find_element_by_id("search_input_text").send_keys(keyword)
        sleep(2)
        self.driver.find_element_by_id("name").click()
        price = float(self.driver.find_element_by_xpath(
            "//*[contains(@resource-id, 'stockCode') and @text='"+stock_type+"']/../../.."
            "//*[contains(@resource-id, 'current_price')]").text)
        # print(price)
        assert price > expect_price

    def test_webview(self):
        self.driver.find_element_by_xpath("//*[@text='交易' and"
                                          " contains(@resource-id, 'tab_name')]").click()
        self.driver.find_element_by_id("page_type_fund").click()

        WebDriverWait(self.driver, 20, 1).until(lambda x:
                                                'WEBVIEW_com.xueqiu.android'
                                                in self.driver.contexts)
        #等到'WEBVIEW_com.xueqiu.android'  出现时执行 webview的click
        #by_accessibility_id----->对应的字段是content-desc  报错
        self.driver.find_element(MobileBy.ACCESSIBILITY_ID, '蛋卷基金安全开户').click()
        # self.driver.find_element(MobileBy.XPATH, "//*[contains(@text,'蛋卷基金安全开户')]").click()

        self.driver.switch_to.context('WEBVIEW_com.xueqiu.android')

        WebDriverWait(self.driver, 20, 1).until(lambda x:
                                                '手机号'
                                                in self.driver.page_source)

        self.driver.find_element(By.NAME,"tel").send_keys('15711079511')
        self.driver.find_element(By.NAME, "captcha").send_keys('1234')
        self.driver.find_element(By.CSS_SELECTOR, '.dj-button').click()

        assert '好的，知道了' in self.driver.page_source









