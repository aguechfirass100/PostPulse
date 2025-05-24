"""
Generates realistic synthetic social media engagement data with:
- Daily activity cycles (higher engagement during daytime hours)
- Multi-day peak engagement windows with exponential decay
- Configurable noise and platform-specific behaviors for:
  * Likes (broad daily engagement)
  * Comments (more daytime-focused)
  * Shares (late-night activity with slower decay)
  
Outputs JSON data with timestamps and metrics suitable for time series forecasting.
Example structure:
[
    {
        "timestamp": "2025-04-17 15:45",
        "likes": 174,
        "comments": 48,
        "shares": 26
    },
    ...
]
"""

import numpy as np
from datetime import datetime, timedelta
import random
import json
from math import sin, pi

def simulate_metric(
    start_time: datetime,
    duration_hours: int,
    peak_value: float = 500,
    noise_level: float = 0.15,
    # New parameters
    active_hours: tuple = (8, 23),  # 8AM - 11PM (high engagement)
    peak_duration_days: float = 3.0  # Engagement stays high for 3 days
):
    data = []
    peak_duration_hours = int(peak_duration_days * 24)
    
    for hour in range(duration_hours):
        current_time = start_time + timedelta(hours=hour)
        hour_of_day = current_time.hour
        
        # --- 1. Daily Activity Cycle ---
        if active_hours[0] <= hour_of_day <= active_hours[1]:
            # Daytime engagement multiplier (sinusoidal curve)
            daily_multiplier = 0.7 + 0.3 * sin(2 * pi * (hour_of_day - 8) / 24)
        else:
            # Nighttime engagement (10-30% of peak)
            daily_multiplier = 0.1 + 0.2 * random.random()  # Random low value

        # --- 2. Three-Day Peak Window ---
        if hour <= peak_duration_hours:
            # Initial peak period (full engagement)
            decay_multiplier = 1.0
        else:
            # Exponential decay after peak window
            decay_hours = hour - peak_duration_hours
            decay_multiplier = np.exp(-0.05 * decay_hours)  # Slow decay

        # --- Combine effects ---
        base_value = peak_value * daily_multiplier * decay_multiplier
        
        # Add noise (avoid zeros)
        value = max(1, int(base_value + random.gauss(0, peak_value * noise_level)))
        
        data.append({
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M"),
            "value": value
        })
    
    return data

if __name__ == "__main__":
    start = datetime(2025, 4, 17, 15, 45)  # 3:45 PM
    hours = 336  # Simulate 1 week

    # Generate metrics
    likes = simulate_metric(
        start, hours,
        peak_value=1000,
        noise_level=0.2,
        active_hours=(9, 23),  # 9AM - 11PM
        peak_duration_days=3
    )
    
    comments = simulate_metric(
        start, hours,
        peak_value=300,
        noise_level=0.25,
        active_hours=(10, 22),  # Comments more daytime-focused
        peak_duration_days=2.5
    )
    
    shares = simulate_metric(
        start, hours,
        peak_value=400,
        noise_level=0.3,
        active_hours=(8, 1),  # Shares can happen late (8AM - 1AM)
        peak_duration_days=4  # Shares decay slower (viral potential)
    )

    # Combine data
    combined_data = [
        {
            "timestamp": likes[i]["timestamp"],
            "likes": likes[i]["value"],
            "comments": comments[i]["value"],
            "shares": shares[i]["value"]
        }
        for i in range(hours)
    ]

    with open("trend prediction + forecasting models/data3/Daily_activity_cycle.json", "w") as f:
        json.dump(combined_data, f, indent=4)