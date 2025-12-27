import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("Discrepancy Checker")

uploaded_file = st.file_uploader("## Upload a FVR", type=["xlsx"])

# 🔒 Main guard
if uploaded_file and uploaded_file.name.endswith(".xlsx"):
    excel_file = pd.ExcelFile(uploaded_file)

    selected_sheets = st.multiselect(
        "Select sheets to check discrepancy",
        options=excel_file.sheet_names,
        key="sheets_to_display"
    )

    # 🔒 Only when user selects sheets
    if selected_sheets:
        sheet_tables = {}

        for sheet in selected_sheets:
            sheet_tables[sheet] = pd.read_excel(
                uploaded_file,
                sheet_name=sheet
            )

        st.success("Selected sheets loaded successfully")

            # =====================================================
        # 🔢 OVERALL DISCREPANCY (LEVEL vs PROPERTY) - FIXED
        # =====================================================
        st.subheader("🔢 Overall Discrepancy")

        property_sheet = selected_sheets[0]

        # Ensure there is at least one other sheet besides property_sheet
        other_sheets = [sheet for sheet in selected_sheets if sheet != property_sheet]

        if other_sheets:  # Only show if there are other sheets
            level_sheet = st.selectbox(
                "Select sheet for breakdown level",
                options=other_sheets
            )

            if level_sheet:  # Only proceed if user selects a sheet
                breakdown_level = st.selectbox(
                    "Select breakdown level column",
                    options=sheet_tables[level_sheet].columns.tolist()
                )

                metric = st.selectbox(
                    "Select metric",
                    options=[
                        "Occupancy On Books This Year",
                        "Booked Room Revenue This Year"
                    ]
                )

                # Calculate totals
                prop_total = sheet_tables[property_sheet][metric].sum()
                level_total = sheet_tables[level_sheet][metric].sum()

                discrepancy = level_total - prop_total
                discrepancy_pct = (discrepancy / prop_total * 100) if prop_total != 0 else 0

                st.metric(
                    label=f"{breakdown_level} vs Property ({metric})",
                    value=f"{discrepancy:,.2f}",
                    delta=f"{discrepancy_pct:.2f} %"
                )
        else:
            st.warning("You need at least two sheets to compare property vs breakdown.")


        # -----------------------------
        # 📊 VIEW TABLES (OPTIONAL)
        # -----------------------------
        st.subheader("📊 View Selected Tables")

        sheet_to_view = st.selectbox(
            "Choose a sheet to view",
            options=selected_sheets
        )

        st.dataframe(
            sheet_tables[sheet_to_view],
            use_container_width=True
        )

        # =====================================================
        # 📈 GRAPH 1: OCCUPANCY vs DATE
        # =====================================================
        st.subheader("📈 Occupancy On Books This Year vs Occupancy Date")

        occupancy_frames = []

        for sheet_name, df in sheet_tables.items():
            if {
                "Occupancy Date",
                "Occupancy On Books This Year"
            }.issubset(df.columns):

                temp = df[
                    ["Occupancy Date", "Occupancy On Books This Year"]
                ].copy()

                temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
                temp["Category"] = sheet_name

                occupancy_frames.append(temp)

        if occupancy_frames:
            occupancy_df = pd.concat(occupancy_frames)

            occupancy_pivot = occupancy_df.pivot_table(
                index="Occupancy Date",
                columns="Category",
                values="Occupancy On Books This Year",
                aggfunc="sum"
            ).sort_index()

            st.line_chart(occupancy_pivot, use_container_width=True)

# ============================
# 📥 DOWNLOAD OPTIONS
# ============================

            col1, col2 = st.columns(2)

            # ---- Download DATA ----
            with col1:
                csv = occupancy_pivot.reset_index().to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Data (CSV)",
                    data=csv,
                    file_name="occupancy_data.csv",
                    mime="text/csv"
                )

            # ---- Download GRAPH ----
            with col2:
                fig, ax = plt.subplots(figsize=(12, 6))

                for column in occupancy_pivot.columns:
                    ax.plot(
                        occupancy_pivot.index,
                        occupancy_pivot[column],
                        label=column
                    )

                ax.set_title("Occupancy On Books This Year vs Occupancy Date")
                ax.set_xlabel("Occupancy Date")
                ax.set_ylabel("Occupancy")
                ax.legend()
                ax.grid(True)

                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches="tight")
                plt.close(fig)
                buf.seek(0)

                st.download_button(
                    label="⬇️ Download Graph (PNG)",
                    data=buf,
                    file_name="occupancy_trend.png",
                    mime="image/png"
                )


        # =====================================================
        # 📉 GRAPH 2: REVENUE vs DATE
        # =====================================================
        st.subheader("📉 Booked Room Revenue This Year vs Occupancy Date")

        revenue_frames = []

        for sheet_name, df in sheet_tables.items():
            if {
                "Occupancy Date",
                "Booked Room Revenue This Year"
            }.issubset(df.columns):

                temp = df[
                    ["Occupancy Date", "Booked Room Revenue This Year"]
                ].copy()

                temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
                temp["Category"] = sheet_name

                revenue_frames.append(temp)

        if revenue_frames:
            revenue_df = pd.concat(revenue_frames)

            revenue_pivot = revenue_df.pivot_table(
                index="Occupancy Date",
                columns="Category",
                values="Booked Room Revenue This Year",
                aggfunc="sum"
            ).sort_index()

            st.line_chart(revenue_pivot, use_container_width=True)

            # ============================
            # 📥 DOWNLOAD OPTIONS
            # ============================

            col1, col2 = st.columns(2)

            # ---- Download DATA ----
            with col1:
                csv = revenue_pivot.reset_index().to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Data (CSV)",
                    data=csv,
                    file_name="revenue_data.csv",
                    mime="text/csv"
                )

            # ---- Download GRAPH ----
            with col2:
                fig, ax = plt.subplots(figsize=(12, 6))

                for column in revenue_pivot.columns:
                    ax.plot(
                        revenue_pivot.index,
                        revenue_pivot[column],
                        label=column
                    )

                ax.set_title("Booked Room Revenue This Year vs Occupancy Date")
                ax.set_xlabel("Occupancy Date")
                ax.set_ylabel("Booked Room Revenue This Year")
                ax.legend()
                ax.grid(True)

                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches="tight")
                plt.close(fig)
                buf.seek(0)

                st.download_button(
                    label="⬇️ Download Graph (PNG)",
                    data=buf,
                    file_name="revenue_trend.png",
                    mime="image/png"
                )


else:
    st.info("Please upload a valid Excel file.")
