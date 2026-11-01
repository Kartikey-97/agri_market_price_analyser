import streamlit as st
from src.data_loader import load_dashboard_data

st.title("Data Explorer")
st.write("Browse the underlying cleaned 2024 historical dataset.")

# Use caching and avoid loading everything if possible, but load_dashboard_data loads the dataframe
with st.spinner("Loading 4.7M rows dataset..."):
    df = load_dashboard_data()

st.sidebar.subheader("Filter Data")
state = st.sidebar.selectbox("State", ["All"] + list(df["State"].unique()))

if state != "All":
    filtered_df = df[df["State"] == state]
    district = st.sidebar.selectbox("District", ["All"] + list(filtered_df["District"].unique()))
    if district != "All":
        filtered_df = filtered_df[filtered_df["District"] == district]
        market = st.sidebar.selectbox("Market", ["All"] + list(filtered_df["Market"].unique()))
        if market != "All":
            filtered_df = filtered_df[filtered_df["Market"] == market]
            commodity = st.sidebar.selectbox("Commodity", ["All"] + list(filtered_df["Commodity"].unique()))
            if commodity != "All":
                filtered_df = filtered_df[filtered_df["Commodity"] == commodity]
else:
    filtered_df = df

st.subheader(f"Data Preview ({len(filtered_df):,} records)")
# Display only top 1000 to prevent browser crash
st.dataframe(filtered_df.head(1000), use_container_width=True)

if len(filtered_df) > 1000:
    st.info("Displaying the top 1000 rows only to optimize performance.")
