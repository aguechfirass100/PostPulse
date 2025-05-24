import os
import json
import shutil
from pathlib import Path
from tqdm import tqdm

# 🔧 Hardcoded paths
ROOT_FOLDER = "/home/firas/dataset_raw"
OUTPUT_FOLDER = "/home/firas/dataset_processed"

def process_dataset():
    root_path = Path(ROOT_FOLDER)
    output_path = Path(OUTPUT_FOLDER)

    # Create output folders
    images_out = output_path / "all_images"
    captions_out = output_path / "captions"
    images_out.mkdir(parents=True, exist_ok=True)
    captions_out.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Starting processing...")
    print(f"[INFO] Root folder     : {root_path}")
    print(f"[INFO] Output folder   : {output_path}")

    img_counter = 1

    # Loop through each of the 11 subfolders
    for folder in sorted(root_path.iterdir()):
        if not folder.is_dir():
            continue
        print(f"\n[INFO] 📂 Processing folder: {folder.name}")

        # Find JSON file
        json_file = None
        for file in folder.glob("*.json"):
            json_file = file
            break
        if not json_file:
            print(f"[⚠️ WARNING] No JSON file found in {folder.name}. Skipping.")
            continue

        # Find image folder (assume only one folder that contains images)
        img_folder = None
        for sub in folder.iterdir():
            if sub.is_dir():
                # Check if this folder contains image files
                img_files = list(sub.glob("*.[pjJP][npNP]*[gG]"))  # matches jpg/jpeg/png
                if len(img_files) >= 10:  # sanity check
                    img_folder = sub
                    break
        if not img_folder:
            print(f"[⚠️ WARNING] No image folder found in {folder.name}. Skipping.")
            continue

        print(f"[✓] Found JSON file  : {json_file.name}")
        print(f"[✓] Found image folder: {img_folder.name}")

        with open(json_file, 'r', encoding='utf-8') as f:
            captions = json.load(f)

        image_files = list(img_folder.glob("*"))

        # Process each image
        for img_file in tqdm(image_files, desc=f"Processing images in {folder.name}"):
            image_stem = img_file.stem
            if image_stem not in captions:
                print(f"[⚠️ WARNING] No caption for image: {img_file.name}. Skipping.")
                continue

            ext = img_file.suffix.lower()
            new_img_name = f"img{img_counter}{ext}"
            new_caption_name = f"img{img_counter}.txt"

            # Copy image
            shutil.copy(img_file, images_out / new_img_name)

            # Save caption
            with open(captions_out / new_caption_name, 'w', encoding='utf-8') as txt_file:
                txt_file.write(captions[image_stem].strip())

            img_counter += 1

    print("\n✅ [DONE] All images and captions have been processed.")
    print(f"📁 Images saved to   : {images_out}")
    print(f"📝 Captions saved to : {captions_out}")


if __name__ == "__main__":
    process_dataset()
