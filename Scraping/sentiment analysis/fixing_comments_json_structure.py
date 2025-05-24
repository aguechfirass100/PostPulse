import json

with open("/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/sentiment analysis/TTTT-cleaned_Sentiments_Analysis_Data_Set_English_Comments.json", "r", encoding="utf-8") as f:
    lines = f.readlines()

comments = [json.loads(line) for line in lines]

with open("/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/sentiment analysis/TTTT-fixed_comments.json", "w", encoding="utf-8") as f:
    json.dump(comments, f, indent=4)

print("Fixed JSON saved as fixed_comments.json")
