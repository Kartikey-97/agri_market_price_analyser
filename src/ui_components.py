import streamlit as st

def render_limitation_warning():
    st.warning("""
    **Project Limitations & Methodology**:
    * **2024 Data Only:** The dataset and models are restricted to calendar year 2024.
    * **Nearest-Station Weather:** Weather values are assigned from the nearest available weather station (avg distance ~35km), not observed directly at the mandi.
    * **Correlation is not Causation:** Associations between weather and price are observational.
    * **Not a Production Trading System:** This is an academic analytical model. It does not provide agricultural advice on crops to plant, nor guarantees future income.
    """)
