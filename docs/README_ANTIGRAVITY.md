
# Agricultural Market Price Analyser
## Antigravity Development Brief

Build a professional Streamlit dashboard for an academic Data Science
project called **Agricultural Market Price Analyser**.

The dashboard must look like a polished production-style analytics
application rather than a basic college demo.

---

# 1. PROJECT PURPOSE

The application analyzes agricultural mandi market prices in India and
explores relationships between market prices, commodities, locations,
seasonality and weather.

The application should provide:

- Historical price analysis
- Commodity analysis
- State / district / market comparisons
- Weather-price relationship analysis
- Interactive charts
- Next-day price prediction
- Model-performance comparison
- Data exploration

---

# 2. DATA

Primary file:

data/dashboard_data.parquet

Dataset:

- 2024 calendar year
- 4.7M+ cleaned market-price observations
- 28 states/regions represented in the final cleaned data
- ~2,700+ markets
- 300+ commodities

Important:

The dataset is HISTORICAL and covers 2024.

Do not describe the application as a live real-time market feed.

Use wording such as:

"Historical Market Intelligence & Price Forecasting"

rather than claiming live prices.

---

# 3. CORE DATA COLUMNS

Market:

State
District
Market
Commodity
Variety
Grade
Arrival_Date

Price:

Min_Price
Max_Price
Modal_Price

Weather:

avg_temp
min_temp
max_temp
wind_speed
air_pressure
rainfall

Location / weather station:

nearest_station
station_latitude
station_longitude
distance_km

---

# 4. MODEL FILES

Models:

models/linear_model.joblib
models/linear_preprocessor.joblib

models/random_forest_model.joblib
models/random_forest_preprocessor.joblib

models/xgboost_model.json
models/xgboost_categories.joblib

models/catboost_model.cbm

Model comparison:

metadata/model_comparison.csv

---

# 5. MODEL RESULTS

Validation results:

Naive Baseline
MAE: ₹265.21
RMSE: ₹1,078.26
R²: 0.9651

Linear Regression
MAE: ₹296.72
RMSE: ₹1,051.04
R²: 0.9668

Random Forest
MAE: ₹360.40
RMSE: ₹1,332.63
R²: 0.9467

XGBoost
MAE: ₹347.73
RMSE: ₹1,561.90
R²: 0.9268

CatBoost
MAE: ₹346.06
RMSE: ₹1,624.56
R²: 0.9208

Use these values exactly in the Model Performance page.

Do not fabricate additional metrics.

---

# 6. TARGET DEFINITION

The supervised-learning target is:

"Next calendar day's Modal_Price for the same
State + District + Market + Commodity + Variety + Grade series."

Only rows where the next calendar day is actually observed were used
for supervised training.

Therefore the model is a NEXT-DAY forecasting model.

---

# 7. FEATURES USED BY THE MODELS

Categorical:

State
District
Market
Commodity
Variety
Grade

Numeric:

Modal_Price
lag1_price
price_change_1d
avg_temp
min_temp
max_temp
wind_speed
air_pressure
rainfall
distance_km
month
day_of_week

The dashboard predictor must construct the same feature schema.

---

# 8. MODEL INPUT LOGIC

For a selected market/commodity/variety/grade series:

Retrieve the latest available observation.

Use:

- Current modal price
- Previous-day modal price where available
- One-day price change
- Weather features
- Location/weather-station distance
- Month
- Day of week
- State / District / Market / Commodity / Variety / Grade

Then construct the model input using the exact feature order expected
by the corresponding model.

For Linear Regression and Random Forest:

Load the corresponding preprocessor first, then transform the feature
frame before calling predict().

For XGBoost:

Preserve the categorical feature schema saved in
xgboost_categories.joblib.

For CatBoost:

Convert categorical features to strings consistently.

---

# 9. NAIVE FORECAST

Implement the naive benchmark:

predicted_next_day_price = current_modal_price

Display it alongside the ML prediction.

This is important because the naive baseline was very strong.

---

# 10. DASHBOARD STRUCTURE

Create a polished sidebar/navigation structure such as:

1. Overview
2. Market Analysis
3. Commodity Analysis
4. Weather & Price
5. Price Forecast
6. Model Performance
7. Data Explorer

---

# 11. OVERVIEW PAGE

Show KPI cards:

- Total records
- Number of states
- Number of districts
- Number of markets
- Number of commodities
- 2024 date range

Charts:

- Monthly median modal price
- Monthly average modal price
- Price distribution
- State-level market activity

Use Plotly for interactive charts.

---

# 12. MARKET ANALYSIS

Sidebar filters:

State
District
Market
Commodity
Variety
Grade
Date range

Main charts:

- Historical Modal Price line chart
- Min vs Modal vs Max price
- Monthly price trend
- Price distribution

Use interactive Plotly charts with hover information.

---

# 13. COMMODITY ANALYSIS

Allow the user to select a commodity.

Show:

- Average price
- Median price
- Lowest price
- Highest price
- Number of observations
- Number of markets

Charts:

- Monthly commodity price
- State-wise commodity prices
- Market comparison
- Price distribution

---

# 14. WEATHER & PRICE

Show the relationship between price and:

