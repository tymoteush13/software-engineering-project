import mss
import time
from datetime import datetime
import pygetwindow as gw
from PIL import Image, ImageChops
import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_similarity_ssim(image1, image2):
    """Calculate the Structural Similarity Index (SSIM) between two images."""
    image1_gray = image1.convert("L")
    image2_gray = image2.convert("L")
    
    image1_np = np.array(image1_gray)
    image2_np = np.array(image2_gray)
    
    similarity, _ = ssim(image1_np, image2_np, full=True)
    return similarity

def calculate_similarity_pixels(image1, image2):
    """Calculate the percentage of different pixels between two images."""
    diff = ImageChops.difference(image1, image2)
    diff_np = np.array(diff)
    total_pixels = diff_np.size
    different_pixels = np.count_nonzero(diff_np)
    similarity = 1 - (different_pixels / total_pixels)
    return similarity

def get_monitor_area(app_name):
    """Find the monitor area for an application window by name."""
    windows = gw.getWindowsWithTitle(app_name)
    for window in windows:
        if app_name.lower() in window.title.lower():
            # Restore the window if it's minimized
            if window.isMinimized:
                window.restore()
                time.sleep(0.5)  # Give some time for the window to restore

            # Activate the window
            window.activate()
            time.sleep(0.5)  # Give some time for the window to activate

            # Get the position and size of the window
            left = window.left
            top = window.top
            width = window.width
            height = window.height
            return {"top": top, "left": left, "width": width, "height": height}

    print(f"Application with name containing '{app_name}' not found.")
    return None

def take_screenshot(monitor_area):
    """Capture a screenshot of the specified monitor area."""
    with mss.mss() as sct:
        sct_img = sct.grab(monitor_area)
        # Convert raw screenshot to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        return img

def main():
    # Find the monitor area for the application "Teams"
    app_name = "Teams"
    monitor_area = get_monitor_area(app_name)

    if monitor_area is None:
        print("Unable to find the application window. Exiting.")
        return

    # Initialize the previous screenshot as None
    previous_image = None

    while True:
        # Take a new screenshot
        current_image = take_screenshot(monitor_area)

        # Compare with the previous image if it exists
        if previous_image is not None:
            # Calculate similarity using SSIM
            similarity = calculate_similarity_ssim(previous_image, current_image)
            print(f"SSIM Similarity: {similarity:.2f}")

            # Skip saving if similarity is above 90%
            if similarity > 0.9:
                print("Screenshots are similar. Skipping save.")
                time.sleep(5)
                continue

        # Save the current screenshot
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"screenshot_{current_time}.png"
        current_image.save(file_name)
        print(f"Screenshot saved as {file_name}")

        # Update the previous image
        previous_image = current_image

        # Wait before the next iteration
        time.sleep(5)

if __name__ == "__main__":
    main()
