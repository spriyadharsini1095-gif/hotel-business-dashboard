"""
Shared data loading + cleaning logic for the Hotel Business Investigation dashboard.
Every page imports get_clean_data() so the cleaning steps (and their justification)
live in exactly one place, matching the notebook's Stage 1 decisions.
"""
import pandas as pd
import streamlit as st

COLORS = {"City Hotel": "#4C72B0", "Resort Hotel": "#DD8452"}
MONTH_ORDER = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']


@st.cache_data
def load_raw_data(path: str = "hotel_bookings_data.csv") -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data
def get_clean_data(path: str = "hotel_bookings_data.csv"):
    """Applies the same Stage 1 cleaning decisions as the analysis notebook.
    Returns (clean_df, cleaning_log) where cleaning_log is a list of
    (step, detail, rows_before, rows_after) tuples for display on the Data Quality page.
    """
    df = load_raw_data(path)
    log = []
    clean = df.copy()
    rows_before = len(clean)

    # 1. company / agent -> presence flags instead of dropping
    clean["booked_via_company"] = clean["company"].notna().astype(int)
    clean["booked_via_agent"] = clean["agent"].notna().astype(int)
    clean = clean.drop(columns=["company", "agent"])
    log.append(("Missing company/agent",
                 "Converted to booked_via_company / booked_via_agent flags (0/1) "
                 "instead of dropping rows, since a missing ID means 'not used', not an error.",
                 rows_before, len(clean)))

    # 2. city: drop missing rows
    n = len(clean)
    clean = clean.dropna(subset=["city"])
    log.append(("Missing city", f"Dropped {n - len(clean)} rows with no recorded city (0.4% of data).",
                 n, len(clean)))

    # 3. children: fill missing with 0
    n_missing_children = clean["children"].isna().sum()
    clean["children"] = clean["children"].fillna(0)
    log.append(("Missing children", f"Filled {n_missing_children} missing values with 0 (most common value).",
                 len(clean), len(clean)))

    # 4. duplicates
    n = len(clean)
    clean = clean.drop_duplicates()
    log.append(("Duplicate rows", f"Dropped {n - len(clean)} exact duplicate rows ({(n - len(clean)) / n * 100:.1f}%).",
                 n, len(clean)))

    # 5. meal: recategorise Undefined -> No Meal
    clean["meal"] = clean["meal"].replace({"Undefined": "No Meal"})
    log.append(("Meal category cleanup", "Merged 'Undefined' into 'No Meal' (same real-world meaning).",
                 len(clean), len(clean)))

    # 6. adr anomalies
    n = len(clean)
    clean = clean[(clean["adr"] >= 0) & (clean["adr"] <= 1000)]
    clean["adr_is_zero"] = (clean["adr"] == 0).astype(int)
    log.append(("ADR anomalies", f"Dropped {n - len(clean)} rows with negative or extreme (>1000) ADR; flagged zero-rate rows.",
                 n, len(clean)))

    # 7. zero-guest bookings
    n = len(clean)
    clean["total_guests"] = clean["adults"] + clean["children"] + clean["babies"]
    clean = clean[clean["total_guests"] > 0]
    log.append(("Zero-guest bookings", f"Dropped {n - len(clean)} bookings with zero adults, children, and babies.",
                 n, len(clean)))

    # helper columns
    clean["total_nights"] = clean["stays_in_weekend_nights"] + clean["stays_in_weekdays_nights"]
    clean["arrival_date_month"] = pd.Categorical(clean["arrival_date_month"],
                                                  categories=MONTH_ORDER, ordered=True)
    bins = [0, 7, 30, 60, 90, 180, 365, clean["lead_time"].max() + 1]
    labels = ["0-7", "8-30", "31-60", "61-90", "91-180", "181-365", "365+"]
    clean["lead_time_bin"] = pd.cut(clean["lead_time"], bins=bins, labels=labels, include_lowest=True)

    return clean, log, rows_before
