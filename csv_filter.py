# app.py
"""
Streamlit CSV Column Chooser

Usage:
    1. Install dependencies:
       pip install streamlit pandas

    2. Run the application:
       streamlit run app.py
"""

import streamlit as st
import pandas as pd
from io import BytesIO


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a DataFrame to UTF‑8 encoded CSV bytes without the index column."""
    return df.to_csv(index=False).encode("utf-8")


def main() -> None:
    st.set_page_config(page_title="CSV Column Chooser", page_icon="🗂️")
    st.title("🗂️ CSV Column Chooser & Downloader")

    st.write(
        "Upload a **CSV** file, pick the columns you care about, and download a new "
        "CSV containing **only** those columns — all rows preserved."
    )

    # Step 1 — Upload
    uploaded_file = st.file_uploader("Step 1 — Upload your CSV", type="csv")

    if uploaded_file is None:
        st.info("Awaiting CSV upload…")
        st.stop()

    # Step 2 — Read the CSV safely
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as err:
        st.error(f"❌ Could not read CSV: {err}")
        st.stop()

    if df.empty:
        st.warning("The uploaded CSV appears to be empty.")
        st.stop()

    # Optional preview of the raw data
    with st.expander("👀 Peek at your data", expanded=False):
        st.dataframe(df, use_container_width=True, height=300)

    # Step 3 — Column selection
    st.subheader("Step 2 — Select columns")
    column_options = df.columns.tolist()
    selected_cols = st.multiselect(
        "Choose the columns to keep:",
        options=column_options,
        default=column_options,  # pre‑select all columns by default
        help="At least one column must be selected to enable download.",
    )

    if not selected_cols:
        st.info("Select at least one column to continue.")
        st.stop()

    # Create the filtered DataFrame
    filtered_df = df[selected_cols]

    # Optional preview of the filtered data
    with st.expander("🔎 Preview filtered data", expanded=False):
        st.dataframe(filtered_df, use_container_width=True, height=300)

    # Step 4 — Generate download
    csv_bytes = to_csv_bytes(filtered_df)

    st.subheader("Step 3 — Download")
    st.download_button(
        label="📥 Download filtered CSV",
        data=csv_bytes,
        file_name="filtered_columns.csv",
        mime="text/csv",
    )

    st.success("Ready! Click the button above to download your new CSV file.")


if __name__ == "__main__":
    main()
