import os
import json
import google.generativeai as genai
from PIL import Image
import io
import base64
import threading
from queue import Queue
import time
from datetime import datetime

# List of API keys (one per thread)
first_key = "AIzaSyDp3loz-ah-YQ4hTrcuP77J_G8--xTXYGI"
second_key = "AIzaSyCVMtwzvQ0sGg1b0YMb9Adc34EzIBaFP8w"

API_KEYS = [first_key]

# Path to your folder containing images
# Replace with the path to your image folder
IMAGE_FOLDER = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/data_to_upload/Manufacturing_Industry/images"

# Output JSON file
OUTPUT_JSON = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/data_to_upload/Manufacturing_Industry/Manufacturing_Industry.json"

# Log file to track processed images
LOG_FILE = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/data_to_upload/Manufacturing_Industry/Manufacturing_Industry.log"

# Number of threads (one per API key)
NUM_THREADS = len(API_KEYS)

# Queue to hold images to be processed
image_queue = Queue()

# Lock for thread-safe writing to the JSON file and log file
json_lock = threading.Lock()
log_lock = threading.Lock()


def generate_prompt_for_image(image_path, api_key):
    """Generates a prompt for the given image using Google's Generative AI."""
    try:
        # Configure the Google Generative AI library with the thread's API key
        genai.configure(api_key=api_key)

        # Load the image using PIL
        with Image.open(image_path) as img:
            # Convert the image to RGB mode if it's in P or RGBA mode
            if img.mode in ['P', 'RGBA']:
                img = img.convert('RGB')

            # Convert the image to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="JPEG")
            img_bytes = img_bytes.getvalue()

            # Encode the image as base64
            image_base64 = base64.b64encode(img_bytes).decode("utf-8")
            # Debug statement
            print(f"Loaded image: {image_path}, size: {len(img_bytes)} bytes")

        # Verify the image data is not empty or corrupted
        if len(image_base64) == 0:
            print(f"Error: Image file is empty: {image_path}")
            return None

        # Use the Generative AI model to describe the image
        model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model name
        response = model.generate_content(
            [
                "Describe this image in detail as a single block of text. Include the subject, setting, colors, mood, and perspective. "
                "Write it in a way that could be used as a prompt for a generative image model, with a natural flow and no bullet points or numbered items.",
                # Pass image as base64
                {"mime_type": "image/jpeg", "data": image_base64}
            ]
        )

        # Debug: Print the API response
        print(f"API Response for {image_path}: {response}")

        # Return the generated text
        return response.text

    except Exception as e:
        # Print the exact error message
        print(f"Error generating prompt for {image_path}: {str(e)}")
        return None


def load_processed_images(log_file):
    """Loads the list of already processed images from the log file."""
    if os.path.exists(log_file):
        with open(log_file, "r") as log:
            return set(line.strip().split(" - ")[2] for line in log.readlines() if "Processed" in line)
    return set()


def update_log_file(log_file, thread_id, image_name, status, error=None):
    """Updates the log file with details of the processed image."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Thread {thread_id} - {image_name} - {status}"
    if error:
        log_entry += f" - Error: {error}"
    log_entry += "\n"

    with log_lock:
        with open(log_file, "a") as log:
            log.write(log_entry)


def process_image(image_name, api_key, thread_id, image_prompts):
    """Processes a single image and updates the JSON file and log file."""
    image_id = os.path.splitext(image_name)[0]  # Use the image name as the ID
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    print(f"Processing image: {image_name}")

    # Generate a prompt for the image
    prompt = generate_prompt_for_image(image_path, api_key)

    if prompt:
        # Add the prompt to the dictionary
        with json_lock:
            image_prompts[image_id] = prompt
            print(f"Generated prompt for {image_name}")

            # Save the updated prompts to the JSON file
            with open(OUTPUT_JSON, "w") as json_file:
                json.dump(image_prompts, json_file, indent=4)
                print(f"Updated JSON file with prompt for {image_name}")

        # Update the log file
        update_log_file(LOG_FILE, thread_id, image_name, "Processed")
        print(f"Updated log file with {image_name}")
    else:
        # Update the log file with the error
        update_log_file(LOG_FILE, thread_id, image_name,
                        "Skipped", error="Failed to generate prompt")
        print(f"Skipping {image_name} due to an error.")


def worker(api_key, thread_id, image_prompts):
    """Worker function to process images from the queue."""
    while not image_queue.empty():
        # Get an image from the queue
        image_name = image_queue.get()

        # Process the image
        process_image(image_name, api_key, thread_id, image_prompts)

        # Mark the task as done
        image_queue.task_done()


def main():
    """Main function to process images and save prompts to a JSON file."""
    # Load existing prompts if the JSON file exists
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r") as json_file:
            image_prompts = json.load(json_file)
    else:
        image_prompts = {}

    # Load the list of already processed images
    processed_images = load_processed_images(LOG_FILE)

    # Add unprocessed images to the queue
    for image_name in os.listdir(IMAGE_FOLDER):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            if image_name not in processed_images:
                image_queue.put(image_name)

    # Create and start worker threads
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(
            API_KEYS[i], i + 1, image_prompts))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All prompts processed and saved to JSON file.")


if __name__ == "__main__":
    main()
