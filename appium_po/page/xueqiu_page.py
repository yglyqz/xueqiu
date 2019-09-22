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
        # cls.driver.find_element_by_id("image_cancel").click()
        self.driver.find_element_by_id("user_profile_icon")

    def goto_search(self):
        self.driver.find_element_by_id("tv_search").click()
        return SearchPage(self.driver)

    def goto_profile(self):
        return ProfilePage()

