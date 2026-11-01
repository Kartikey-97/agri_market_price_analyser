import streamlit as st
import joblib
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
import os

@st.cache_resource
def load_linear_model():
    model = joblib.load("models/linear_model.joblib")
    preprocessor = joblib.load("models/linear_preprocessor.joblib")
    return model, preprocessor

@st.cache_resource
def load_random_forest_model():
    model = joblib.load("models/random_forest_model.joblib")
    preprocessor = joblib.load("models/random_forest_preprocessor.joblib")
    return model, preprocessor

@st.cache_resource
def load_xgboost_model():
    model = XGBRegressor()
    model.load_model("models/xgboost_model.json")
    categories = joblib.load("models/xgboost_categories.joblib")
    return model, categories

@st.cache_resource
def load_catboost_model():
    model = CatBoostRegressor()
    model.load_model("models/catboost_model.cbm")
    return model
