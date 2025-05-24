import json

# Path to your JSON file
# Update with actual path
json_file_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/descriptions_generator/descriptions/Manufacturing_Industry/Manufacturing_Industry.json"

# Load the JSON file
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Count the number of top-level keys (IDs)
num_ids = len(data.keys())

# Print the result
print(f"Number of IDs in the JSON file: {num_ids}")
