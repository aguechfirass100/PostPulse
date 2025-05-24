import os
import json

def remove_excess_data():
    # Define paths (assuming this script is in the same directory as the data)
    images_dir = '/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/downloaded_images/Automotive_Transport'  # Folder containing images
    json_file = '/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/prompts/Automotive_Transport/Automotive_Transport.json'  # JSON file with prompts
    output_file = '/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/handling_excess_images/Automotive_Transport/images_without_prompts_final_check.json'  # Output file
    
    # Check if required files/directories exist
    if not os.path.exists(images_dir):
        print(f"Error: Images directory '{images_dir}' not found!")
        return
    
    if not os.path.exists(json_file):
        print(f"Error: JSON file '{json_file}' not found!")
        return
    
    # Load the prompts JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            prompts = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return
    
    # Get list of image files (without extensions)
    image_files = [os.path.splitext(f)[0] for f in os.listdir(images_dir) 
                  if os.path.isfile(os.path.join(images_dir, f))]
    
    # Find images without prompts
    images_without_prompts = []
    
    for image_id in image_files:
        if image_id not in prompts or not prompts[image_id].strip():
            images_without_prompts.append(image_id)
    
    # Print the size of the list
    print(f"Found {len(images_without_prompts)} images without prompts")
    
    # Save the results to a new JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(images_without_prompts, f, indent=4)
        print(f"Successfully saved image IDs to {output_file}")
    except Exception as e:
        print(f"Error saving output file: {e}")
    
    return images_without_prompts

if __name__ == "__main__":
    remove_excess_data()