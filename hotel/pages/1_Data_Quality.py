import streamlit as st
import pandas as pd
from utils import get_clean_data, load_raw_data

st.set_page_config(page_title="Data Quality", page_icon="📋", layout="wide")
st.title("📋 Data Quality & Cleaning")

df = load_raw_data()
clean, log, rows_before = get_clean_data()

st.markdown("### 1. Missing values (raw data)")
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
missing_pct = (missing / len(df) * 100).round(2)
st.dataframe(pd.DataFrame({"missing_count": missing, "missing_pct (%)": missing_pct}))

st.markdown("### 2. Duplicate rows (raw data)")
dup_count = df.duplicated().sum()
st.metric("Exact duplicate rows", f"{dup_count:,}", f"{dup_count/len(df)*100:.1f}% of dataset")
with st.expander("See a sample of duplicated rows"):
    st.dataframe(df[df.duplicated(keep=False)].sort_values(list(df.columns)).head(10))

st.markdown("### 3. Meal category cleanup")
st.bar_chart(df["meal"].value_counts())
st.caption("`Undefined` is merged into `No Meal` in the cleaned dataset — both mean no meal plan was booked.")

st.markdown("### 4. Anomalies (raw data)")
c1, c2, c3 = st.columns(3)
c1.metric("Negative ADR rows", int((df["adr"] < 0).sum()))
c2.metric("Extreme ADR rows (>1000)", int((df["adr"] > 1000).sum()))
total_guests = df["adults"] + df["children"].fillna(0) + df["babies"]
c3.metric("Zero-guest bookings", int((total_guests == 0).sum()))

st.markdown("---")
st.markdown("### Cleaning steps applied (in order)")

for step, detail, before, after in log:
    with st.container(border=True):
        cols = st.columns([2, 5, 2])
        cols[0].markdown(f"**{step}**")
        cols[1].markdown(detail)
        cols[2].markdown(f"{before:,} → {after:,} rows")

st.success(f"Final cleaned dataset: **{len(clean):,} rows** "
           f"(removed {rows_before - len(clean):,}, {(rows_before-len(clean))/rows_before*100:.1f}% of the raw data)")
