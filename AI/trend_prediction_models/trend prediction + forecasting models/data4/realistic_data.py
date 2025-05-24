"""
Generates coordinated synthetic engagement metrics (likes/comments/shares) with:
1. Realistic scaling between metrics (comments ≈30% of likes, shares ≈15%)
2. Three-phase engagement lifecycle:
   - Initial ramp-up period
   - Sustained peak engagement (72 hours)
   - Gradual exponential decay
3. Daily activity patterns (higher engagement 8AM-12AM)
4. Configurable noise levels per metric

Outputs JSON with aligned timestamps for time series analysis.
Example output structure:
[
    {
        "timestamp": "2025-04-17 15:45",
        "likes": 215,
        "comments": 72,
        "shares": 32
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
    metric_type: str,  # 'likes', 'comments', or 'shares'
    noise_level: float = 0.1
):
    # Base parameters (all metrics scale from these)
    base_peak = 1000  # Reference peak value for likes
    
    # Metric-specific multipliers
    multipliers = {
        'likes': 1.0,
        'comments': 0.3,  # Typically 30% of likes
        'shares': 0.15    # Typically 15% of likes
    }
    
    # Time parameters
    peak_start = 3  # Hours until initial peak
    peak_duration = 72  # 3-day high-engagement window
    full_decay_days = 14  # Days until near-zero engagement
    
    data = []
    
    for hour in range(duration_hours):
        current_time = start_time + timedelta(hours=hour)
        hour_of_day = current_time.hour
        days_passed = hour / 24
        
        # --- 1. Daily Activity Cycle ---
        # Active hours (8AM - 12AM)
        if 8 <= hour_of_day <= 23:
            daily_mult = 0.7 + 0.3 * sin(2*pi*(hour_of_day-8)/16)
        else:
            daily_mult = 0.2 + 0.1 * random.random()  # 20-30% of peak
        
        # --- 2. Engagement Lifecycle Curve ---
        if hour < peak_start:
            # Initial ramp-up (first few hours)
            life_mult = (hour / peak_start) ** 2
        elif hour < peak_duration:
            # Peak period (full engagement)
            life_mult = 1.0
        else:
            # Slow decay after peak period
            decay_days = (hour - peak_duration) / 24
            life_mult = np.exp(-0.15 * decay_days)  # Gentle decay
        
        # --- 3. Combine Effects ---
        raw_value = (
            base_peak * 
            multipliers[metric_type] * 
            daily_mult * 
            life_mult
        )
        
        # Add controlled noise (avoid <5 values)
        value = max(
            5,  # Minimum engagement
            int(raw_value * (1 + random.gauss(0, noise_level)))
        )
        
        data.append({
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M"),
            "value": value
        })
    
    return data

if __name__ == "__main__":
    start = datetime(2025, 4, 17, 15, 45)  # 3:45 PM
    hours = 336  # 1 week simulation

    # Generate coordinated metrics
    likes = simulate_metric(start, hours, 'likes', noise_level=0.15)
    comments = simulate_metric(start, hours, 'comments', noise_level=0.2)
    shares = simulate_metric(start, hours, 'shares', noise_level=0.25)

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

    with open("trend prediction + forecasting models/data4/realistic_data.json", "w") as f:
        json.dump(combined_data, f, indent=4)