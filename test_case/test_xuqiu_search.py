from time import sleep

import pytest
from appium import webdriver
from hamcrest import *


class Test_Xueqiu:
    @classmethod
    def setup_class(cls):
        capabilities = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "appPackage": "com.xueqiu.android",
            "appActivity": ".view.WelcomeActivityAlias",
            "autoGrantPermissions": True,
            "noReset": True,
            "automationName": "UiAutomator2",
        }

        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", capabilities)
        cls.driver.implicitly_wait(10)
        cls.driver.find_element_by_id("user_profile_icon")

    @classmethod
    def teardown_class(cls):
        sleep(5)
        cls.driver.quit()

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




