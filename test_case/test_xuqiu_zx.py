from time import sleep

import pytest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


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
    def teardown_cls(cls):
        sleep(5)
        cls.driver.quit()

    @pytest.fixture()
    def search_fixture(self):
        # pass
        yield
        self.driver.find_element_by_id("action_close").click()

    def test_add_zx(self):
        self.driver.find_element_by_xpath("//*[@text='自选' and contains(@resource-id,'tab_name')]").click()
        self.driver.find_element_by_id("action_search").click()
        self.driver.find_element_by_id("search_input_text").send_keys("alibaba")
        self.driver.find_element_by_id("name").click()
        self.driver.find_element_by_xpath(
            "//*[contains(@resource-id, 'stockCode') and @text='BABA']/../../.."
            "//*[contains(@resource-id, 'follow_btn')]").click()
        self.driver.find_element_by_id("action_close").click()
        sleep(2)
        assert "阿里巴巴" in self.driver.page_source

    def test_del_zx(self):
        t = self.driver.find_element_by_xpath("//*[contains(@text,'BABA')]")
        TouchAction(self.driver).long_press(el=t).perform()
        self.driver.find_element_by_xpath("//*[contains(@resource-id,'md_title') and @text='删除']").click()
        sleep(1)
        self.driver.find_element_by_id("action_search").click()
        self.driver.find_element_by_id("search_input_text").send_keys("alibaba")
        self.driver.find_element_by_id("name").click()
        status = self.driver.find_element_by_xpath(
            "//*[contains(@resource-id, 'stockCode') and @text='BABA']/../../.."
            "//*[contains(@resource-id, 'follow_btn')]").get_attribute("text")
        assert "加自选" == status