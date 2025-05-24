import os
import json
import random
import logging
import re
from PIL import Image
from time import sleep
import google.generativeai as genai


# ======================== USER CONFIGURATION ========================
SECTOR_NAME = "Automotive_Transport"  # Change this for each sector
IMAGE_DIR = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/data_to_upload/Automotive_Transport/Automotive_Transport images"  # Path to sector's images folder
PROMPT_JSON_PATH = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/data_to_upload/Automotive_Transport/Automotive_Transport.json"  # Path to sector's prompt JSON
OUTPUT_JSON_PATH = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/text_model_data/Automotive_Transport/Automotive_Transport_text_data.json"  # Where to save final dataset
LOG_PATH = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/text_model_data/Automotive_Transport/Automotive_Transport_text_data.log"
GEMINI_API_KEY = "your_api_key_here"
# ====================================================================

TONES = [
    "Professional", "Casual", "Persuasive", "Inspirational/Motivational",
    "Humorous", "Informative", "Fear of missing out", "Storytelling",
    "Sarcastic", "Supportive"
]
PLATFORMS = ["Facebook", "Instagram", "Twitter", "LinkedIn"]
NUM_IMAGES = 600
MAX_RETRIES = 3
API_DELAY = 1

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

def get_processed_ids():
    """Extract processed image IDs from log file"""
    processed = set()
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            for line in f:
                match = re.search(r"Successfully processed image_id: (\w+)", line)
                if match:
                    processed.add(match.group(1))
    return processed

def process_sector():
    # Initialize Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Load existing data and prompts
    existing_data = []
    if os.path.exists(OUTPUT_JSON_PATH):
        with open(OUTPUT_JSON_PATH, 'r') as f:
            existing_data = json.load(f)

    with open(PROMPT_JSON_PATH, 'r') as f:
        all_prompts = json.load(f)

    # Get already processed IDs
    processed_ids = get_processed_ids()
    available_ids = [img_id for img_id in all_prompts if img_id not in processed_ids]
    needed = NUM_IMAGES - len(existing_data)
    
    if needed <= 0:
        logging.info(f"Sector {SECTOR_NAME} already completed")
        return

    # Select remaining images
    selected_ids = random.sample(available_ids, min(needed, len(available_ids)))
    
    # Create balanced tone-platform distribution
    combinations = [(t, p) for t in TONES for p in PLATFORMS]
    required_per_combination = NUM_IMAGES // len(combinations)
    balanced_pairs = (combinations * required_per_combination)[:len(selected_ids)]
    random.shuffle(balanced_pairs)

    # Process images
    for idx, (image_id, (tone, platform)) in enumerate(zip(selected_ids, balanced_pairs)):
        entry = None
        image_path = os.path.join(IMAGE_DIR, f"{image_id}.jpg")
        
        try:
            img = Image.open(image_path)
        except Exception as e:
            logging.error(f"Image load failed: {image_id} - {str(e)}")
            continue

        # Enhanced prompt template
        system_prompt = f"""**Sector:** {SECTOR_NAME}
**Platform:** {platform}
**Tone:** {tone}
**Image Context:** {all_prompts[image_id]}

Generate:
1. A text generation prompt starting with "Create a {tone.lower()} {platform} post..."
2. Marketing copy that includes:
   - 2-3 relevant emojis
   - 1-2 hashtags
   - Clear call-to-action
   - Platform-appropriate length
   - {SECTOR_NAME}-specific terminology

**Format EXACTLY like this:**
Prompt: [generated prompt]
Description: [generated description]"""

        for attempt in range(MAX_RETRIES + 1):
            try:
                response = model.generate_content([system_prompt, img])
                response_text = response.text
                
                # Parse response
                prompt = response_text.split("Prompt: ")[1].split("Description: ")[0].strip()
                description = response_text.split("Description: ")[1].strip()

                # Create entry (without image_id)
                entry = {
                    "prompt": prompt,
                    "description": description,
                    "tone": tone,
                    "platform": platform
                }

                # Log first before saving
                logging.info(f"Successfully processed image_id: {image_id}")
                existing_data.append(entry)
                
                # Save incremental progress
                with open(OUTPUT_JSON_PATH, 'w') as f:
                    json.dump(existing_data, f, indent=2)
                
                sleep(API_DELAY)
                break

            except Exception as e:
                if attempt == MAX_RETRIES:
                    logging.error(f"Failed after {MAX_RETRIES} attempts: {image_id}")
                else:
                    sleep(2 ** attempt)  # Exponential backoff

if __name__ == "__main__":
    logging.info(f"\n{'='*40}\nStarting processing for sector: {SECTOR_NAME}\n{'='*40}")
    process_sector()
    logging.info(f"\n{'='*40}\nCompleted processing for sector: {SECTOR_NAME}\n{'='*40}")