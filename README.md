# Image Processor

## Overview
This Python script automates the downloading and processing of images listed in a CSV file. It is designed to fetch images from specified URLs, resize and crop them to a standardized format, and save them in designated directories for original and processed images.

## Features
- **Automatic Image Downloading**: Downloads images from URLs specified in a CSV file.
- **Image Resizing and Cropping**: Adjusts image dimensions to fit a standard size while maintaining the aspect ratio.
- **Error Logging**: Captures and logs any errors during the download or processing phases, ensuring the process continues uninterrupted.

## Requirements
- Python 3.x
- Libraries: `PIL`, `requests`, `csv`, `os`

To install the required Python libraries, run:
```bash
pip install Pillow requests
```
## Project Structure
project/
│
├── source/                    # Directory for storing original images
├── target/                    # Directory for storing processed images
├── error.log                  # Error log file
├── cars.csv                   # CSV file containing image URLs
├── image_processor.py         # Main script for downloading and processing images
└── README.md                  # Documentation file

## Usage
Ensure that cars.csv is in the project directory and contains URLs of images to be processed. The CSV format should include headers with at least one column for URLs.
Navigate to the project directory in the command line.
Execute the script with:
```bash
python3 download_resize_images.py
```