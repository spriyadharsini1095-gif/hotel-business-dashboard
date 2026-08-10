import streamlit as st
from utils import get_clean_data

st.set_page_config(page_title="Hotel Business Investigation", page_icon="🏨", layout="wide")

st.title("🏨 Investigate Hotel Business using Data Visualization")
st.caption("Understanding Booking & Cancellation Behaviour · Dataset: 2017–2019 hotel bookings")

clean, log, rows_before = get_clean_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Raw rows", f"{rows_before:,}")
col2.metric("Clean rows", f"{len(clean):,}")
col3.metric("Overall cancellation rate", f"{clean['is_canceled'].mean()*100:.1f}%")
col4.metric("Hotel types", clean["hotel"].nunique())

st.markdown("---")

st.markdown("""
### About this dashboard

This dashboard answers three business questions for a hotel company using two years of booking data:

1. **Which hotel type do customers book most often, and how does that change by season?**
2. **Does length of stay affect the cancellation rate?**
3. **Does lead time (days between booking and arrival) affect the cancellation rate?**

Use the **pages in the sidebar** to move through the investigation:

| Page | What it covers |
|---|---|
| 📋 Data Quality | Missing values, duplicates, anomalies, and the cleaning decisions applied |
| 🏨 Hotel Type & Seasonality | Booking share and monthly trends by hotel type |
| 📅 Stay Duration | Cancellation rate vs. length of stay |
| ⏳ Lead Time | Cancellation rate vs. days booked in advance |
| 🔍 Deeper Analysis | Univariate and multivariate views (correlations, market segment, deposit type) |
| ✅ Summary & Recommendations | Key findings and actionable next steps |

All charts use the **cleaned dataset** — see the Data Quality page for exactly what was removed and why.
""")

with st.expander("Preview cleaned data (first 20 rows)"):
    st.dataframe(clean.head(20))
