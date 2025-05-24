import json

# Path to your JSON file
input_json_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/descriptions_generator/descriptions/Manufacturing_Industry/Manufacturing_Industry.json"  # File with "image_id": {"tone", "description"}
output_json_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/descriptions_generator/descriptions/Manufacturing_Industry/Manufacturing_Industry_cleaned.json"  # Output file

# Load the JSON file
with open(input_json_path, "r") as input_file:
    data = json.load(input_file)

# Function to clean the description
def clean_description(description):
    # Split the description by "\n\n"
    parts = description.split("\n\n", 1)
    # If there are two parts, return the second part; otherwise, return the original description
    return parts[1] if len(parts) > 1 else description

# Iterate through the data and clean the descriptions
for image_id, content in data.items():
    description = content.get("description", "")
    content["description"] = clean_description(description)

# Save the cleaned data to a new JSON file
with open(output_json_path, "w") as output_file:
    json.dump(data, output_file, indent=4)

print(f"Cleaned data saved to {output_json_path}")