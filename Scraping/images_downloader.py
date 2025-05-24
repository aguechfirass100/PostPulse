import os
import json
import requests
import logging
from urllib.parse import urlparse

# sector_folders = ["Automotive_Transport", "Manufacturing_Industry"]
sector_folders = ["Manufacturing_Industry"]
base_output_dir = "downloaded_images"
os.makedirs(base_output_dir, exist_ok=True)

log_filename = "download_log.txt"
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', handlers=[
    logging.FileHandler(log_filename),
    logging.StreamHandler()
])


def log(message):
    logging.info(message)


def download_image(url, output_path):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            log(f"✅ Downloaded: {output_path}")
            return True
        else:
            log(f"❌ Failed: {url} (Status Code: {response.status_code})")
            return False
    except Exception as e:
        log(f"⚠️ Error downloading {url}: {e}")
        return False


for sector in sector_folders:
    sector_path = os.path.join(os.getcwd(), sector)
    output_sector_path = os.path.join(base_output_dir, sector)
    os.makedirs(output_sector_path, exist_ok=True)

    log(f"📂 Processing Sector: {sector}")
    json_files = [f for f in os.listdir(sector_path) if f.endswith(".json")]

    if not json_files:
        log(f"⚠️ No JSON files found in {sector}")
        continue

    total_json = len(json_files)
    log(f"📄 Found {total_json} JSON files in {sector}")

    image_count = 0
    for json_index, file_name in enumerate(json_files, start=1):
        json_path = os.path.join(sector_path, file_name)
        log(f"🔍 [{json_index}/{total_json}] Processing file: {file_name}")

        try:
            # Load JSON file
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            images_in_file = 0
            for item in data:
                if "imageURL" in item:
                    image_url = item["imageURL"]

                    # Extract the filename from the URL
                    parsed_url = urlparse(image_url)
                    image_filename = os.path.basename(parsed_url.path)
                    image_filename = os.path.join(output_sector_path, image_filename)

                    if download_image(image_url, image_filename):
                        image_count += 1
                        images_in_file += 1

            log(f"📥 Downloaded {images_in_file} images from {file_name}")

        except Exception as e:
            log(f"⚠️ Error reading {json_path}: {e}")

    log(f"✅ Finished {sector}: {image_count} images downloaded\n" + "-"*50)

log("🎉 All sectors processed successfully!")

























# import os
# import json
# import requests
# import logging

# sector_folders = ["Automotive_Transport", "Manufacturing_Industry"]
# base_output_dir = "downloaded_images"
# os.makedirs(base_output_dir, exist_ok=True)

# log_filename = "download_log.txt"
# logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', handlers=[
#     logging.FileHandler(log_filename),
#     logging.StreamHandler()
# ])


# def log(message):
#     logging.info(message)


# def download_image(url, filename):
#     try:
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             with open(filename, "wb") as f:
#                 f.write(response.content)
#             log(f"✅ Downloaded: {filename}")
#             return True
#         else:
#             log(f"❌ Failed: {url} (Status Code: {response.status_code})")
#             return False
#     except Exception as e:
#         log(f"⚠️ Error downloading {url}: {e}")
#         return False


# for sector in sector_folders:
#     sector_path = os.path.join(os.getcwd(), sector)
#     output_sector_path = os.path.join(base_output_dir, sector)
#     os.makedirs(output_sector_path, exist_ok=True)

#     log(f"📂 Processing Sector: {sector}")
#     json_files = [f for f in os.listdir(sector_path) if f.endswith(".json")]

#     if not json_files:
#         log(f"⚠️ No JSON files found in {sector}")
#         continue

#     total_json = len(json_files)
#     log(f"📄 Found {total_json} JSON files in {sector}")

#     image_count = 0
#     for json_index, file_name in enumerate(json_files, start=1):
#         json_path = os.path.join(sector_path, file_name)
#         log(f"🔍 [{json_index}/{total_json}] Processing file: {file_name}")

#         try:
#             # Load JSON file
#             with open(json_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)

#             images_in_file = 0
#             for item in data:
#                 if "imageURL" in item:
#                     image_url = item["imageURL"]
#                     image_filename = os.path.join(
#                         output_sector_path, f"image_{image_count}.jpg")
#                     if download_image(image_url, image_filename):
#                         image_count += 1
#                         images_in_file += 1

#             log(f"📥 Downloaded {images_in_file} images from {file_name}")

#         except Exception as e:
#             log(f"⚠️ Error reading {json_path}: {e}")

#     log(f"✅ Finished {sector}: {image_count} images downloaded\n" + "-"*50)

# log("🎉 All sectors processed successfully!")
