import os
import shutil

def ensure_directory_exists(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    return file_path

def delete_file(file_path):
    """Deletes a file or directory if it exists."""
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Deletes the directory and its contents
        else:
            os.remove(file_path)

def capture_screenshot(page, screenshot_path):
    """Captures a full-page screenshot."""
    delete_file(screenshot_path)
    ensure_directory_exists(screenshot_path)
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"✅ Screenshot saved at {screenshot_path}")
