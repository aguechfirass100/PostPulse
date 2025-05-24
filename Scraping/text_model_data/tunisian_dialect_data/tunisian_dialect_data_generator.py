import os
import json
import time
from google.generativeai import configure, GenerativeModel

industry = "Automotive_Transport"
num_samples = 500
output_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/text_model_data/tunisian_dialect_data/output/output.json"
log_path = "/home/AGFirass/Documents/4DS5-S2/PIDEV/Scraping/text_model_data/tunisian_dialect_data/output/output.log"
api_key = "api key goes here"

configure(api_key=api_key)
model = GenerativeModel("gemini-1.5-flash")

PROMPT_GENERATION_TEMPLATE = (
    "Generate an English prompt for a Tunisian dialect social media caption. "
    "The caption should be: "
    "- One sentence long, clear, and easy to read for a local Tunisian audience. "
    "- Engaging and tailored for marketing/advertisement use on platforms like Instagram, Facebook, or Twitter. "
    "- Fun, informal, and attention-grabbing to appeal to younger generations. "
    "- Focused on highlighting the product's benefits or unique selling points in a way that resonates with Tunisian culture. "
    "The prompt should request the generation of a short, catchy, and creative social media caption in Tunisian dialect. "
    "The caption should have a friendly and conversational tone, as if a local influencer is promoting the product. "
    "Avoid overly formal language or complicated expressions. Keep it lighthearted and relatable."
    "please make sure you dont use arabic letters when writing tunisian dialects, just use english lettters."
    "please just give direct response,, just give one option directly, no need for any other thing, no need for intro, or here is, or anything"
    "just give me directly the response that i need, no options, no translations, nothing"
    "the human prompt: it should be a prompt that a user gives to a text to text generation model so he can generate in the tunisian dialect"
    "the gpt is the response in tunisian dialect"
    "for example human: Write a Tunisian caption to promote our new gourmet burger at Burger House and gpt would be: 🍔 El burger jdiiid fi Burger House ykhalleek tansa esmek 😍🔥 mat3am mouch normal! fech testana mala🧀🍟 #BurgerHouseTN #MallaT3am"
    "and please in the gpt do not give me a lot of options, just give me one option, any random option, tone does not matter, do not give me translation too"
)

def load_log(log_path):
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return int(f.read().strip() or 0)
    return 0

def save_log(log_path, count):
    with open(log_path, "w") as f:
        f.write(str(count))

def main():
    print(f"[INFO] Starting Gemini-powered data generation...")
    generated_count = load_log(log_path)
    print(f"[INFO] Resuming from: {generated_count}/{num_samples}")

    if generated_count >= num_samples:
        print("[INFO] Already completed. Exiting.")
        return

    data = []
    if os.path.exists(output_path):
        try:
            with open(output_path, "r") as f:
                data = json.load(f)
        except Exception:
            print("[WARN] Output file unreadable. Starting fresh.")
            data = []

    while generated_count < num_samples:
        print(f"\n[STEP] Generating prompt {generated_count + 1}/{num_samples}")
        
        try:
            prompt_gen_response = model.generate_content(PROMPT_GENERATION_TEMPLATE.format(industry=industry))
            human_prompt = prompt_gen_response.text.strip()
            print(f"[PROMPT] {human_prompt}")

            # Adding a delay of 5 seconds between each API call
            time.sleep(5)

            ai_response = model.generate_content(human_prompt)
            gpt_value = ai_response.text.strip()
            print(f"[RESPONSE] {gpt_value}")

            sample = [
                {"from": "human", "value": human_prompt},
                {"from": "gpt", "value": gpt_value}
            ]

            data.extend(sample)
            generated_count += 1
            save_log(log_path, generated_count)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"[✔] Saved sample {generated_count}/{num_samples}")

        except Exception as e:
            print(f"[ERROR] Failed to generate content: {e}")
            print("[INFO] Retrying in 5 seconds...")
            time.sleep(5)

    print(f"\n[✅ DONE] All {num_samples} samples generated and saved to {output_path}")

if __name__ == "__main__":
    main()
