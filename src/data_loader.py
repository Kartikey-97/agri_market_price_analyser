import pandas as pd
import streamlit as st
import json

@st.cache_data
def load_monthly_summary():
    return pd.read_csv("data/monthly_summary.csv")

@st.cache_data
def load_state_summary():
    return pd.read_csv("data/state_summary.csv")

@st.cache_data
def load_commodity_summary():
    return pd.read_csv("data/commodity_summary.csv")

@st.cache_data
def load_market_summary():
    return pd.read_csv("data/market_summary.csv")

@st.cache_data
def load_series_latest():
    return pd.read_parquet("data/series_latest.parquet")

@st.cache_data
def load_dashboard_data():
    return pd.read_parquet("data/dashboard_data.parquet")

@st.cache_data
def load_model_comparison():
    return pd.read_csv("metadata/model_comparison.csv")

@st.cache_data
def load_feature_config():
    with open("metadata/feature_config.json", "r") as f:
        return json.load(f)
