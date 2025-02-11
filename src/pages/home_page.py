from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page
    
    def txt_header(self):
        return self.page.get_by_role("heading", name="Make ads that work.")
    
    def lnk_tab(self):
        return self.page.get_by_role("navigation").get_by_role("link", name="AI Ads Library")
    
    def go_to_ai_ads_library(self):
        self.lnk_tab().click()
