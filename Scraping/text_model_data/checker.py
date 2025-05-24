import json

# Path to your JSON file
JSON_FILE_PATH = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/text_model_data/Automotive_Transport/Automotive_Transport_text_data.json"  # Change this to your actual file path

# Load the JSON file and count entries
try:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
        total_entries = len(data)
        print(f"\n📊 Total entries in the dataset: {total_entries}\n")
        
        if total_entries == 600:
            print("✅ You have exactly 600 entries!")
        elif total_entries > 600:
            print("⚠️ You have more than 600 entries!")
        else:
            print("❌ You have fewer than 600 entries!")
except Exception as e:
    print(f"❌ Error reading the JSON file: {e}")