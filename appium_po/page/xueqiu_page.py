from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from appium_po.page.profile_page import ProfilePage
from appium_po.page.search_page import SearchPage


class XueqiuPage:
    def __init__(self):
        capabilities = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "appPackage": "com.xueqiu.android",
            "appActivity": ".view.WelcomeActivityAlias",
            "autoGrantPermissions": True,
            "noReset": True,
            "automationName": "UiAutomator2",
        }

        from appium import webdriver
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", capabilities)
        self.driver.implicitly_wait(10)
        # self.driver.find_element_by_id("image_cancel").click()
        #等待某个元素出现
        WebDriverWait(self.driver, 60).until(
            expected_conditions.invisibility_of_element_located((By.ID, "image_cancel"))
        )

        def click_cancel():
            size = len(self.driver.find_element_by_id("image_cancel").is_displayed())
            if size >= 1:
                self.driver.find_element_by_id("image_cancel").click()
            return size >= 1
        #等待20s 每次1秒进行循环
        WebDriverWait(self.driver, 20, 1).until(click_cancel)

        self.driver.find_element_by_id("user_profile_icon")

    def goto_search(self):
        self.driver.find_element_by_id("tv_search").click()
        return SearchPage(self.driver)

    def goto_profile(self):
        return ProfilePage()

