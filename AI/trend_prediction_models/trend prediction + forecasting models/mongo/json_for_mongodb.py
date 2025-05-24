import json
from datetime import datetime

def convert_to_mongodb_time_series(input_file, output_file):
    # Load the original JSON data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Transform each entry
    transformed_data = []
    for entry in data:
        # Parse the existing timestamp
        original_timestamp = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M")
        
        # Create new MongoDB-compatible entry
        new_entry = {
            "timestamp": {"$date": original_timestamp.isoformat() + "Z"},
            "likes": entry['likes'],
            "comments": entry['comments'],
            "shares": entry['shares']
        }
        transformed_data.append(new_entry)
    
    # Save the transformed data
    with open(output_file, 'w') as f:
        json.dump(transformed_data, f, indent=2)

# Usage example:
convert_to_mongodb_time_series(
    input_file='right_skewed_engagement.json',
    output_file='mongodb_time_series_engagement.json'
)

print("Conversion complete! Ready for MongoDB import.")