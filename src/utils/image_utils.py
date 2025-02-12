import cv2
import numpy as np
import os
import requests
from sklearn.cluster import DBSCAN
from src.utils.logger_util import logger

def load_image(image_path):
    """Loads an image from the given path and converts it to grayscale."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Error loading image: {image_path}")
    return image


def match_images(template, screenshot, match_threshold=20, eps_factor=0.05, min_samples=3, cluster_ratio=0.5):
    """Matches two images using SIFT and Flann based matcher."""
    template = load_image(template)
    screenshot = load_image(screenshot)
    sift = cv2.SIFT_create()
    template_kp, template_des = sift.detectAndCompute(template, None)
    screenshot_kp, screenshot_des = sift.detectAndCompute(screenshot, None)

    if template_des is None or screenshot_des is None:
        return [], template_kp, screenshot_kp, False

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(template_des, screenshot_des, k=2)

    ratio_threshold = 0.75
    good_matches = [m for m, n in matches if m.distance < ratio_threshold * n.distance]
    is_present = len(good_matches) >= match_threshold

    if is_present:
        matched_points = np.array([screenshot_kp[m.trainIdx].pt for m in good_matches])
        eps = eps_factor * max(screenshot.shape)
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(matched_points)

        unique_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
        labels, counts = np.unique(clustering.labels_, return_counts=True)
        largest_cluster_count = max(counts[labels != -1], default=0)

        if unique_clusters > 1 and (largest_cluster_count / len(good_matches)) < cluster_ratio:
            is_present = False

    return good_matches, template_kp, screenshot_kp, is_present


def compare_images(image1_path, image2_path):
    """Compares two images using pixel-based difference calculation."""
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    if img1 is None or img2 is None:
        return False

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    return np.count_nonzero(thresh) == 0


def download_image(image_url, save_path):
    """Downloads an image from the given URL and saves it to the specified path."""
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    return False


def process_thumbnails(thumbnails, template_paths, image_dir):
    """Processes thumbnails and compares them with templates."""
    os.makedirs(image_dir, exist_ok=True)

    for template_path in template_paths:
        for index, thumbnail in enumerate(thumbnails):
            image_url = thumbnail.get_attribute("src")

            image_path = os.path.join(image_dir, f"thumbnail_{index}.jpg")
            download_image(image_url, image_path)
            
            if compare_images(image_path, template_path):
                logger.info(f"✅ Match Found: {template_path} matches {image_path}")
                break
        else:
            logger.info(f"❌ No match found for template {template_path}")

    logger.info("Finished processing all templates")


def draw_matched_image(template_path, screenshot_path, matches, kp1, kp2, output_path):
    """Draws and saves matched keypoints between two images."""
    template_img = cv2.imread(template_path)
    screenshot_img = cv2.imread(screenshot_path)

    if template_img is None or screenshot_img is None:
        logger.info(f"❌ Error loading images: {template_path} or {screenshot_path}")
        return

    match_result_img = cv2.drawMatches(template_img, kp1, screenshot_img, kp2, matches[:50], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite(output_path, match_result_img)
