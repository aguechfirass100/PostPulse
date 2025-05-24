import json

# Paths to your JSON files
prompt_json_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/prompts/Manufacturing_Industry/Manufacturing_Industry.json"  # File with "image_id": "prompt"
description_json_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/descriptions_generator/descriptions/Manufacturing_Industry/Manufacturing_Industry_cleaned.json"  # File with "image_id": {"description", "tone"}
output_json_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/descriptions_generator/descriptions/Manufacturing_Industry/Manufacturing_Industry_cleaned__with_prompts.json"  # Output file

# Load the first JSON file (image_id: prompt)
with open(prompt_json_path, "r") as prompt_file:
    prompts_data = json.load(prompt_file)

# Load the second JSON file (image_id: {description, tone})
with open(description_json_path, "r") as description_file:
    descriptions_data = json.load(description_file)

# Create a new dictionary to store the merged data
merged_data = {}

# Iterate through the prompts data and merge with descriptions
for image_id, prompt in prompts_data.items():
    if image_id in descriptions_data:
        # Get the description and tone from the second file
        description_info = descriptions_data[image_id]
        description = description_info.get("description", "")
        tone = description_info.get("tone", "")

        # Add the merged data to the new dictionary
        merged_data[image_id] = {
            "prompt": prompt,
            "description": description,
            "tone": tone
        }

# Save the merged data to a new JSON file
with open(output_json_path, "w") as output_file:
    json.dump(merged_data, output_file, indent=4)

print(f"Merged data saved to {output_json_path}")
