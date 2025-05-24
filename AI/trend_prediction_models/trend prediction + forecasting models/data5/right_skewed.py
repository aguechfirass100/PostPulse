"""
Generates synthetic social media engagement data with strong right-skewed temporal patterns.
Key characteristics:
1. Right-skewed Weibull distribution peaking around day 3
2. Platform-specific behaviors:
   - Likes: Highest volume, moderate decay
   - Comments: Faster decay, lower baseline
   - Shares: Slowest decay, lowest volume
3. Daily cycles with:
   - Active hours (8AM-11PM) with sinusoidal patterns
   - Nighttime baseline engagement
4. Configurable noise levels per metric

Outputs JSON with aligned hourly timestamps for 2 weeks.
Example structure:
[
    {
        "timestamp": "2025-04-17 15:45",
        "likes": 642,
        "comments": 193,
        "shares": 86
    },
    ...
]
"""

import numpy as np
from datetime import datetime, timedelta
import random
import json
from math import sin, pi, exp

def simulate_metric(
    start_time: datetime,
    duration_hours: int,
    metric_type: str,  # 'likes', 'comments', or 'shares'
    noise_level: float = 0.1
):
    # Base parameters
    base_params = {
        'likes': {'peak': 800, 'decay': 0.12, 'daily_min': 0.15},
        'comments': {'peak': 240, 'decay': 0.15, 'daily_min': 0.10},
        'shares': {'peak': 120, 'decay': 0.10, 'daily_min': 0.08}
    }
    params = base_params[metric_type]
    
    data = []
    peak_day = 3  # Right-skewed peak occurs around day 3
    
    for hour in range(duration_hours):
        current_time = start_time + timedelta(hours=hour)
        hour_of_day = current_time.hour
        days_passed = hour / 24
        
        # --- 1. Right-Skewed Daily Average Curve ---
        # Weibull distribution parameters for right-skewed peak
        shape = 1.5  # Controls skewness (higher = more right-skewed)
        scale = 5.0  # Controls spread
        
        # Convert days to distribution scale
        x = days_passed + 0.5  # +0.5 to avoid zero-day issues
        daily_avg_mult = (shape/scale) * (x/scale)**(shape-1) * exp(-(x/scale)**shape)
        daily_avg_mult /= 0.35  # Normalize so peak ≈1.0
        
        # --- 2. Hourly Engagement Pattern ---
        if 8 <= hour_of_day <= 23:  # Active hours (8AM-11PM)
            hour_mult = 0.7 + 0.3 * sin(2*pi*(hour_of_day-8)/16)
        else:  # Low engagement hours
            hour_mult = params['daily_min'] + (0.2 * random.random())
        
        # --- 3. Combine Effects ---
        base_value = params['peak'] * daily_avg_mult * hour_mult
        
        # Add noise with minimum value
        value = max(
            3,  # Absolute minimum
            int(base_value * (1 + random.gauss(0, noise_level)))
        )
        
        data.append({
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M"),
            "value": value
        })
    
    return data

if __name__ == "__main__":
    start = datetime(2025, 4, 17, 15, 45)  # Thursday 3:45 PM
    hours = 336  # 2 weeks duration

    # Generate metrics
    likes = simulate_metric(start, hours, 'likes', noise_level=0.12)
    comments = simulate_metric(start, hours, 'comments', noise_level=0.15)
    shares = simulate_metric(start, hours, 'shares', noise_level=0.18)

    # Combine data
    combined_data = []
    for i in range(hours):
        combined_data.append({
            "timestamp": likes[i]["timestamp"],
            "likes": likes[i]["value"],
            "comments": comments[i]["value"],
            "shares": shares[i]["value"]
        })

    with open("trend prediction + forecasting models/data5/right_skewed_engagement.json", "w") as f:
        json.dump(combined_data, f, indent=4)