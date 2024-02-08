import csv
import requests
from PIL import Image
from io import BytesIO
import os

# Ensure source and target directories and error.log exist
os.makedirs('source', exist_ok=True)
os.makedirs('target', exist_ok=True)
error_log_path = 'error.log'
if not os.path.exists(error_log_path):
    open(error_log_path, 'w').close()

def resize_and_crop_image(original_image, target_width=750, target_height=500):
    """Resize and crop the image to the target size."""
    original_width, original_height = original_image.size

    # Convert to RGB if in palette mode
    if original_image.mode != 'RGB':
        original_image = original_image.convert('RGB')

    target_ratio = target_width / target_height
    original_ratio = original_width / original_height

    if original_ratio > target_ratio:
        new_height = target_height
        new_width = int(original_ratio * new_height)
    else:
        new_width = target_width
        new_height = int(new_width / original_ratio)

    resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2

    cropped_image = resized_image.crop((left, top, right, bottom))
    return cropped_image

def download_and_process_image(url, filename, source_folder='source', target_folder='target'):
    """Download and process an image from a URL, then save it."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Downloading image: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            source_path = os.path.join(source_folder, filename)
            with open(source_path, 'wb') as f:
                f.write(response.content)

            image = Image.open(BytesIO(response.content))
            processed_image = resize_and_crop_image(image)
            target_path = os.path.join(target_folder, filename)
            processed_image.save(target_path)
            print(f"Image processed and saved as {target_path}")
        else:
            log_error(f"Failed to download image {url}: HTTP status {response.status_code}")
    except Exception as e:
        log_error(f"An error occurred while processing {url}: {e}")

def log_error(message):
    """Log an error message to error.log."""
    with open('error.log', 'a', encoding='utf-8') as error_file:
        error_file.write(f"{message}\n")

def process_csv(csv_filename):
    """Process a CSV file to download and process images."""
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header
        for idx, row in enumerate(csvreader, start=1):
            image_url = row[-1]
            filename = f"car_{idx}.jpg"
            print(f"\nProcessing image {idx}")
            download_and_process_image(image_url, filename)

if __name__ == "__main__":
    csv_filename = 'cars.csv'
    print("Starting to process the file:", csv_filename)
    process_csv(csv_filename)
    print("File processing completed.")
