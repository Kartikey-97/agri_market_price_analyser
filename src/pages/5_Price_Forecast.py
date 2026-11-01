import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from src.data_loader import load_feature_config, load_dashboard_data
from src.model_loader import load_linear_model
from src.ui_components import render_limitation_warning

st.title("Next-Day & 7-Day Future Price Forecast")
st.write("Simulate future agricultural prices and analyze predicted trends.")

render_limitation_warning()
st.info("This tool simulates a live forecast by projecting 7 days into the future starting from **Today**. Because this is a 2024 dataset, it uses the features from the most recent historical record as the starting point for today's projection.")

with st.spinner("Loading complete series data..."):
    config = load_feature_config()
    df_all = load_dashboard_data()

st.sidebar.subheader("Select Series")
# Hierarchical filtering
state = st.sidebar.selectbox("State", df_all["State"].unique())
filtered1 = df_all[df_all["State"] == state]

district = st.sidebar.selectbox("District", filtered1["District"].unique())
filtered2 = filtered1[filtered1["District"] == district]

market = st.sidebar.selectbox("Market", filtered2["Market"].unique())
filtered3 = filtered2[filtered2["Market"] == market]

commodity = st.sidebar.selectbox("Commodity", filtered3["Commodity"].unique())
filtered4 = filtered3[filtered3["Commodity"] == commodity]

variety = st.sidebar.selectbox("Variety", filtered4["Variety"].unique())
filtered5 = filtered4[filtered4["Variety"] == variety]

grade = st.sidebar.selectbox("Grade", filtered5["Grade"].unique())
final_series = filtered5[filtered5["Grade"] == grade].sort_values("Arrival_Date").reset_index(drop=True)

if final_series.empty:
    st.error("Series not found.")
else:
    # Always use the latest record for the features
    target_idx = len(final_series) - 1
    row = final_series.iloc[target_idx].to_dict()
    current_price = row["Modal_Price"]
    
    # Anchor the simulation to REAL WORLD TODAY
    today = datetime.now().date()
    
    st.subheader(f"Live Future Projection for {commodity} in {market}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Current Price (as of {today})", f"₹{current_price:,.2f}")
    
    # Check for lag1_price (previous day)
    lag_found = False
    if target_idx > 0:
        prev_row = final_series.iloc[target_idx - 1]
        if (pd.to_datetime(row["Arrival_Date"]) - pd.to_datetime(prev_row["Arrival_Date"])).days == 1:
            row["lag1_price"] = prev_row["Modal_Price"]
            row["price_change_1d"] = row["Modal_Price"] - row["lag1_price"]
            lag_found = True
            
    if not lag_found:
        row["lag1_price"] = current_price
        row["price_change_1d"] = 0.0
        
    features = config["all_model_features"]
    
    # 7-Day Recursive Forecast
    predictions = []
    dates = []
    
    current_sim_row = row.copy()
    
    try:
        model, preprocessor = load_linear_model()
        
        for i in range(1, 8):
            future_date = today + pd.Timedelta(days=i)
            dates.append(future_date)
            
            # Update temporal features to match the SIMULATED future dates
            current_sim_row["month"] = future_date.month
            current_sim_row["day_of_week"] = future_date.weekday()
            
            X_pred = pd.DataFrame([current_sim_row])[features]
            X_transformed = preprocessor.transform(X_pred)
            pred = model.predict(X_transformed)[0]
            predictions.append(pred)
            
            # Update lag features for the NEXT iteration
            current_sim_row["price_change_1d"] = pred - current_sim_row["lag1_price"]
            current_sim_row["lag1_price"] = pred
            current_sim_row["Modal_Price"] = pred # Though target isn't used as input for tomorrow, just keeping it consistent
            
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")

    if predictions:
        next_day_pred = predictions[0]
        day7_pred = predictions[-1]
        
        diff_1d = next_day_pred - current_price
        pct_1d = (diff_1d / current_price) * 100 if current_price > 0 else 0
        col2.metric("Tomorrow's Prediction", f"₹{next_day_pred:,.2f}", f"{diff_1d:,.2f} ({pct_1d:.2f}%)")
        
        diff_7d = day7_pred - current_price
        pct_7d = (diff_7d / current_price) * 100 if current_price > 0 else 0
        col3.metric("7-Day Forecast", f"₹{day7_pred:,.2f}", f"{diff_7d:,.2f} ({pct_7d:.2f}%)")
        
        st.divider()
        
        # Plotting the 7-day projection
        st.subheader("7-Day Projected Price Trend")
        plot_df = pd.DataFrame({
            "Date": [today] + dates,
            "Price": [current_price] + predictions,
            "Type": ["Actual (Current)"] + ["Predicted"] * 7
        })
        
        fig = px.line(plot_df, x="Date", y="Price", markers=True, title=f"Predicted Future Trend for {commodity}")
        fig.add_scatter(x=[plot_df["Date"].iloc[0]], y=[plot_df["Price"].iloc[0]], mode='markers', marker=dict(size=12, color="red"), name="Current Price")
        st.plotly_chart(fig, use_container_width=True)
        
        # Automated AI-like Insight Analysis
        trend = "upward" if day7_pred > current_price else "downward"
        magnitude = abs(pct_7d)
        
        if magnitude < 0.5:
            analysis = f"The price for **{commodity}** is predicted to remain relatively **stable** over the next 7 days, ending near ₹{day7_pred:,.2f}. The linear regression model indicates that current market momentum and localized weather conditions are not strong enough to force a major price breakout."
        elif trend == "upward":
            analysis = f"The forecast indicates an **upward trend** of **+{magnitude:.1f}%** over the next week, reaching ₹{day7_pred:,.2f} by {dates[-1].strftime('%B %d')}. This projected increase is driven by positive recent price momentum and historical weather variable baselines associated with higher market prices."
        else:
            analysis = f"The forecast indicates a **downward trend** of **-{magnitude:.1f}%** over the next week, dropping to ₹{day7_pred:,.2f} by {dates[-1].strftime('%B %d')}. This decrease suggests that the current price is facing negative momentum or correction, factored in by the model's lag features and local environmental conditions."
            
        with st.expander('Insights', expanded=True):
            st.markdown(analysis)
