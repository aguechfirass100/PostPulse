import json

with open('/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/sentiment analysis/TTTT-fixed_comments.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for entry in data:
    entry['comment'] = entry['comment'].encode('latin1').decode('utf-8')

with open('TTTT-decoded_comments.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Comments have been decoded and saved to decoded_comments.json")