- Average temperature
- Maximum temperature
- Minimum temperature
- Rainfall
- Wind speed

Recommended visuals:

- Scatter plot
- Correlation matrix
- Price vs rainfall
- Price vs temperature
- Monthly weather + price comparison

Use selected commodity/market filters.

Remember:

Correlation should be described as association, not causation.

---

# 15. PRICE FORECAST PAGE

This is the most important interactive feature.

Controls:

State
District
Market
Commodity
Variety
Grade
Model

Show:

Current Modal Price
Previous Modal Price
Recent change
Weather context
Selected model

Then display:

"Predicted Next-Day Modal Price"

Also display:

Naive prediction
ML prediction
Difference between naive and ML

Example layout:

CURRENT PRICE
₹3,500

NAIVE NEXT-DAY
₹3,500

MODEL PREDICTION
₹3,620

CHANGE
+₹120 / +3.43%

Include a clear note:

"Prediction is an academic model estimate based on historical
2024 data and should not be interpreted as a guaranteed market price."

---

# 16. HISTORICAL FORECAST DEMO

Because ground-truth future data is only available inside the historical
2024 dataset, provide an optional mode where users can select a historical
date and evaluate a next-day prediction against the actual next-day price.

This allows:

Predicted Price
Actual Price
Absolute Error

and an interactive prediction-vs-actual chart.

This is preferable to pretending the historical-only dataset is a live
production forecasting system.

---

# 17. MODEL PERFORMANCE PAGE

Show:

- Metric comparison table
- MAE comparison
- RMSE comparison
- R² comparison

Use bar charts or clean Plotly visualizations.

Explain:

MAE = average absolute prediction error in ₹.

RMSE penalizes larger errors more heavily.

R² indicates how much variance is explained relative to the baseline
definition used by the metric.

Also clearly show the training/validation periods:

Training:
2024-01-01 → 2024-09-30

Validation:
2024-10-01 → 2024-11-30

Test:
2024-12-01 → 2024-12-30

---

# 18. DATA EXPLORER

Interactive filters.

Show:

- filtered data table
- record count
- summary statistics
- downloadable CSV for filtered results

Do not attempt to render all 4.7M rows at once.

Use sampling/pagination/limited display.

---

# 19. DESIGN REQUIREMENTS

Make the UI look professional.

Suggested design:

- clean modern dashboard
- responsive layout
- wide desktop layout
- consistent spacing
- KPI cards
- Plotly charts
- clear typography
- restrained color usage
- polished sidebar
- meaningful section headers
- good empty/error states
- loading indicators where necessary

Do not make it look like a generic Streamlit template.

Avoid unnecessary decorative elements.

---

# 20. PERFORMANCE REQUIREMENTS

The full parquet contains millions of rows.

Use Streamlit caching:

@st.cache_data

and:

@st.cache_resource

for model loading.

Never repeatedly load the model or parquet file on every widget change.

Avoid displaying the entire dataset.

Use filtered operations and aggregation before charting.

Where useful, use precomputed files:

data/monthly_summary.csv
data/state_summary.csv
data/commodity_summary.csv
data/market_summary.csv
data/series_latest.parquet

---

# 21. FILE STRUCTURE

Expected final application structure:

agri_market_price_analyser/
│
├── app.py
├── requirements.txt
│
├── models/
│   ├── linear_model.joblib
│   ├── linear_preprocessor.joblib
│   ├── random_forest_model.joblib
│   ├── random_forest_preprocessor.joblib
│   ├── xgboost_model.json
│   ├── xgboost_categories.joblib
│   └── catboost_model.cbm
│
├── data/
│   ├── dashboard_data.parquet
│   ├── series_latest.parquet
│   ├── monthly_summary.csv
│   ├── state_summary.csv
│   ├── commodity_summary.csv
│   └── market_summary.csv
│
├── metadata/
│   ├── feature_config.json
│   ├── dataset_metadata.json
│   ├── model_comparison.csv
│   ├── commodity_lookup.csv
│   ├── location_lookup.csv
│   └── environment_versions.txt
│
└── docs/
    └── (additional project documentation if needed)

---

# 22. IMPORTANT LIMITATIONS

The dashboard should transparently mention:

1. Dataset is limited to 2024.
2. Weather data is historical.
3. Weather-station matching uses nearest available station rather than
   direct weather measurements at every mandi.
4. Some locations are relatively far from their assigned station.
5. The supervised target only includes series with an observed next-day
   price.
6. A future forecast beyond the historical period requires appropriate
   future input features, particularly weather.
7. Predictions are estimates and not guaranteed market prices.

---

# 23. DO NOT DO

Do not:

- claim live mandi prices
- claim guaranteed forecasts
- fabricate future weather
- invent model metrics
- invent feature importance
- invent accuracy percentages
- call correlation causation
- silently change the model's input feature schema

---

# 24. FINAL GOAL

The finished application should feel like a professional agricultural
market intelligence dashboard suitable for demonstrating:

Data Science
Machine Learning
Time-series forecasting
Exploratory Data Analysis
Weather-price analysis
Interactive visualization
Model evaluation

The application should be visually impressive while remaining
technically faithful to the supplied dataset and trained models.
