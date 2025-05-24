# Trend Prediction Models for PostPulse

This directory contains the implementation of trend prediction models for the PostPulse marketing platform. These models analyze historical engagement data to forecast future post performance and provide insights for content planning.

## Overview

PostPulse's trend prediction capabilities include:
- Forecasting future engagement metrics (likes, comments, shares)
- Identifying optimal posting times
- Detecting emerging trends in audience behavior
- Providing actionable insights for content strategy optimization

## Model Selection

We selected Facebook's (Meta's) Prophet as our primary forecasting model:

### Primary Model: Prophet
- **Developer**: Facebook (Meta)
- **Model Type**: Additive time-series forecasting model
- **Formula**: y(t) = g(t) + s(t) + h(t) + ε<sub>t</sub>
  - g(t): trend component
  - s(t): seasonality component
  - h(t): holidays/events component
  - ε<sub>t</sub>: error term
- **Key Strengths**:
  - No fine-tuning required
  - Handles missing data and outliers automatically
  - Captures both linear and non-linear trends
  - Resistant to over-generalization
  - Simple Python API for integration
  - Highly interpretable components

## Inference Workflow

### Data Preparation
- Aggregate post performance metrics (likes, comments, shares) into daily time series
- Rename and format columns to Prophet's expected schema (ds for date, y for values)

### Model Initialization & Fitting
- Instantiate Prophet with default settings to capture trend and seasonality
- Fit the model on prepared historical data

### Forecast Generation
- Specify a 5-day forecasting horizon
- Generate future dates and compute corresponding forecasts

### Post-Processing
- Extract predicted values (yhat) for the 5-day window
- Clip negative forecasts to zero to maintain interpretability

## Evaluation Metrics

- **Mean Absolute Error (MAE)**: 92
- **Root Mean Squared Error (RMSE)**: 124
- **Interpretation**: Errors remained below typical daily volatility, indicating reliable forecasts for content planning

## Data Collection Strategy

Since our platform generates unique engagement patterns, we implemented a two-phase approach:

1. **Initial Phase**: Rule-based system to analyze engagement metrics (likes, shares, comments) in real-time
2. **Ongoing Collection**: Store engagement data for each post, building a custom dataset over time
3. **Model Evolution**: As sufficient data accumulates, the model becomes increasingly tailored to our platform's specific audience behaviors

## API Endpoint

```
POST /predict-trend
```

### Request Parameters

```json
{
  "post_id": "post_12345",
  "historical_data": [
    {"date": "2025-05-10", "likes": 120, "comments": 15, "shares": 8},
    {"date": "2025-05-11", "likes": 150, "comments": 22, "shares": 12},
    {"date": "2025-05-12", "likes": 135, "comments": 18, "shares": 10},
    {"date": "2025-05-13", "likes": 160, "comments": 25, "shares": 14},
    {"date": "2025-05-14", "likes": 180, "comments": 30, "shares": 20}
  ],
  "forecast_days": 5,
  "metrics": ["likes", "comments", "shares"]
}
```

### Response

```json
{
  "post_id": "post_12345",
  "forecasts": {
    "likes": [
      {"date": "2025-05-15", "value": 195, "lower_bound": 175, "upper_bound": 215},
      {"date": "2025-05-16", "value": 210, "lower_bound": 185, "upper_bound": 235},
      {"date": "2025-05-17", "value": 205, "lower_bound": 180, "upper_bound": 230},
      {"date": "2025-05-18", "value": 225, "lower_bound": 200, "upper_bound": 250},
      {"date": "2025-05-19", "value": 240, "lower_bound": 215, "upper_bound": 265}
    ],
    "comments": [
      {"date": "2025-05-15", "value": 32, "lower_bound": 28, "upper_bound": 36},
      {"date": "2025-05-16", "value": 35, "lower_bound": 30, "upper_bound": 40},
      {"date": "2025-05-17", "value": 33, "lower_bound": 28, "upper_bound": 38},
      {"date": "2025-05-18", "value": 38, "lower_bound": 33, "upper_bound": 43},
      {"date": "2025-05-19", "value": 42, "lower_bound": 37, "upper_bound": 47}
    ],
    "shares": [
      {"date": "2025-05-15", "value": 22, "lower_bound": 18, "upper_bound": 26},
      {"date": "2025-05-16", "value": 25, "lower_bound": 20, "upper_bound": 30},
      {"date": "2025-05-17", "value": 23, "lower_bound": 19, "upper_bound": 27},
      {"date": "2025-05-18", "value": 27, "lower_bound": 22, "upper_bound": 32},
      {"date": "2025-05-19", "value": 30, "lower_bound": 25, "upper_bound": 35}
    ]
  },
  "trend_insights": {
    "overall_trend": "upward",
    "peak_engagement_day": "2025-05-19",
    "growth_rate": "+33% over forecast period"
  }
}
```

## Deployment

Currently deployed via Google Colab Pro with L4 GPU instances (though Prophet is CPU-based) and exposed through ngrok tunnels for API access.

## Visualizations

The trend predictions power several dashboard visualizations:
- 30-day engagement forecast charts
- Day-of-week performance heatmaps
- Anomaly detection alerts when performance deviates significantly from predictions

## Future Improvements

- Incorporate external factors (holidays, events, industry news)
- Develop platform-specific seasonality patterns
- Add competitive analysis for benchmarking
- Implement automated content scheduling based on predicted optimal times