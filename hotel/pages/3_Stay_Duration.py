import streamlit as st
import matplotlib.pyplot as plt
from utils import get_clean_data, COLORS

st.set_page_config(page_title="Stay Duration", page_icon="📅", layout="wide")
st.title("📅 Stay Duration vs. Cancellation Rate")
st.caption("Business question: Does the length of stay affect the booking cancellation rate?")

clean, _, _ = get_clean_data()

max_nights = st.slider("Max nights to show", 5, 30, 14)

cancel_by_hotel = clean.groupby("hotel")["is_canceled"].mean() * 100
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Overall cancellation rate by hotel")
    fig, ax = plt.subplots(figsize=(5, 5))
    bars = ax.bar(cancel_by_hotel.index, cancel_by_hotel.values,
                   color=[COLORS[h] for h in cancel_by_hotel.index])
    ax.set_ylabel("Cancellation Rate (%)")
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%", (bar.get_x() + bar.get_width() / 2, h),
                    ha="center", va="bottom", fontweight="bold")
    st.pyplot(fig)

with col2:
    st.subheader(f"Cancellation rate vs. length of stay (0–{max_nights} nights)")
    stay_df = clean[clean["total_nights"].between(0, max_nights)]
    stay_cancel = (stay_df.groupby(["total_nights", "hotel"], observed=True)["is_canceled"]
                   .mean().mul(100).unstack())
    fig, ax = plt.subplots(figsize=(9, 5))
    stay_cancel.plot(marker="o", ax=ax, color=[COLORS[h] for h in stay_cancel.columns])
    ax.set_xlabel("Total Nights Stayed")
    ax.set_ylabel("Cancellation Rate (%)")
    st.pyplot(fig)

st.markdown("""
**Reading the chart:** cancellation rate trends **upward** as stay length increases for both hotel
types — short 1–2 night bookings cancel least, while week-plus stays cancel noticeably more often.
The climb is steeper for City Hotel than Resort Hotel.

**Why this might happen:** a longer stay is a bigger commitment, usually booked further ahead — giving
more time for plans to change — and is more likely booked on a flexible/refundable rate that removes
the financial penalty for cancelling.

**Possible action:** a tiered deposit or stricter cancellation window for longer stays (e.g. 5+ nights),
while keeping short stays flexible to stay attractive.
""")
