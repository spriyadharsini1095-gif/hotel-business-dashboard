import streamlit as st
import matplotlib.pyplot as plt
from utils import get_clean_data, COLORS, MONTH_ORDER

st.set_page_config(page_title="Hotel Type & Seasonality", page_icon="🏨", layout="wide")
st.title("🏨 Hotel Type & Seasonality")
st.caption("Business question: Which hotel type do customers book most often, and how does that change by season?")

clean, _, _ = get_clean_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Share of bookings by hotel type")
    hotel_share = clean["hotel"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(hotel_share, labels=hotel_share.index, autopct="%1.1f%%",
           colors=[COLORS[h] for h in hotel_share.index], startangle=90)
    ax.set_title("Booking Share by Hotel Type")
    st.pyplot(fig)
    pct = hotel_share.iloc[0] / hotel_share.sum() * 100
    st.caption(f"{hotel_share.index[0]} accounts for {pct:.1f}% of all bookings.")

with col2:
    st.subheader("Filter")
    years = st.multiselect("Arrival year", sorted(clean["arrival_date_year"].unique()),
                            default=sorted(clean["arrival_date_year"].unique()))
    hotels = st.multiselect("Hotel type", clean["hotel"].unique(), default=list(clean["hotel"].unique()))

filtered = clean[clean["arrival_date_year"].isin(years) & clean["hotel"].isin(hotels)]

st.subheader("Bookings per month by hotel type")
monthly = filtered.groupby(["arrival_date_month", "hotel"], observed=True).size().unstack()
fig, ax = plt.subplots(figsize=(11, 5))
monthly.plot(marker="o", ax=ax, color=[COLORS[h] for h in monthly.columns])
ax.set_title("Bookings per Month by Hotel Type")
ax.set_xlabel("Month")
ax.set_ylabel("Number of Bookings")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
**Reading the chart:** both hotel types follow the same broad seasonal shape — rising through spring,
peaking in July/August, and falling toward the November–January trough. City Hotel's swing is sharper,
suggesting more leisure/short-notice demand, while Resort Hotel stays comparatively steadier through
the shoulder months.

**Possible actions:** raise rates and push higher-margin packages during the July–August peak;
use the winter trough for promotions or maintenance windows; target Resort Hotel marketing spend in
its stronger shoulder months (March–May) to help grow its overall share.
""")
