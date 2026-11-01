import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from src.data_loader import load_dashboard_data
from src.ui_components import render_limitation_warning

# INLINE INSIGHT LOGIC TO FORCE HOT-RELOAD & CUSTOMIZE
def inline_generate_scatter_insight(corr_val, commodity, weather_var):
    strength = "weak"
    if abs(corr_val) > 0.2: strength = "moderate"
    if abs(corr_val) > 0.5: strength = "strong"
    
    direction = "positive" if corr_val > 0 else "negative"
    
    # Categorize crop
    comm_lower = commodity.lower()
    perishables = ['tomato', 'banana', 'green chilli', 'brinjal', 'bhindi (ladies finger)']
    tubers = ['onion', 'potato']
    grains = ['wheat', 'paddy', 'rice']
    
    crop_type = "general agricultural"
    if comm_lower in perishables: crop_type = "highly perishable"
    elif comm_lower in tubers: crop_type = "storage-dependent root/tuber"
    elif comm_lower in grains: crop_type = "staple grain"

    analysis = f"**Environmental Observational Analysis:** For **{commodity}**, the relationship with **{weather_var}** demonstrates a **{strength} {direction} correlation (r = {corr_val:.3f})**. "
    
    if weather_var == "avg_temp":
        if crop_type == "highly perishable":
            analysis += f"As a {crop_type} crop, {commodity} is extremely sensitive to heat stress. High temperatures drastically reduce shelf life, often forcing farmers into distress sales which can temporarily crash prices, followed by supply shortages that spike prices."
        elif crop_type == "storage-dependent root/tuber":
            analysis += f"For a {crop_type} like {commodity}, extreme ambient heat accelerates sprouting and rotting in uncooled warehouses, severely disrupting the market supply chain."
        else:
            analysis += f"Temperature fluctuations can signal transitions between harvest seasons for {commodity}, indirectly aligning with price shifts."
            
    elif weather_var == "rainfall":
        if crop_type == "highly perishable":
            analysis += f"Heavy rainfall is devastating for {crop_type} crops like {commodity}. It causes immediate physical damage to the harvest and blocks rural transport logistics, leading to massive sudden price spikes in urban markets."
        elif crop_type == "storage-dependent root/tuber":
            analysis += f"If rainfall occurs during the harvest window for {commodity}, the moisture significantly increases the risk of rot during long-term storage, altering the national pricing curve for months."
        elif crop_type == "staple grain":
            analysis += f"Unseasonal rainfall during the harvest window can ruin standing {commodity} crops, though national buffer stocks usually stabilize extreme price shocks."
        else:
            analysis += "Rainfall generally disrupts physical market operations and transport logistics, causing short-term pricing volatility."
            
    elif weather_var == "wind_speed":
        analysis += f"High wind speeds (and associated cyclonic activity) can cause physical crop lodging for {commodity} or disrupt regional transport hubs, though the direct linear correlation with price is usually weak."

    analysis += "\n\n**Crucial Limitation:** This is strictly an observational association. Weather anomalies may coincide with seasonal harvest cycles rather than directly causing daily price fluctuations."
    return analysis

def inline_generate_timeline_insight(df, commodity, weather_var):
    price_vol = df["Modal_Price"].std() / df["Modal_Price"].mean() * 100
    weather_vol = df[weather_var].std() / df[weather_var].mean() * 100
    
    insight = f"**Timeline Analysis:** Over the course of 2024, the median price of **{commodity}** exhibited a relative volatility of **{price_vol:.1f}%**, while **{weather_var}** exhibited **{weather_vol:.1f}%** volatility. "
    
    insight += "Visual inspection of the timelines reveals whether seasonal weather shifts align with macro pricing trends. "
    
    if weather_var == "avg_temp":
        insight += f"For example, observe the summer peak (May-June). For {commodity}, extreme heat often correlates with the lowest point of cold-storage reserves or the destruction of perishable standing crops, leading to delayed pricing ripples."
    elif weather_var == "rainfall":
        insight += f"For {commodity}, track the monsoon months (July-September). Sharp spikes in rainfall often immediately precede market price volatility as rural logistics are severed and harvest quality degrades."
    elif weather_var == "wind_speed":
        insight += f"Trace the timeline to see if major wind anomalies (storm systems) line up with sudden, short-lived price shocks for {commodity}."
        
    return insight

st.title("Weather & Price Association")
st.write("Explore observational relationships between nearest-station weather metrics and market prices.")

render_limitation_warning()

@st.cache_data
def get_weather_data_sample():
    df = load_dashboard_data()
    return df[["Commodity", "Modal_Price", "avg_temp", "rainfall", "wind_speed", "distance_km", "Arrival_Date"]]

with st.spinner("Loading data..."):
    df = get_weather_data_sample()

st.sidebar.subheader("Filter Settings")
commodities = df["Commodity"].value_counts().head(50).index.tolist()
selected_comm = st.sidebar.selectbox("Select Commodity (Top 50)", commodities)

weather_var = st.sidebar.selectbox("Weather Variable", ["avg_temp", "rainfall", "wind_speed"])

# Filter for the selected commodity
filtered_df = df[df["Commodity"] == selected_comm].dropna(subset=[weather_var, "Modal_Price"]).copy()

# Sample down for the scatter plot if too large
if len(filtered_df) > 5000:
    plot_df = filtered_df.sample(5000, random_state=42)
else:
    plot_df = filtered_df

st.subheader(f"Price vs {weather_var} for {selected_comm}")
fig = px.scatter(plot_df, x=weather_var, y="Modal_Price", opacity=0.5, 
                 trendline="ols",
                 title=f"{selected_comm}: Modal Price vs {weather_var}")
st.plotly_chart(fig, use_container_width=True)

# Generate insight based on correlation
corr = plot_df[[weather_var, "Modal_Price"]].corr().iloc[0, 1]
with st.expander("Insights", expanded=True):
    st.info(inline_generate_scatter_insight(corr, selected_comm, weather_var))

st.divider()

# Historical Price Trend with Weather
st.subheader(f"Historical Timeline: Price & {weather_var}")
st.write("Compare the daily aggregate price fluctuations against the corresponding weather patterns over the year 2024.")

# Group by date for a cleaner timeline
timeline_df = filtered_df.groupby("Arrival_Date").agg({
    "Modal_Price": "median",
    weather_var: "mean"
}).reset_index().sort_values("Arrival_Date")

# Create a figure with a secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add Price trace
fig2.add_trace(
    go.Scatter(x=timeline_df["Arrival_Date"], y=timeline_df["Modal_Price"], 
               name="Median Modal Price (₹)", line=dict(color="blue", width=2)),
    secondary_y=False,
)

# Add Weather trace
weather_color = "red" if weather_var == "avg_temp" else ("teal" if weather_var == "rainfall" else "orange")
fig2.add_trace(
    go.Scatter(x=timeline_df["Arrival_Date"], y=timeline_df[weather_var], 
               name=f"Mean {weather_var}", line=dict(color=weather_color, width=2, dash="dot"), opacity=0.7),
    secondary_y=True,
)

# Set up axes layout
fig2.update_layout(
    title_text=f"2024 Timeline: {selected_comm} Price vs {weather_var}",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig2.update_yaxes(title_text="<b>Modal Price (₹)</b>", secondary_y=False, color="blue")
fig2.update_yaxes(title_text=f"<b>{weather_var}</b>", secondary_y=True, color=weather_color)

st.plotly_chart(fig2, use_container_width=True)

with st.expander("Insights", expanded=True):
    st.info(inline_generate_timeline_insight(timeline_df, selected_comm, weather_var))

