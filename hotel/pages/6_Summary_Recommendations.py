import streamlit as st
from utils import get_clean_data

st.set_page_config(page_title="Summary & Recommendations", page_icon="✅", layout="wide")
st.title("✅ Summary & Recommendations")

clean, _, _ = get_clean_data()

st.markdown("### Key findings")
st.markdown("""
- **Hotel type popularity:** City Hotel is booked roughly **twice as often** as Resort Hotel overall.
  Both properties share the same summer peak (July–August) and winter trough (November–January), but
  City Hotel's demand swings more sharply between the two.
- **Stay duration and cancellations:** the longer a booking's stay, the **higher its cancellation
  rate** — true for both hotel types, and more pronounced at City Hotel.
- **Lead time and cancellations:** the further in advance a booking is made, the **higher its
  cancellation rate** — again true for both, with City Hotel climbing more steeply at long lead times.

A common thread: **City Hotel bookings are consistently more cancellation-prone** than Resort Hotel
bookings, whether the driver is a longer stay or a longer lead time.
""")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### Recommendations — hotel type & seasonality")
    st.markdown("""
    - Grow **Resort Hotel's** share by targeting marketing spend in its stronger shoulder months
      (March–May), building on a base that already holds up better than City Hotel's.
    - Capitalise on the **July–August peak** with higher rates and premium packages; use the
      **November–January trough** for value promotions or maintenance windows.
    """)

    st.markdown("### Recommendations — stay duration")
    st.markdown("""
    - Tiered deposit / cancellation policy for longer stays (e.g. 5+ nights), which show the highest
      cancellation risk.
    - Offer a modest discount for long stays in exchange for a partial upfront payment, keeping them
      appealing to book while reducing the "free option to cancel."
    """)

with c2:
    st.markdown("### Recommendations — lead time")
    st.markdown("""
    - Automatic reminder / re-confirmation emails for bookings made 90+ days out — the highest-risk band.
    - A small refundable-until-a-cutoff deposit that scales with how far ahead the booking is made.
    """)

    st.markdown("### Highest-impact recommendation")
    st.info("""
    A **tiered deposit/cancellation policy targeted at City Hotel's longest-lead-time, longest-stay
    segment** is likely to have the single biggest impact — it's the one property and segment where
    both major cancellation drivers found in this data (stay length and lead time) overlap most
    strongly.
    """)

st.markdown("---")
st.metric("Overall cancellation rate (cleaned data)", f"{clean['is_canceled'].mean()*100:.1f}%")
