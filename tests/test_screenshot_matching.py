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
    ai_ads_page = AIAdsLibraryPage(page)
    home_page = HomePage(page)
    
    page.goto(URL)
    expect(home_page.txt_header()).to_be_visible()
    home_page.go_to_ai_ads_library()
    ai_ads_page.apply_facebook_filter()
    
    time.sleep(5) 
    
    capture_screenshot(page, SCREENSHOT_PATH)
    
    template_images = glob.glob(f"{TEMPLATE_DIR}/*.png") 
    
    delete_file(MATCH_RESULT_IMAGES_DIR)
    ensure_directory_exists(MATCH_RESULT_IMAGES_DIR)

    for img in template_images:
            matches, kp1, kp2, is_present = match_images(img, SCREENSHOT_PATH)

            template_name = os.path.splitext(os.path.basename(img))[0]
            match_result_img_path = os.path.join(MATCH_RESULT_IMAGES_DIR, f"matched_{template_name}.jpg")

            if is_present:
                draw_matched_image(img, SCREENSHOT_PATH, matches, kp1, kp2, match_result_img_path)
                print(f"✅ Match found for {img} and comparison image saved at {match_result_img_path}")
            else:
                print(f"❌ No match found for {img}")