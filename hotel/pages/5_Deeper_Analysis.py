import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_clean_data, COLORS

st.set_page_config(page_title="Deeper Analysis", page_icon="🔍", layout="wide")
st.title("🔍 Deeper Analysis")
st.caption("Univariate and multivariate views that support the three main business questions.")

clean, _, _ = get_clean_data()

tab1, tab2 = st.tabs(["Univariate", "Multivariate"])

# ---------------- Univariate ----------------
with tab1:
    st.subheader("Distribution of individual variables")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 4))
        clean["is_canceled"].value_counts().plot(kind="bar", color=["#4C72B0", "#DD8452"], ax=ax)
        ax.set_xticklabels(["Not Cancelled", "Cancelled"], rotation=0)
        ax.set_title("Overall Booking Outcome")
        st.pyplot(fig)
        rate = clean["is_canceled"].mean() * 100
        st.caption(f"Baseline cancellation rate across all bookings: {rate:.1f}%")

    with c2:
        fig, ax = plt.subplots(figsize=(6, 4))
        clean["adr"].hist(bins=40, ax=ax, color="#DD8452")
        ax.set_title("Distribution of ADR (Average Daily Rate)")
        ax.set_xlabel("ADR")
        st.pyplot(fig)

    c3, c4 = st.columns(2)
    with c3:
        fig, ax = plt.subplots(figsize=(6, 4))
        clean["lead_time"].hist(bins=40, ax=ax, color="#4C72B0")
        ax.set_title("Distribution of Lead Time")
        ax.set_xlabel("Lead Time (days)")
        st.pyplot(fig)
        st.caption("Right-skewed — most bookings have short lead times, "
                   "which is why lead time is binned into ranges elsewhere in this dashboard.")

    with c4:
        fig, ax = plt.subplots(figsize=(6, 4))
        clean["customer_type"].value_counts().plot(kind="bar", color="#55A868", ax=ax)
        ax.set_title("Bookings by Customer Type")
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig)

# ---------------- Multivariate ----------------
with tab2:
    st.subheader("Relationships between multiple variables")

    st.markdown("**Correlation between numeric features**")
    numeric_cols = ["lead_time", "total_nights", "adults", "children", "babies",
                     "adr", "previous_cancellations", "booking_changes",
                     "total_of_special_requests", "is_canceled"]
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(clean[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)
    st.caption("Look at the is_canceled row/column — the darkest cells against it are the "
               "strongest (positive or negative) cancellation drivers.")

    st.markdown("---")
    st.markdown("**ADR by hotel type and cancellation status**")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=clean, x="hotel", y="adr", hue="is_canceled", ax=ax,
                palette=[COLORS["City Hotel"], COLORS["Resort Hotel"]])
    ax.set_ylim(0, 400)
    ax.legend(title="Cancelled", labels=["No", "Yes"])
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("**Cancellation rate by market segment and hotel type**")
    seg_cancel = (clean.groupby(["market_segment", "hotel"], observed=True)["is_canceled"]
                  .mean().mul(100).unstack())
    fig, ax = plt.subplots(figsize=(10, 5))
    seg_cancel.plot(kind="bar", ax=ax, color=[COLORS[h] for h in seg_cancel.columns])
    ax.set_ylabel("Cancellation Rate (%)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("**Cancellation rate by deposit type**")
    dep_cancel = clean.groupby("deposit_type")["is_canceled"].mean().mul(100)
    fig, ax = plt.subplots(figsize=(7, 4))
    dep_cancel.plot(kind="bar", color="#8172B2", ax=ax)
    ax.set_ylabel("Cancellation Rate (%)")
    plt.xticks(rotation=0)
    st.pyplot(fig)
    st.caption("Directly tests one of the Stage 3 recommendations — whether deposit type is already "
               "associated with different cancellation behaviour in the historical data.")
