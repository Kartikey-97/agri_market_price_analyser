import streamlit as st
import plotly.express as px
from src.data_loader import load_commodity_summary

def inline_generate_commodity_insight(df_price):
    if df_price.empty: return "No data available."
    
    top_comm = df_price.iloc[0]['Commodity']
    top_comm_price = df_price.iloc[0]['Median_Price']
    bottom_comm = df_price.iloc[-1]['Commodity']
    bottom_price = df_price.iloc[-1]['Median_Price']
    
    insight = f"**Commodity Value Disparity:** The agricultural dataset contains extreme intra-commodity variance. "
    insight += f"High-value specialty items like **{top_comm}** anchor the top of the distribution with median prices around ₹{top_comm_price:,.2f}, "
    insight += f"which is orders of magnitude higher than bulk staple crops (the lowest in this top-20 tier being {bottom_comm} at ₹{bottom_price:,.2f}). "
    insight += "This extreme stratification confirms that computing any unweighted 'average agricultural price' is mathematically misleading. "
    insight += "Furthermore, pricing metrics strictly depend on the intrinsic unit value and bulk scale of the crop (e.g., spices vs root vegetables)."
    
    return insight

st.title("Commodity Analysis")
st.write("Understand the pricing scales and reporting volume across different agricultural commodities.")

comm_df = load_commodity_summary()

if not comm_df.empty:
    st.subheader("Top Commodities by Record Volume")
    top_comm_vol = comm_df.sort_values(by="Records", ascending=False).head(20)
    
    fig1 = px.bar(top_comm_vol, x="Commodity", y="Records", 
                  title="Top 20 Commodities by Volume",
                  labels={"Records": "Number of Observations"})
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Commodities by Median Price")
    robust_comm = comm_df[comm_df["Records"] >= 100]
    top_comm_price = robust_comm.sort_values(by="Median_Price", ascending=False).head(20)
    
    fig2 = px.bar(top_comm_price, x="Commodity", y="Median_Price", 
                  title="Top 20 Commodities by Median Price (Min 100 records)",
                  labels={"Median_Price": "Median Price (₹)"})
    st.plotly_chart(fig2, use_container_width=True)
    
    with st.expander("Insights", expanded=True):
        st.info(inline_generate_commodity_insight(top_comm_price))
    
    st.subheader("Full Commodity Summary")
    st.dataframe(comm_df, use_container_width=True)
