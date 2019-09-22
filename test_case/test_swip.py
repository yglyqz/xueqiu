from time import sleep

from base.base_driver import BaseDriver

class Test_Xueqiu:
    def setup_class(self):
        base_driver = BaseDriver()
        self.driver = base_driver.android_driver()
        self.driver.implicitly_wait(15)

    def teardown_class(self):
        sleep(10)
        self.driver.quit()

    def test_swipe_percent(self):
        sleep(5)
        size = self.driver.get_window_size()
        width = size["width"]
        height = size['height']

        for i in range(5):
            self.driver.swipe(width*0.8, height*0.8, width*0.2, height*0.2, 1000)

