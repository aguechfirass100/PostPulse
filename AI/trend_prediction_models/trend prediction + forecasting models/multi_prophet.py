import json
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from matplotlib.backends.backend_pdf import PdfPages
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Configuration ---
DATA_FILES = [
    "trend prediction + forecasting models/data1/Noisy_Data.json",
    "trend prediction + forecasting models/data3/Daily_activity_cycle.json",
    "trend prediction + forecasting models/data4/realistic_data.json",
    "trend prediction + forecasting models/data5/right_skewed_engagement.json"
]
METRIC = 'likes'  # Change to 'comments' or 'shares' if needed
TRAIN_HOURS = 168  # 7 days of training
TEST_HOURS = 48    # 2 days of testing

# Create PDF report
pdf = PdfPages('prophet_forecast_report.pdf')

# Create Plotly figure
plotly_fig = make_subplots(
    rows=len(DATA_FILES), 
    cols=1,
    subplot_titles=[f.split("/")[-1] for f in DATA_FILES],
    vertical_spacing=0.1
)

for i, file in enumerate(DATA_FILES, 1):
    # --- Load Data ---
    with open(file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[['timestamp', METRIC]].rename(columns={'timestamp': 'ds', METRIC: 'y'})
    
    # --- Split Train/Test ---
    train_df = df.iloc[:TRAIN_HOURS]
    test_df = df.iloc[TRAIN_HOURS:TRAIN_HOURS+TEST_HOURS]
    
    # --- Train Model ---
    model = Prophet(interval_width=0.95)
    model.fit(train_df)
    
    # --- Forecast ---
    future = model.make_future_dataframe(periods=TEST_HOURS, freq='h')
    forecast = model.predict(future)
    forecast['yhat'] = forecast['yhat'].clip(lower=0)
    
    # --- Merge Results ---
    forecast_trimmed = forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']]
    test_df.set_index('ds', inplace=True)
    comparison = test_df.join(forecast_trimmed, how='left')
    
    # --- Calculate Error Metrics ---
    mae = mean_absolute_error(comparison['y'], comparison['yhat'])
    rmse = np.sqrt(mean_squared_error(comparison['y'], comparison['yhat']))
    
    # --- Matplotlib Plot (for PDF) ---
    plt.figure(figsize=(15, 6))
    plt.plot(comparison.index, comparison['y'], label='Actual', color='blue', marker='o', markersize=4)
    plt.plot(comparison.index, comparison['yhat'], label='Forecast', color='red', linestyle='--')
    plt.fill_between(
        comparison.index,
        comparison['yhat_lower'],
        comparison['yhat_upper'],
        color='pink',
        alpha=0.3,
        label='95% CI'
    )
    plt.title(f'{file.split("/")[-1]}\nMAE: {mae:.2f}, RMSE: {rmse:.2f}', pad=20)
    plt.xlabel('Time')
    plt.ylabel(METRIC.capitalize())
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    pdf.savefig()
    plt.close()
    
    # --- Add to Plotly Figure ---
    plotly_fig.add_trace(
        go.Scatter(
            x=comparison.index,
            y=comparison['y'],
            name='Actual',
            mode='lines+markers',
            marker=dict(size=4)
        ),
        row=i, col=1
    )
    plotly_fig.add_trace(
        go.Scatter(
            x=comparison.index,
            y=comparison['yhat'],
            name='Forecast',
            line=dict(dash='dash')
        ),
        row=i, col=1
    )
    plotly_fig.add_trace(
        go.Scatter(
            x=comparison.index,
            y=comparison['yhat_upper'],
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ),
        row=i, col=1
    )
    plotly_fig.add_trace(
        go.Scatter(
            x=comparison.index,
            y=comparison['yhat_lower'],
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(255, 182, 193, 0.3)',
            name='95% CI'
        ),
        row=i, col=1
    )
    
    # Add error metrics to subplot title
    plotly_fig.layout.annotations[i-1].text += f" (MAE: {mae:.2f}, RMSE: {rmse:.2f})"

pdf.close()

# Configure Plotly layout
plotly_fig.update_layout(
    height=1000,
    title_text=f"Prophet Forecast Comparison - {METRIC.capitalize()}",
    hovermode="x unified"
)

# Save and show Plotly figure
plotly_fig.write_html("prophet_forecast_interactive.html")
print("Report generated: prophet_forecast_report.pdf")
print("Interactive visualization saved: prophet_forecast_interactive.html")

# To display in Jupyter notebook:
# plotly_fig.show()