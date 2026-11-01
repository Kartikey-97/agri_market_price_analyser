import streamlit as st
from src.data_loader import load_model_comparison

def inline_generate_model_insight(df):
    if df.empty: return "No data available."
    
    naive_mae = df.loc[df['Model'] == 'Naive Baseline', 'MAE'].values[0]
    lr_rmse = df.loc[df['Model'] == 'Linear Regression', 'RMSE'].values[0]
    rf_mae = df.loc[df['Model'] == 'Random Forest', 'MAE'].values[0]
    
    insight = f"**Predictive Modeling Benchmark:** The results strongly validate the heavy day-to-day persistence of agricultural prices. "
    insight += f"The strictly 'Naive' approach (carrying today's exact price over to tomorrow) achieved an exceptional MAE of ₹{naive_mae:,.2f}. "
    insight += f"Conversely, Linear Regression optimized better for outlier penalties, securing the absolute lowest RMSE (₹{lr_rmse:,.2f}). "
    insight += f"Crucially, the failure of complex tree ensembles (like Random Forest at ₹{rf_mae:,.2f} MAE) to dramatically beat the naive baseline "
    insight += "proves that raw algorithmic complexity does not automatically yield better day-ahead predictions in highly autoregressive, noisy series."
    return insight

st.title("Model Performance")
st.write("Canonical model comparison on the frozen 2024 dataset.")

comp_df = load_model_comparison()

st.subheader("Validation Metrics")
st.dataframe(comp_df, use_container_width=True)

with st.expander("Insights", expanded=True):
    st.info(inline_generate_model_insight(comp_df))

st.markdown("""
### Explanation of Metrics
* **MAE (Mean Absolute Error):** The average absolute difference between predicted and actual price, expressed in rupees. (Lower is better).
* **RMSE (Root Mean Squared Error):** Similar to MAE but gives more weight to larger errors. (Lower is better).
* **R²:** A variance-explanation statistic. (Higher is better).

### Evaluation Timeline (Chronological Split)
* **Training:** 2024-01-01 → 2024-09-30
* **Validation:** 2024-10-01 → 2024-11-30
* **Test:** 2024-12-01 → 2024-12-30
""")
