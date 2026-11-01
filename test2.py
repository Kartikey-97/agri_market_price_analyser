import pandas as pd
from io import StringIO
df = pd.read_parquet('data/dashboard_data.parquet')
df["Month"] = pd.to_datetime(df["Arrival_Date"]).dt.month
monthly_trend = df.groupby("Month")["Modal_Price"].median().reset_index()
monthly_trend = monthly_trend.rename(columns={"Modal_Price": "Median_Price"})
month_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
monthly_trend["Month_Name"] = monthly_trend["Month"].map(month_map)

j = monthly_trend.to_json()
df2 = pd.read_json(StringIO(j))

try:
    max_idx = df2['Median_Price'].idxmax()
    min_idx = df2['Median_Price'].idxmin()
    max_month = df2.loc[max_idx]['Month_Name']
    min_month = df2.loc[min_idx]['Month_Name']
    max_price = df2.loc[max_idx]['Median_Price']
    min_price = df2.loc[min_idx]['Median_Price']
    diff = max_price - min_price
    pct_change = (diff / min_price) * 100 if min_price > 0 else 0
    print("Success!", max_month, pct_change)
except Exception as e:
    import traceback
    print("Failed!", e)
    traceback.print_exc()
