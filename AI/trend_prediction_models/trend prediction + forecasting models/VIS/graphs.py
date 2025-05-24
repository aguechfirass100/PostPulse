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
    
    plt.title('Daily Average Engagement')
    plt.ylabel('Average Count')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.style.use('seaborn-v0_8-darkgrid')  # Add this before plotting
    
    # Highlight peak day (Day 3)
    peak_day = df.index[0] + pd.Timedelta(days=2)
    plt.axvline(peak_day, color='red', linestyle='--', alpha=0.5)
    plt.text(peak_day, plt.ylim()[1]*0.9, ' Peak Day', color='red')
    
    plt.tight_layout()
    plt.show()

# Usage
load_and_plot('trend prediction + forecasting models/data1/Noisy_Data.json')  # Replace with your JSON file
