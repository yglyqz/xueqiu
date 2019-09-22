from time import sleep

import pytest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


class Test_Xueqiu:
    def setup_method(self):
        capabilities = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "appPackage": "com.xueqiu.android",
            "appActivity": ".view.WelcomeActivityAlias",
            "autoGrantPermissions": True,
            "noReset": True,
            "automationName": "UiAutomator2",
        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("user_profile_icon")

    def teardown_method(self):
        sleep(5)
        self.driver.quit()

    #alibaba xiaomi google
    @pytest.mark.parametrize(("keyword, stock_type, expect_price"),[
        ("alibaba", "BABA", 180),
        ("xiaomi", "01810", 9),
        ("google", "GOOGL", 1200)
    ])
    def test_search(self, keyword, stock_type, expect_price):
        self.driver.find_element_by_id("tv_search").click()
        self.driver.find_element_by_id("search_input_text").send_keys(keyword)
        sleep(2)
        self.driver.find_element_by_id("name").click()
        price = float(self.driver.find_element_by_xpath(
            "//*[contains(@resource-id, 'stockCode') and @text='"+stock_type+"']/../../.."
            "//*[contains(@resource-id, 'current_price')]").text)
        # print(price)
        assert price > expect_price

    def test_wrong_phone(self):
        self.driver.find_element_by_id("user_profile_icon").click()
        self.driver.find_element_by_id("iv_login_phone").click()
        self.driver.find_element_by_id("tv_login_with_account").click()
        self.driver.find_element_by_id("login_account").send_keys('123456')
        self.driver.find_element_by_id("login_password").send_keys('123456')
        self.driver.find_element_by_id("button_next").click()
        sleep(2)
        assert "手机号码填写错误" == self.driver.find_element_by_id("md_content").get_attribute("text")


    def test_wrong_password(self):
        self.driver.find_element_by_id("user_profile_icon").click()
        self.driver.find_element_by_id("iv_login_phone").click()
        self.driver.find_element_by_id("tv_login_with_account").click()
        self.driver.find_element_by_id("login_account").send_keys('15811079511')
        self.driver.find_element_by_id("login_password").send_keys('123456')
        self.driver.find_element_by_id("button_next").click()
        sleep(2)
        assert "用户名或密码错误" == self.driver.find_element_by_id("md_content").get_attribute("text")

    def test_swip(self):
        size = self.driver.get_window_size()
        # print(size)   #{'width': 1080, 'height': 1794}
        width = size["width"]
        height = size["height"]

        for i in range(5):
            self.driver.swipe(width*0.8, height*0.8, width*0.1, height*0.1)

    def test_long_click(self):
        self.driver.find_element_by_xpath("//*[@text='自选' and contains(@resource-id,'tab_name')]").click()
        t = self.driver.find_element_by_xpath("(//*[contains(@resource-id,'name_and_symbol')])[1]")
        TouchAction(self.driver).long_press(el=t).perform()
        assert "置顶" in self.driver.page_source

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