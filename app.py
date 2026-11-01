import streamlit as st

st.set_page_config(
    page_title="Agricultural Market Price Analyser",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("Market Analyser")
    st.sidebar.markdown("Historical Market Intelligence & Next-Day Price Forecasting")
    
    pages = {
        "Analytics": [
            st.Page("src/pages/1_Overview.py", title="Overview"),
            st.Page("src/pages/2_Market_Analysis.py", title="Market Analysis"),
            st.Page("src/pages/3_Commodity_Analysis.py", title="Commodity Analysis"),
            st.Page("src/pages/4_Weather_Price.py", title="Weather & Price"),
            st.Page("src/pages/7_Data_Explorer.py", title="Data Explorer"),
        ],
        "Machine Learning": [
            st.Page("src/pages/5_Price_Forecast.py", title="Price Forecast"),
            st.Page("src/pages/6_Model_Performance.py", title="Model Performance"),
        ]
    }
    
    pg = st.navigation(pages)
    pg.run()
    
    st.sidebar.divider()
    st.sidebar.caption("Data Scope: Calendar Year 2024")

if __name__ == "__main__":
    main()
