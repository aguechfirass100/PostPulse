import os
import json
import time
import logging
from apify_client import ApifyClient
from random import randint


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scraping_log.log")
    ]
)

API_TOKEN = "apify_api_zW7y7RscMDje9ZjWyXnSfwDvtqLu3v3tKDKX"
client = ApifyClient(API_TOKEN)

sectors = {
    "Manufacturing_Industry": [
        # "Renewable energy equipment social media ad poster",
        # "Industrial safety gear promotional image",
        # "Packaging machinery advertisement",
        # "CNC machining services marketing poster",
        # "Plastic injection molding services ad",
        # "Pharmaceutical manufacturing equipment social media ad",
        # "Water treatment plant services promotional poster",
        # "Agricultural machinery advertisement",
        # "HVAC systems industrial ad poster",
        # "Mining equipment marketing image",
        # "Pulp and paper industry machinery ad",
        # "Semiconductor manufacturing equipment social media poster",
        # "Industrial painting services promotional image",
        # "Food packaging solutions advertisement",
        # "Textile dyeing machinery marketing poster",
        # "Industrial air compressor ad",
        # "Waste recycling equipment social media ad poster",
        # "Industrial heating systems promotional image",
        # "Laser cutting services advertisement",
        # "Oil and gas industry equipment marketing poster",
        # "Industrial automation software ad",
        # "Robotic welding systems social media poster",
        # "Material handling equipment promotional image",
        # "Industrial filtration systems advertisement",
        # "Solar panel manufacturing equipment marketing poster",
        # "Industrial conveyor systems ad",
        # "Biotechnology manufacturing services social media ad",
        # "Industrial water pumps promotional poster",
        # "Cleanroom equipment advertisement",
        # "Industrial sensors and controls marketing image",
        # "Heavy equipment rental social media ad poster",
        # "Factory machinery social media ad poster",
        # "Industrial robotics social media ad poster",
        # "3D printing industry social media ad poster",
        # "Construction materials social media ad poster",
        # "Metal fabrication services social media ad poster",
        # "Textile manufacturing social media ad poster",
        # "Chemical production plant social media ad poster",
        # "Energy sector equipment social media ad poster",
        # "Food processing machinery social media ad poster",
        # "Additive manufacturing services social media ad poster",
        # "Automation systems for factories social media ad poster",
        # "Industrial maintenance services social media ad poster",
        # "Supply chain solutions for manufacturing social media ad poster",
        # "Advanced manufacturing technology social media ad poster",
        # "Custom metal fabrication social media ad poster",
        # "Industrial waste management social media ad poster",
        # "Construction site safety equipment social media ad poster",
        # "Industrial 3D printing service social media ad poster",
        # "Smart factory solutions social media ad poster"
    ],
    "Automotive_Transport": [
        # "Car maintenance service social media ad poster",
        # "Luxury yacht promotional image",
        # "Bicycle brand marketing poster",
        # "Taxi service advertisement",
        # "Car accessories promotional image",
        # "Boat rental service social media ad",
        # "Automotive parts supplier marketing poster",
        # "Scooter rental service advertisement",
        # "Luxury RV promotional image",
        # "Car wash service social media ad poster",
        # "Auto detailing service marketing poster",
        # "Tire shop promotional image",
        # "Car audio systems advertisement",
        # "Vehicle leasing service social media ad",
        # "Off-road vehicle marketing poster",
        # "Car modification service promotional image",
        # "Electric bicycle advertisement",
        # "Luxury limousine service social media ad",
        # "Car window tinting service marketing poster",
        # "Vehicle tracking system promotional image",
        "Car rental deals advertisement",
        "Motorhome sales social media ad poster",
        "Automotive repair tools marketing poster",
        "Classic car restoration service promotional image",
        "Car security systems advertisement",
        "Vehicle graphics and wraps social media ad",
        "Luxury car rental service marketing poster",
        "Automotive diagnostic services promotional image",
        "Car performance tuning advertisement",
        "Vehicle emission testing service social media ad",
        # "Luxury car social media ad poster",
        # "Electric vehicle social media ad poster",
        # "Car dealership discount social media ad poster",
        # "Truck rental service social media ad poster",
        # "Motorcycle brand social media ad poster",
        # "Public transportation service social media ad poster",
        # "Auto repair shop social media ad poster",
        # "Car insurance promotion social media ad poster",
        # "Ride-sharing service social media ad poster",
        # "EV charging station social media ad poster",
        # "Electric truck social media ad poster",
        # "Autonomous vehicle technology social media ad poster",
        # "Vehicle fleet management software social media ad poster",
        # "Luxury sports car social media ad poster",
        # "Hybrid vehicle promotion social media ad poster",
        # "Car rental service social media ad poster",
        # "Electric scooter social media ad poster",
        # "Cargo shipping service social media ad poster",
        # "Logistics and delivery services social media ad poster",
        # "Motorcycle safety gear social media ad poster"
    ]
}

for sector in sectors.keys():
    os.makedirs(sector, exist_ok=True)


def scrape_data(sector, query):
    logging.info(f"Scraping images for: {query}")
    run_input = {
        "query": query,
        "filter": "all",
        "limit": 200,
    }

    retries = 3
    delay = randint(3, 6)

    for attempt in range(retries):
        try:
            run = client.actor("NagEuvONHQtmNhnle").call(run_input=run_input)
            dataset = list(client.dataset(
                run["defaultDatasetId"]).iterate_items())

            filename = query.replace(" ", "_").lower() + ".json"
            filepath = os.path.join(sector, filename)

            with open(filepath, "w") as f:
                json.dump(dataset, f, indent=4)

            logging.info(f"✅ Saved {len(dataset)} entries to {filepath}")
            time.sleep(delay)
            return

        except Exception as e:
            logging.error(
                f"❌ Error scraping {query}, attempt {attempt + 1}: {e}")
            time.sleep(randint(3, 6))

    logging.error(f"❌ Failed to scrape {query} after {retries} attempts")


def main():
    for sector, queries in sectors.items():
        for query in queries:
            scrape_data(sector, query)


if __name__ == "__main__":
    main()
