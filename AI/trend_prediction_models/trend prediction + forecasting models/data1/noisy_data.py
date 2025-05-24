"""
Generates synthetic social media engagement data using a peak-and-decay model:
- Simulates a single engagement spike followed by exponential decay
- Adds configurable Gaussian noise for natural variation
- Customizable per-metric parameters:
  * Likes (fast initial rise, moderate decay)
  * Comments (sharp peak, quick drop-off)
  * Shares (delayed peak, slower decay)

Outputs JSON data with hourly timestamps and values, ideal for simulating post-lifecycle trends.
Example structure:
[
    {
        "timestamp": "2025-04-17 15:45",
        "likes": 431,
        "comments": 112,
        "shares": 89
    },
    ...
]
"""


import numpy as np
from datetime import datetime, timedelta
import random
import json

def simulate_metric(
    start_time: datetime,
    duration_hours: int,
    peak_time: float = 4.0,  # Time (in hours) when engagement peaks
    peak_value: float = 100,  # Maximum engagement value at peak
    decay_rate: float = 0.5,  # Controls how fast engagement decays (higher = faster decay)
    noise_level: float = 0.1  # Random noise to make it look natural
):
    data = []
    
    for hour in range(duration_hours):
        # Time since post (in hours, with fractional parts)
        t = hour + 0.5  # Adding 0.5 to smooth the curve
        
        # Modified log-normal formula for peak-and-decay behavior
        if t <= peak_time:
            # Growth phase (ramps up to peak)
            value = peak_value * (t / peak_time) ** 2
        else:
            # Decay phase (gradually decreases)
            value = peak_value * np.exp(-decay_rate * (t - peak_time))
        
        # Add noise (avoid negative values)
        value += random.gauss(0, peak_value * noise_level)
        value = max(1, round(value))  # Ensure at least 1 engagement
        
        timestamp = start_time + timedelta(hours=hour)
        data.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M"),
            "value": value
        })
    
    return data

if __name__ == "__main__":
    start = datetime(2025, 4, 17, 15, 45)
    hours = 336  # Track engagement for 3 days

    # Example usage:
    likes = simulate_metric(
        start, hours,
        peak_time=4.0, peak_value=500, decay_rate=0.3, noise_level=0.15
    )
    
    comments = simulate_metric(
        start, hours,
        peak_time=3.5, peak_value=150, decay_rate=0.4, noise_level=0.2
    )
    
    shares = simulate_metric(
        start, hours,
        peak_time=5.0, peak_value=200, decay_rate=0.25, noise_level=0.25
    )

    # Combine into one dataset
    combined_data = [
        {
            "timestamp": likes[i]["timestamp"],
            "likes": likes[i]["value"],
            "comments": comments[i]["value"],
            "shares": shares[i]["value"]
        }
        for i in range(hours)
    ]

    with open("trend prediction + forecasting models/data1/Noisy_Data.json", "w") as f:
        json.dump(combined_data, f, indent=4)