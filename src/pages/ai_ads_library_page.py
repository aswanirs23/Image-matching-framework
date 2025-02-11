from playwright.sync_api import Page
import time

class AIAdsLibraryPage:
    def __init__(self, page: Page):
        self.page = page
         
    def get_thumbnail(self, index):
        return self.thumbnails[index]
    
    def btn_filter(self):
        return self.page.get_by_role("button", name="Ad Channels")
    
    def opt_facebook_filter(self):
        return self.page.get_by_label("Ad Channels").get_by_text("Facebook ads")
    
    def apply_facebook_filter(self):
        self.btn_filter().click()
        self.opt_facebook_filter().click()
        self.btn_filter().click()
    
    def get_thumbnail_urls(self):
        time.sleep(5) 
        return self.page.locator("//*[@class='youtube-thumbnail']").all()