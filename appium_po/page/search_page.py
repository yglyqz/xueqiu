from selenium.webdriver.remote.webdriver import WebDriver


class SearchPage:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def search(self, keyword):
        self.driver.find_element_by_id("search_input_text").send_keys(keyword)
        return self

    def select(self, index):
        self.driver.find_elements_by_id("name")[index].click()
        return self

    def get_price(self, stock_type):
        price = float(self.driver.find_element_by_xpath(
            "//*[contains(@resource-id, 'stockCode') and @text='" + stock_type + "']/../../.."
            "//*[contains(@resource-id, 'current_price')]").text)
        print(price)
        return price