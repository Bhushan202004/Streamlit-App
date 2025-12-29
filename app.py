import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hotel Forecast – Date-wise View", layout="wide")
st.title("📊 Hotel Forecast – Date-wise View (All Levels)")

uploaded_file = st.file_uploader("Upload Excel Forecast File", type=["xlsx"])

if uploaded_file:
    sheets = pd.read_excel(uploaded_file, sheet_name=None)

    occupancy_data = []
    revenue_data = []

    for sheet_name, df in sheets.items():

        df = df.copy()

        # ---------- OCCUPANCY ----------
        occ_cols = {"Occupancy Date", "Occupancy On Books This Year"}
        if occ_cols.issubset(df.columns):
            df_occ = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
            df_occ["Occupancy Date"] = pd.to_datetime(df_occ["Occupancy Date"], errors="coerce")
            df_occ = df_occ.dropna(subset=["Occupancy Date"])

            occ_datewise = (
                df_occ.groupby("Occupancy Date", as_index=False)
                      .agg({"Occupancy On Books This Year": "sum"})
            )

            occ_datewise["Level"] = sheet_name
            occupancy_data.append(occ_datewise)

        # ---------- REVENUE ----------
        rev_cols = {"Occupancy Date", "Booked Room Revenue This Year"}
        if rev_cols.issubset(df.columns):
            df_rev = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
            df_rev["Occupancy Date"] = pd.to_datetime(df_rev["Occupancy Date"], errors="coerce")
            df_rev = df_rev.dropna(subset=["Occupancy Date"])

            rev_datewise = (
                df_rev.groupby("Occupancy Date", as_index=False)
                      .agg({"Booked Room Revenue This Year": "sum"})
            )

            rev_datewise["Level"] = sheet_name
            revenue_data.append(rev_datewise)

    # =======================
    # 📈 OCCUPANCY GRAPH
    # =======================
    if occupancy_data:
        occ_final = pd.concat(occupancy_data)

        fig_occ = px.line(
            occ_final,
            x="Occupancy Date",
            y="Occupancy On Books This Year",
            color="Level",
            markers=True,
            title="Occupancy On Books This Year vs Occupancy Date"
        )

        st.plotly_chart(fig_occ, use_container_width=True)

        st.download_button(
            "⬇️ Download Occupancy Data (CSV)",
            occ_final.to_csv(index=False).encode("utf-8"),
            file_name="datewise_occupancy_all_levels.csv",
            mime="text/csv"
        )

    # =======================
    # 📉 REVENUE GRAPH
    # =======================
    if revenue_data:
        rev_final = pd.concat(revenue_data)

        fig_rev = px.line(
            rev_final,
            x="Occupancy Date",
            y="Booked Room Revenue This Year",
            color="Level",
            markers=True,
            title="Booked Room Revenue This Year vs Occupancy Date"
        )

        st.plotly_chart(fig_rev, use_container_width=True)

        st.download_button(
            "⬇️ Download Revenue Data (CSV)",
            rev_final.to_csv(index=False).encode("utf-8"),
            file_name="datewise_revenue_all_levels.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload an Excel file to continue.")
