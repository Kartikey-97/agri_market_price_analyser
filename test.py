import pandas as pd
from io import StringIO
df = pd.read_parquet('data/dashboard_data.parquet')
df["Month"] = pd.to_datetime(df["Arrival_Date"]).dt.month
monthly_trend = df.groupby("Month")["Modal_Price"].median().reset_index()
monthly_trend = monthly_trend.rename(columns={"Modal_Price": "Median_Price"})
month_map = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
monthly_trend["Month_Name"] = monthly_trend["Month"].map(month_map)

j = monthly_trend.to_json()
print("JSON string length:", len(j))

try:
    df2 = pd.read_json(StringIO(j))
    print("Success! Length:", len(df2))
except Exception as e:
    print("Failed!", e)
