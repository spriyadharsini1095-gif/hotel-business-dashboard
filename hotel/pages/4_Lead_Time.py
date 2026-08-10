import streamlit as st
import matplotlib.pyplot as plt
from utils import get_clean_data, COLORS

st.set_page_config(page_title="Lead Time", page_icon="⏳", layout="wide")
st.title("⏳ Lead Time vs. Cancellation Rate")
st.caption("Business question: Does lead time (days between booking and arrival) affect the cancellation rate?")

clean, _, _ = get_clean_data()

hotel_filter = st.radio("Hotel type", ["Both"] + list(clean["hotel"].unique()), horizontal=True)
view = clean if hotel_filter == "Both" else clean[clean["hotel"] == hotel_filter]

lead_cancel = (view.groupby(["lead_time_bin", "hotel"], observed=True)["is_canceled"]
               .mean().mul(100).unstack())

fig, ax = plt.subplots(figsize=(11, 5))
lead_cancel.plot(marker="o", ax=ax, color=[COLORS[h] for h in lead_cancel.columns])
ax.set_title("Cancellation Rate vs. Lead Time")
ax.set_xlabel("Lead Time (days before arrival)")
ax.set_ylabel("Cancellation Rate (%)")
st.pyplot(fig)

st.dataframe(lead_cancel.style.format("{:.1f}"))

st.markdown("""
**Reading the chart:** cancellation rate is **lowest for last-minute bookings** (0–7 days out) and
rises steadily with lead time, peaking for bookings made **181+ days** in advance. City Hotel's rate
climbs more sharply than Resort Hotel's, which stays comparatively more moderate.

**Why this might happen:** far-ahead City Hotel bookings likely include more business/short-trip
travel, whose plans are inherently more changeable the further out they're made — meetings get moved,
trips get cancelled — while far-ahead Resort Hotel bookings are more often deliberate holiday planning
guests are committed to.

**Possible action:** pre-arrival reminder/re-confirmation emails for 90+ day bookings, and a small
refundable-until-a-cutoff deposit that scales with how far ahead the booking is made.
""")
