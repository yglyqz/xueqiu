from appium_po.page.profile_page import ProfilePage
from appium_po.page.search_page import SearchPage


class XueqiuPage:
    def goto_search(self):

        return SearchPage()

    def goto_profile(self):
        return ProfilePage()

