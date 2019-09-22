from time import sleep

from appium import webdriver

class BaseDriver:
    def android_driver(self):
        capabilities = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "appPackage": "com.xueqiu.android",
            "appActivity": ".view.WelcomeActivityAlias",
            "autoGrantPermissions": True,
        }

        driver = webdriver.Remote("http://localhost:4723/wd/hub", capabilities)

        return driver


if __name__ == '__main__':
    t = BaseDriver()
    t.android_driver()
    sleep(10)