import json

# Specify the input and output file names
input_file = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/text_model_data/Manufacturing_Industry/Manufacturing_Industry_text_data.json"    # change this to the path of your JSON file
output_file = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/text_model_data/Manufacturing_Industry/Manufacturing_Industry_text_data_formatted.json"  # the file where the reformatted data will be saved

# Load the original dataset
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Create an output list where each record is two dictionaries:
# one from the human prompt and one from the GPT answer.
output = []
for record in data:
    human_message = {
        "from": "human",
        "value": record["prompt"]
    }
    gpt_message = {
        "from": "gpt",
        "value": record["description"]
    }
    output.extend([human_message, gpt_message])

# Write the new data to the output file with proper formatting
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Reformatted dataset saved to {output_file}")
