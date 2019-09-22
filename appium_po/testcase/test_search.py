from appium_po.page.xueqiu_page import XueqiuPage


class TestSearch:

    def test_search_alibaba(self):
        xueqiu = XueqiuPage()
        assert 100 == xueqiu.goto_search().search("alibaba").select(0).get_price()