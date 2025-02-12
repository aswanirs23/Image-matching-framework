import os
import time
import glob
from playwright.sync_api import expect
from src.utils.logger_util import logger
from src.pages.ai_ads_library_page import AIAdsLibraryPage
from src.pages.home_page import HomePage
from src.utils.image_utils import match_images, draw_matched_image
from src.utils.file_handles import ensure_directory_exists, delete_file, capture_screenshot
from config import URL, TEMPLATE_DIR, SCREENSHOT_PATH, MATCH_RESULT_IMAGES_DIR

def test_compare_screenshot_with_templates(page):
    logger.info("Starting test screenshot matching with templates ")
    home_page = HomePage(page)
    ai_ads_page = AIAdsLibraryPage(page)
    
    page.goto(URL)
    expect(home_page.txt_header()).to_be_visible()
    logger.info("Header 'Make ads that work.' is visible in the page")
    home_page.go_to_ai_ads_library()
    logger.info("Navigating to AI Ads Library")
    ai_ads_page.apply_facebook_filter()
    logger.info("Applying Facebook filter")
    time.sleep(5) 
    
    capture_screenshot(page, SCREENSHOT_PATH)
    logger.info("Screenshot saved at output/page_screenshot/page_screenshot.png")
    
    template_images = glob.glob(f"{TEMPLATE_DIR}/*.png") 
    logger.info(f"Found {len(template_images)} template images")
    
    delete_file(MATCH_RESULT_IMAGES_DIR)
    ensure_directory_exists(MATCH_RESULT_IMAGES_DIR)
    logger.info("Deleted and ensured directory exists at output/match_result_images/")
    for img in template_images:
            matches, kp1, kp2, is_present = match_images(img, SCREENSHOT_PATH)
            logger.info(f"Matching {img} with screenshot")

            template_name = os.path.splitext(os.path.basename(img))[0]
            match_result_img_path = os.path.join(MATCH_RESULT_IMAGES_DIR, f"matched_{template_name}.jpg")

            if is_present:
                draw_matched_image(img, SCREENSHOT_PATH, matches, kp1, kp2, match_result_img_path)
                logger.info(f"✅ Match found for {img} and comparison image saved at {match_result_img_path}")
            else:
                logger.info(f"❌ No match found for {img}")
    logger.info("Test Image matching with templates completed")