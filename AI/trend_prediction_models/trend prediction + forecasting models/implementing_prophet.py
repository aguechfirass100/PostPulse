import json
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# --- Load and prepare data ---
with open("data5/right_skewed_engagement.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df[['timestamp', 'likes']]
df.columns = ['ds', 'y']  # Prophet requires 'ds' and 'y'

# --- Split into train (7 days = 168 hours) and test (2 days = 48 hours) ---
train_df = df.iloc[:168]
test_df = df.iloc[168:216]  # Next 48 hours

# --- Train the Prophet model ---
model = Prophet()
model.fit(train_df)

# --- Forecast the next 48 hours ---
future = model.make_future_dataframe(periods=48, freq='H')
forecast = model.predict(future)
forecast['yhat'] = forecast['yhat'].apply(lambda x: max(0, x)) #added this because the forcast can have negative values 

# --- Merge forecast with test data ---
forecast_trimmed = forecast[['ds', 'yhat']].set_index('ds')
test_df.set_index('ds', inplace=True)
comparison = test_df.join(forecast_trimmed, how='left')

# --- Print first few comparisons ---
print(comparison[['y', 'yhat']].head(10))  # Real vs Forecasted likes

# --- Plot forecast vs actual ---
plt.figure(figsize=(12, 5))
plt.plot(comparison.index, comparison['y'], label='Actual Likes', marker='o')
plt.plot(comparison.index, comparison['yhat'], label='Forecasted Likes', linestyle='--')
plt.title('Prophet Forecast vs Actual (Likes)')
plt.xlabel('Time')
plt.ylabel('Likes')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
