import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def load_and_plot(json_file):
    # Load JSON data
    with open(json_file) as f:
        data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    # --- Calculate Peak Day (Dynamic) ---
    # Sum all metrics (likes + comments + shares) per day, then find the max
    daily_totals = df.resample('D').sum().sum(axis=1)  # Sum all metrics per day
    peak_day = daily_totals.idxmax()  # Date with highest total engagement
    
    # Create figure
    plt.figure(figsize=(15, 10))
    
    # --- Plot 1: Hourly Trends ---
    plt.subplot(2, 1, 1)
    for metric in ['likes', 'comments', 'shares']:
        plt.plot(df.index, df[metric], label=metric.capitalize(), alpha=0.8)
    
    plt.title('Hourly Engagement Trends')
    plt.ylabel('Count')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Highlight active hours (8AM-11PM)
    for day in pd.date_range(df.index[0].date(), df.index[-1].date()):
        plt.axvspan(
            datetime.combine(day, datetime.strptime("08:00", "%H:%M").time()),
            datetime.combine(day, datetime.strptime("23:00", "%H:%M").time()),
            color='green', alpha=0.05
        )
    
    # --- Plot 2: Daily Averages ---
    plt.subplot(2, 1, 2)
    daily = df.resample('D').mean()
    for metric in ['likes', 'comments', 'shares']:
        plt.plot(daily.index, daily[metric], 
                label=metric.capitalize(), 
                marker='o', linewidth=2.5)
    
    top_days = daily_totals.nlargest(3).index  # Top 3 days
    for day in top_days:
        plt.axvline(day, color='red', linestyle='--', alpha=0.5)

    plt.title('Daily Average Engagement')
    plt.ylabel('Average Count')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Highlight dynamic peak day
    plt.axvline(peak_day, color='red', linestyle='--', alpha=0.5)
    plt.text(peak_day, plt.ylim()[1]*0.9, f' Peak Day ({peak_day.strftime("%Y-%m-%d")})', color='red')
    
    plt.tight_layout()
    plt.show()

# Usage
load_and_plot('trend prediction + forecasting models/data5/right_skewed_engagement.json')  # Replace with your JSON file