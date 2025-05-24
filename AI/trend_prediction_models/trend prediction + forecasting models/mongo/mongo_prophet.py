from pymongo import MongoClient
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# --- Select the metric to forecast ---
metric = "shares"  # Change to 'comments' or 'shares' as needed

# --- MongoDB Connection ---
client = MongoClient("mongodb://localhost:27017")
db = client['engagementSim']
collection = db['postMetrics']

# --- Load data from MongoDB ---
cursor = collection.find({}, {"_id": 0, "timestamp": 1, metric: 1})
data = list(cursor)

# Convert to DataFrame
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.rename(columns={"timestamp": "ds", metric: "y"})

# --- Use only first 7 days for training ---
df = df.sort_values('ds')

# --- Split into train (7 days = 168 hours) and test (2 days = 48 hours) ---
train_df = df.iloc[:168]
test_df = df.iloc[168:216]

# --- Train the Prophet model ---
model = Prophet()
model.fit(train_df)

# --- Forecast the next 48 hours ---
future = model.make_future_dataframe(periods=48, freq='H')
forecast = model.predict(future)
forecast['yhat'] = forecast['yhat'].apply(lambda x: max(0, x))


# --- Merge forecast with test data ---
forecast_trimmed = forecast[['ds', 'yhat']].set_index('ds')
test_df.set_index('ds', inplace=True)
comparison = test_df.join(forecast_trimmed, how='left')

# --- Print first few comparisons ---
print(comparison[['y', 'yhat']].head(10))  # Real vs Forecasted

# --- Plot forecast vs actual ---
plt.figure(figsize=(12, 5))
plt.plot(comparison.index, comparison['y'], label=f'Actual {metric.capitalize()}', marker='o')
plt.plot(comparison.index, comparison['yhat'], label=f'Forecasted {metric.capitalize()}', linestyle='--')
plt.title(f'Prophet Forecast vs Actual ({metric.capitalize()})')
plt.xlabel('Time')
plt.ylabel(metric.capitalize())
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
