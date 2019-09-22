from appium_po.page.xueqiu_page import XueqiuPage


class TestSearch:

    def setup(self):
        self.xueqiu = XueqiuPage()

    def test_search_alibaba(self):
        assert 180 < self.xueqiu.goto_search().search("alibaba").select(0).get_price("BABA")

