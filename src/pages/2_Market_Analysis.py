import streamlit as st
import plotly.express as px
from src.data_loader import load_market_summary

def inline_generate_market_insight(df, state_filter):
    if df.empty: return "No data available."
    
    top_market = df.iloc[0]['Market']
    top_market_records = df.iloc[0]['Records']
    median_price = df.iloc[0]['Median_Price']
    avg_commodities = df['Commodities'].mean()
    
    scope = "Nationally" if state_filter == "All" else f"In **{state_filter}**"
    
    insight = f"**Market Concentration Analysis:** {scope}, **{top_market}** emerges as the highest-volume trading hub with {top_market_records:,} recorded transactions. "
    insight += f"Interestingly, there is no direct correlation between a market's raw volume and its median price (which sits at ₹{median_price:,.2f} for {top_market}). "
    insight += "High-volume super-markets typically trade a massive bedrock of staple commodities (like wheat and potatoes), which drags their aggregate medians down. "
    insight += f"Conversely, markets specializing in a smaller number of luxury crops (spices, fruits) exhibit much higher price floors. The top markets here handle an average of {avg_commodities:.1f} distinct commodities."
    
    return insight

st.title("Market Analysis")
st.write("Explore price dynamics and volume across different agricultural markets.")

market_df = load_market_summary()

if not market_df.empty:
    st.sidebar.subheader("Filter Markets")
    state_filter = st.sidebar.selectbox("Select State", ["All"] + list(market_df["State"].unique()))
    
    if state_filter != "All":
        filtered_df = market_df[market_df["State"] == state_filter]
    else:
        filtered_df = market_df
        
    st.subheader(f"Top 20 Markets by Volume ({state_filter})")
    top_markets = filtered_df.sort_values(by="Records", ascending=False).head(20)
    
    fig = px.bar(top_markets, x="Market", y="Records", color="Median_Price", 
                 title="Market Volume and Median Price",
                 labels={"Records": "Number of Records", "Median_Price": "Median Price (₹)"},
                 hover_data=["Average_Price", "Commodities"])
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Insights", expanded=True):
        st.info(inline_generate_market_insight(top_markets, state_filter))
    
    st.subheader("Market Data Summary")
    st.dataframe(filtered_df.head(100), use_container_width=True)
