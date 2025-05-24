import os
import json

def remove_excess_images():
    # Define paths
    images_dir = '/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/downloaded_images/Manufacturing_Industry'
    excess_file = '/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/handling_excess_images/Manufacturing_Industry/images_without_prompts.json'
    
    # Validate paths
    if not os.path.exists(images_dir):
        print(f"Error: Images directory '{images_dir}' not found!")
        return
    
    if not os.path.exists(excess_file):
        print(f"Error: Excess images file '{excess_file}' not found!")
        return
    
    # Load excess images list
    try:
        with open(excess_file, 'r', encoding='utf-8') as f:
            excess_images = json.load(f)
    except Exception as e:
        print(f"Error loading excess images file: {e}")
        return
    
    if not excess_images:
        print("No excess images to remove")
        return
    
    # Remove images
    removed_count = 0
    already_removed_count = 0
    not_found_count = 0
    
    for img_id in excess_images:
        found = False
        # Check for different extensions
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
            img_path = os.path.join(images_dir, f"{img_id}{ext}")
            if os.path.exists(img_path):
                try:
                    os.remove(img_path)
                    removed_count += 1
                    print(f"Removed: {img_path}")
                    found = True
                    break
                except Exception as e:
                    print(f"Error removing {img_path}: {e}")
                    found = True
                    break
            elif os.path.exists(os.path.join(images_dir, img_id)):  # Case where image has no extension
                try:
                    os.remove(os.path.join(images_dir, img_id))
                    removed_count += 1
                    print(f"Removed extensionless file: {img_id}")
                    found = True
                    break
                except Exception as e:
                    print(f"Error removing extensionless file {img_id}: {e}")
                    found = True
                    break
        
        if not found:
            # Check if this was previously removed by looking for any extension
            any_extension_exists = any(
                os.path.exists(os.path.join(images_dir, f"{img_id}{ext}")) 
                for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
            )
            
            if not any_extension_exists:
                already_removed_count += 1
                print(f"Already removed: {img_id} (no files found with this ID)")
            else:
                not_found_count += 1
                print(f"Warning: ID exists but no matching files found: {img_id}")
    
    # Print summary
    print("\nRemoval Summary:")
    print(f"Successfully removed: {removed_count}")
    print(f"Already removed: {already_removed_count}")
    print(f"IDs not found: {not_found_count}")
    print(f"Total processed: {len(excess_images)}")
    
    return {
        'removed': removed_count,
        'already_removed': already_removed_count,
        'not_found': not_found_count
    }

if __name__ == "__main__":
    remove_excess_images()