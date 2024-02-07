import csv
import requests
from PIL import Image
from io import BytesIO

def resize_and_crop_image(original_image, target_width=750, target_height=500):
    original_width, original_height = original_image.size

    # Соотношение сторон целевого и исходного изображения
    target_ratio = target_width / target_height
    original_ratio = original_width / original_height

    # Определение необходимости обрезки по ширине или высоте
    if original_ratio > target_ratio:
        # Изображение слишком широкое, обрезаем по ширине
        new_height = target_height
        new_width = int(original_ratio * new_height)
    else:
        # Изображение слишком высокое, обрезаем по высоте
        new_width = target_width
        new_height = int(new_width / original_ratio)

    # Масштабирование изображения
    resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)

    # Вычисление области обрезки
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2

    # Обрезка до целевого размера
    cropped_image = resized_image.crop((left, top, right, bottom))
    return cropped_image

def download_and_process_image(url, filename):
    print(f"Downloading image: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            processed_image = resize_and_crop_image(image)
            processed_image.save(filename)
            print(f"Image processed and saved as {filename}")
        else:
            print(f"Failed to download image {url}: HTTP status {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_csv(csv_filename):
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Пропускаем заголовок
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

