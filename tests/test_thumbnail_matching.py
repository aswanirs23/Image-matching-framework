import glob
import allure

from playwright.sync_api import expect
from src.utils.logger_util import logger
from src.pages.ai_ads_library_page import AIAdsLibraryPage
from src.pages.home_page import HomePage
from src.utils.image_utils import process_thumbnails
from config import URL, TEMPLATE_DIR, IMAGE_DIR

@allure.feature("Thumbnail Comparison with Templates")
@allure.story("Compare Thumbnails with Stored Templates")
def test_compare_thumbnails_with_templates(page):
    logger.info("Starting test thumbnail matching with templates ")
    ai_ads_page = AIAdsLibraryPage(page)
    home_page = HomePage(page)
    
    page.goto(URL)
    expect(home_page.txt_header()).to_be_visible()
    logger.info("Header 'Make ads that work.' is visible in the page")
    home_page.go_to_ai_ads_library()
    logger.info("Navigating to AI Ads Library")
    ai_ads_page.apply_facebook_filter()
    logger.info("Applying Facebook filter")
    
    thumbnails = ai_ads_page.get_thumbnail_urls()
    logger.info(f"Found {len(thumbnails)} thumbnails")
    
    template_paths = glob.glob(f"{TEMPLATE_DIR}/*.png")
    logger.info(f"Found {len(template_paths)} template images")
    
    process_thumbnails(thumbnails, template_paths, IMAGE_DIR)
    
    with allure.step("Test completion"):
        logger.info("✅ Thumbnail comparison test completed.")