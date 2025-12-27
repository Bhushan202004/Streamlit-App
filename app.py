# import streamlit as st
# import pandas as pd

# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader(
#     "## Upload a FVR",
#     type=["xlsx"]
# )

# # 🔒 Main guard
# if uploaded_file and uploaded_file.name.endswith(".xlsx"):
#     excel_file = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets to check discrepancy",
#         options=excel_file.sheet_names,
#         key="sheets_to_display"
#     )

#     # 🔒 Only when user selects sheets
#     if selected_sheets:
#         sheet_tables = {}

#         for sheet in selected_sheets:
#             sheet_tables[sheet] = pd.read_excel(
#                 uploaded_file,
#                 sheet_name=sheet
#             )

#         st.success("Selected sheets loaded successfully")


#         st.subheader("⚖️ Overall Percentage Discrepancy Among Selected Sheets")

#         base_sheet = selected_sheets[0]  # first sheet as base
#         discrepancy_summary = {"Metric": [], "Compared Sheet": [], "Discrepancy (%)": []}

#         metrics = ["Occupancy On Books This Year", "Booked Room Revenue This Year"]

#         for metric in metrics:
#           base_total = sheet_tables[base_sheet][metric].sum()
         
#           for sheet_name in selected_sheets[1:]:
#              comp_total = sheet_tables[sheet_name][metric].sum()
#              perc_diff = ((comp_total - base_total) / base_total) * 100
            
#             # <-- append must be here, inside the inner loop
#              discrepancy_summary["Metric"].append(metric)
#              discrepancy_summary["Compared Sheet"].append(sheet_name)
#              discrepancy_summary["Discrepancy (%)"].append(round(perc_diff, 2))


# # Convert to DataFrame for display
#         discrepancy_df = pd.DataFrame(discrepancy_summary)
#         st.dataframe(discrepancy_df, use_container_width=True)



#         # -----------------------------
#         # 📊 VIEW TABLES (OPTIONAL)
#         # -----------------------------
#         st.subheader("📊 View Selected Tables")

#         sheet_to_view = st.selectbox(
#             "Choose a sheet to view",
#             options=selected_sheets
#         )

#         st.dataframe(
#             sheet_tables[sheet_to_view],
#             use_container_width=True
#         )

#         # =====================================================
#         # 📈 GRAPH 1: OCCUPANCY ON BOOKS vs OCCUPANCY DATE
#         # =====================================================
#         st.subheader("📈 Occupancy On Books This Year vs Occupancy Date")

#         occupancy_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {
#                 "Occupancy Date",
#                 "Occupancy On Books This Year"
#             }.issubset(df.columns):

#                 temp = df[
#                     ["Occupancy Date", "Occupancy On Books This Year"]
#                 ].copy()

#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name

#                 occupancy_frames.append(temp)

#         if occupancy_frames:
#             occupancy_df = pd.concat(occupancy_frames)

#             occupancy_pivot = occupancy_df.pivot_table(
#             index="Occupancy Date",
#                 columns="Category",
#                 values="Occupancy On Books This Year",
#                 aggfunc="sum"  # or "mean" if you prefer
#             ).sort_index()
#             st.line_chart(occupancy_pivot, use_container_width=True)

#         # =====================================================
#         # 📉 GRAPH 2: REVENUE vs OCCUPANCY DATE
#         # =====================================================
#         st.subheader("📉 Booked Room Revenue This Year vs Occupancy Date")

#         revenue_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {
#                 "Occupancy Date",
#                 "Booked Room Revenue This Year"
#             }.issubset(df.columns):

#                 temp = df[
#                     ["Occupancy Date", "Booked Room Revenue This Year"]
#                 ].copy()

#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name

#                 revenue_frames.append(temp)

#         if revenue_frames:
#             revenue_df = pd.concat(revenue_frames)

#             revenue_pivot = revenue_df.pivot_table(
#                 index="Occupancy Date",
#                 columns="Category",
#                 values="Booked Room Revenue This Year",
#                 aggfunc="sum"  # or "mean" if you prefer
#             ).sort_index()

#             st.line_chart(revenue_pivot, use_container_width=True)

# else:
#     st.info("Please upload a valid Excel file.")





# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader("## Upload a FVR", type=["xlsx"])

# if uploaded_file and uploaded_file.name.endswith(".xlsx"):
#     excel_file = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets to check discrepancy",
#         options=excel_file.sheet_names,
#         key="sheets_to_display"
#     )

#     if selected_sheets:
#         sheet_tables = {}

#         for sheet in selected_sheets:
#             sheet_tables[sheet] = pd.read_excel(
#                 uploaded_file,
#                 sheet_name=sheet
#             )

#         st.success("Selected sheets loaded successfully")

#         # -------------------------
#         # Plot Occupancy
#         # -------------------------
#         occupancy_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Occupancy On Books This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 occupancy_frames.append(temp)

#         if occupancy_frames:
#             occupancy_df = pd.concat(occupancy_frames)

#             fig_occ = px.line(
#                 occupancy_df,
#                 x="Occupancy Date",
#                 y="Occupancy On Books This Year",
#                 color="Category",
#                 title="Occupancy On Books This Year vs Occupancy Date"
#             )

#             st.plotly_chart(fig_occ, use_container_width=True)

#         # -------------------------
#         # Plot Revenue
#         # -------------------------
#         revenue_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Booked Room Revenue This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 revenue_frames.append(temp)

#         if revenue_frames:
#             revenue_df = pd.concat(revenue_frames)

#             fig_rev = px.line(
#                 revenue_df,
#                 x="Occupancy Date",
#                 y="Booked Room Revenue This Year",
#                 color="Category",
#                 title="Booked Room Revenue This Year vs Occupancy Date"
#             )

#             st.plotly_chart(fig_rev, use_container_width=True)

# else:
#     st.info("Please upload a valid Excel file.")




# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader("## Upload a FVR", type=["xlsx"])

# if uploaded_file and uploaded_file.name.endswith(".xlsx"):
#     excel_file = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets to check discrepancy",
#         options=excel_file.sheet_names,
#         key="sheets_to_display"
#     )

#     if selected_sheets:
#         sheet_tables = {}

#         for sheet in selected_sheets:
#             sheet_tables[sheet] = pd.read_excel(
#                 uploaded_file,
#                 sheet_name=sheet
#             )

#         st.success("Selected sheets loaded successfully")

#         # -------------------------
#         # Optional Table View
#         # -------------------------
#         st.subheader("📊 View Selected Tables")
#         sheet_to_view = st.selectbox(
#             "Choose a sheet to view",
#             options=selected_sheets
#         )
#         st.dataframe(sheet_tables[sheet_to_view], use_container_width=True)

#         # -------------------------
#         # Line Chart: Occupancy
#         # -------------------------
#         st.subheader("📈 Occupancy On Books This Year vs Occupancy Date")

#         occupancy_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Occupancy On Books This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 occupancy_frames.append(temp)

#         if occupancy_frames:
#             occupancy_df = pd.concat(occupancy_frames)
#             fig_occ = px.line(
#                 occupancy_df,
#                 x="Occupancy Date",
#                 y="Occupancy On Books This Year",
#                 color="Category",
#                 markers=False,   # classic smooth line
#                 title="Occupancy On Books This Year"
#             )
#             fig_occ.update_layout(legend_title_text="Sheet/Category")
#             st.plotly_chart(fig_occ, use_container_width=True)

#         # -------------------------
#         # Line Chart: Revenue
#         # -------------------------
#         st.subheader("📉 Booked Room Revenue This Year vs Occupancy Date")

#         revenue_frames = []

#         for sheet_name, df in sheet_tables.items():
#             if {"Occupancy Date", "Booked Room Revenue This Year"}.issubset(df.columns):
#                 temp = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
#                 temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#                 temp["Category"] = sheet_name
#                 revenue_frames.append(temp)

#         if revenue_frames:
#             revenue_df = pd.concat(revenue_frames)
#             fig_rev = px.line(
#                 revenue_df,
#                 x="Occupancy Date",
#                 y="Booked Room Revenue This Year",
#                 color="Category",
#                 markers=False,   # smooth line
#                 title="Booked Room Revenue This Year"
#             )
#             fig_rev.update_layout(legend_title_text="Sheet/Category")
#             st.plotly_chart(fig_rev, use_container_width=True)

# else:
#     st.info("Please upload a valid Excel file.")










# import streamlit as st
# import pandas as pd
# from io import BytesIO

# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader("## Upload a FVR", type=["xlsx"])

# if uploaded_file:
#     excel_file = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets to check discrepancy",
#         options=excel_file.sheet_names
#     )

#     if selected_sheets:
#         sheet_tables = {
#             sheet: pd.read_excel(uploaded_file, sheet_name=sheet)
#             for sheet in selected_sheets
#         }

#         st.success("Selected sheets loaded successfully")

#         # =====================================================
#         # ⚖️ OVERALL PERCENTAGE DISCREPANCY
#         # =====================================================
#         st.subheader("⚖️ Overall Percentage Discrepancy")

#         base_sheet = selected_sheets[0]
#         metrics = [
#             "Occupancy On Books This Year",
#             "Booked Room Revenue This Year"
#         ]

#         rows = []

#         for metric in metrics:
#             base_total = sheet_tables[base_sheet][metric].sum()

#             for sheet in selected_sheets[1:]:
#                 comp_total = sheet_tables[sheet][metric].sum()
#                 diff_pct = ((comp_total - base_total) / base_total) * 100

#                 rows.append({
#                     "Metric": metric,
#                     "Compared Sheet": sheet,
#                     "Discrepancy (%)": round(diff_pct, 2)
#                 })

#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#         # =====================================================
#         # 📈 GRAPH 1: OCCUPANCY vs DATE
#         # =====================================================
#         st.subheader("📈 Occupancy On Books vs Occupancy Date")

#         occ_frames = []

#         for name, df in sheet_tables.items():
#             temp = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
#             temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#             temp["Category"] = name
#             occ_frames.append(temp)

#         occ_df = pd.concat(occ_frames)

#         occ_pivot = occ_df.pivot_table(
#             index="Occupancy Date",
#             columns="Category",
#             values="Occupancy On Books This Year",
#             aggfunc="sum"
#         ).sort_index()

#         st.line_chart(occ_pivot, use_container_width=True)

#         # Download occupancy data
#         buffer = BytesIO()
#         occ_pivot.to_excel(buffer)
#         st.download_button(
#             "⬇ Download Occupancy Graph Data (Excel)",
#             buffer.getvalue(),
#             file_name="occupancy_vs_date.xlsx"
#         )

#         # =====================================================
#         # 📉 GRAPH 2: REVENUE vs DATE
#         # =====================================================
#         st.subheader("📉 Revenue vs Occupancy Date")

#         rev_frames = []

#         for name, df in sheet_tables.items():
#             temp = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
#             temp["Occupancy Date"] = pd.to_datetime(temp["Occupancy Date"])
#             temp["Category"] = name
#             rev_frames.append(temp)

#         rev_df = pd.concat(rev_frames)

#         rev_pivot = rev_df.pivot_table(
#             index="Occupancy Date",
#             columns="Category",
#             values="Booked Room Revenue This Year",
#             aggfunc="sum"
#         ).sort_index()

#         st.line_chart(rev_pivot, use_container_width=True)

#         # Download revenue data
#         buffer = BytesIO()
#         rev_pivot.to_excel(buffer)
#         st.download_button(
#             "⬇ Download Revenue Graph Data (Excel)",
#             buffer.getvalue(),
#             file_name="revenue_vs_date.xlsx"
#         )

#         # =====================================================
#         # 🧮 DATE-WISE DISCREPANCY DRILL-DOWN
#         # =====================================================
#         st.subheader("🧮 Date-wise Discrepancy Drill-down")

#         level = st.selectbox(
#             "Select discrepancy level",
#             selected_sheets[1:]
#         )

#         metric = st.selectbox(
#             "Select metric",
#             metrics
#         )

#         prop_df = sheet_tables[base_sheet][
#             ["Occupancy Date", metric]
#         ].copy()

#         prop_df["Occupancy Date"] = pd.to_datetime(prop_df["Occupancy Date"])
#         prop_df = prop_df.groupby("Occupancy Date")[metric].sum().reset_index()

#         level_df = sheet_tables[level][
#             ["Occupancy Date", level, metric]
#         ].copy()

#         level_df["Occupancy Date"] = pd.to_datetime(level_df["Occupancy Date"])

#         level_agg = (
#             level_df
#             .groupby(["Occupancy Date", level])[metric]
#             .sum()
#             .reset_index()
#         )

#         merged = level_agg.merge(
#             prop_df,
#             on="Occupancy Date",
#             suffixes=("_Level", "_Property")
#         )

#         merged["Discrepancy"] = (
#             merged[f"{metric}_Level"] - merged[f"{metric}_Property"]
#         )

#         merged["Discrepancy %"] = (
#             merged["Discrepancy"] / merged[f"{metric}_Property"] * 100
#         ).round(2)

#         st.dataframe(merged, use_container_width=True)

# else:
#     st.info("Please upload a valid Excel file.")














# ----------------------------------------------------------------------------------------------------------------------------------------------




# import streamlit as st
# import pandas as pd
# from io import BytesIO

# st.set_page_config(layout="wide")
# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader("Upload FVR Excel File", type=["xlsx"])

# if uploaded_file:
#     excel = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets (Property first, then breakdown levels)",
#         excel.sheet_names
#     )

#     if len(selected_sheets) >= 2:
#         data = {s: pd.read_excel(uploaded_file, sheet_name=s) for s in selected_sheets}

#         base_sheet = selected_sheets[0]
#         compare_sheets = selected_sheets[1:]

#         metrics = [
#             "Occupancy On Books This Year",
#             "Booked Room Revenue This Year"
#         ]

#         # ===============================
#         # OVERALL DISCREPANCY (NO DATE)
#         # ===============================
#         st.subheader("Overall Percentage Discrepancy")

#         rows = []
#         for metric in metrics:
#             base_total = data[base_sheet][metric].sum()

#             for sheet in compare_sheets:
#                 comp_total = data[sheet][metric].sum()
#                 diff_pct = ((comp_total - base_total) / base_total) * 100

#                 rows.append({
#                     "Metric": metric,
#                     "Compared Level": sheet,
#                     "Property Total": round(base_total, 2),
#                     "Level Total": round(comp_total, 2),
#                     "Discrepancy %": round(diff_pct, 2)
#                 })

#         st.dataframe(pd.DataFrame(rows), use_container_width=True)

#         # ===============================
#         # LINE GRAPH – OCCUPANCY
#         # ===============================
#         st.subheader("Occupancy vs Date")

#         occ_frames = []
#         for name, df in data.items():
#             tmp = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
#             tmp["Occupancy Date"] = pd.to_datetime(tmp["Occupancy Date"])
#             tmp["Level"] = name
#             occ_frames.append(tmp)

#         occ_df = pd.concat(occ_frames)

#         occ_pivot = occ_df.pivot_table(
#             index="Occupancy Date",
#             columns="Level",
#             values="Occupancy On Books This Year",
#             aggfunc="sum"
#         ).sort_index()

#         st.line_chart(occ_pivot, use_container_width=True)

#         # ===============================
#         # LINE GRAPH – REVENUE
#         # ===============================
#         st.subheader("Revenue vs Date")

#         rev_frames = []
#         for name, df in data.items():
#             tmp = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
#             tmp["Occupancy Date"] = pd.to_datetime(tmp["Occupancy Date"])
#             tmp["Level"] = name
#             rev_frames.append(tmp)

#         rev_df = pd.concat(rev_frames)

#         rev_pivot = rev_df.pivot_table(
#             index="Occupancy Date",
#             columns="Level",
#             values="Booked Room Revenue This Year",
#             aggfunc="sum"
#         ).sort_index()

#         st.line_chart(rev_pivot, use_container_width=True)

#         # ===============================
#         # DRILL-DOWN DISCREPANCY
#         # ===============================
#         st.subheader("Discrepancy Drill-down")

#         level = st.selectbox("Select breakdown level", compare_sheets)
#         metric = st.selectbox("Select metric", metrics)

#         prop_df = data[base_sheet][["Occupancy Date", metric]].copy()
#         prop_df["Occupancy Date"] = pd.to_datetime(prop_df["Occupancy Date"])
#         prop_df = prop_df.groupby("Occupancy Date")[metric].sum().reset_index()

#         level_df = data[level][["Occupancy Date", level, metric]].copy()
#         level_df["Occupancy Date"] = pd.to_datetime(level_df["Occupancy Date"])

#         level_agg = (
#             level_df
#             .groupby(["Occupancy Date", level])[metric]
#             .sum()
#             .reset_index()
#         )

#         merged = level_agg.merge(
#             prop_df,
#             on="Occupancy Date",
#             how="left",
#             suffixes=("_Level", "_Property")
#         )

#         merged["Discrepancy"] = (
#             merged[f"{metric}_Level"] - merged[f"{metric}_Property"]
#         )

#         merged["Discrepancy %"] = (
#             merged["Discrepancy"] / merged[f"{metric}_Property"] * 100
#         ).round(2)

#         st.dataframe(merged, use_container_width=True)

#     else:
#         st.info("Select at least Property sheet + one breakdown sheet")

# else:
#     st.info("Upload an Excel file to begin")


# ----------------------------------------------------------------------------------------------------------------------------------------------




# import streamlit as st
# import pandas as pd
# from io import BytesIO

# st.set_page_config(layout="wide")
# st.title("Discrepancy Checker")

# uploaded_file = st.file_uploader("Upload FVR Excel File", type=["xlsx"])

# if uploaded_file:
#     excel = pd.ExcelFile(uploaded_file)

#     selected_sheets = st.multiselect(
#         "Select sheets (Property first)",
#         excel.sheet_names
#     )

#     if len(selected_sheets) >= 2:
#         data = {s: pd.read_excel(uploaded_file, sheet_name=s) for s in selected_sheets}

#         property_sheet = selected_sheets[0]
#         breakdown_sheets = selected_sheets[1:]

#         metrics = [
#             "Occupancy On Books This Year",
#             "Booked Room Revenue This Year"
#         ]

#         # =====================================================
#         # OVERALL DISCREPANCY SUMMARY
#         # =====================================================
#         st.subheader("Overall Discrepancy vs Property")

#         summary_rows = []

#         for metric in metrics:
#             prop_total = data[property_sheet][metric].sum()

#             for sheet in breakdown_sheets:
#                 level_total = data[sheet][metric].sum()
#                 diff_pct = ((level_total - prop_total) / prop_total) * 100

#                 summary_rows.append({
#                     "Metric": metric,
#                     "Breakdown Level": sheet,
#                     "Property Total": round(prop_total, 2),
#                     "Level Total": round(level_total, 2),
#                     "Discrepancy %": round(diff_pct, 2)
#                 })

#         st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)

#         # =====================================================
#         # GRAPHS (UNCHANGED)
#         # =====================================================
#         st.subheader("Occupancy vs Date")

#         occ_frames = []
#         for name, df in data.items():
#             tmp = df[["Occupancy Date", "Occupancy On Books This Year"]].copy()
#             tmp["Occupancy Date"] = pd.to_datetime(tmp["Occupancy Date"])
#             tmp["Level"] = name
#             occ_frames.append(tmp)

#         occ_df = pd.concat(occ_frames)

#         occ_pivot = occ_df.pivot_table(
#             index="Occupancy Date",
#             columns="Level",
#             values="Occupancy On Books This Year",
#             aggfunc="sum"
#         ).sort_index()

#         st.line_chart(occ_pivot, use_container_width=True)

#         st.subheader("Revenue vs Date")

#         rev_frames = []
#         for name, df in data.items():
#             tmp = df[["Occupancy Date", "Booked Room Revenue This Year"]].copy()
#             tmp["Occupancy Date"] = pd.to_datetime(tmp["Occupancy Date"])
#             tmp["Level"] = name
#             rev_frames.append(tmp)

#         rev_df = pd.concat(rev_frames)

#         rev_pivot = rev_df.pivot_table(
#             index="Occupancy Date",
#             columns="Level",
#             values="Booked Room Revenue This Year",
#             aggfunc="sum"
#         ).sort_index()

#         st.line_chart(rev_pivot, use_container_width=True)

#         # =====================================================
#         # CORRECT OVERALL DRILL-DOWN (NO DATE)
#         # =====================================================
#         st.subheader("Overall Discrepancy Drill-down (No Date)")

#         level_sheet = st.selectbox(
#             "Select breakdown level",
#             breakdown_sheets
#         )

#         level_column = level_sheet  # column name matches sheet name

#         unique_values = sorted(
#             data[level_sheet][level_column].dropna().unique()
#         )

#         selected_value = st.selectbox(
#             f"Select {level_column}",
#             unique_values
#         )

#         metric = st.selectbox(
#             "Select metric",
#             metrics
#         )

#         prop_total = data[property_sheet][metric].sum()

#         selected_total = data[level_sheet].loc[
#             data[level_sheet][level_column] == selected_value,
#             metric
#         ].sum()

#         discrepancy = selected_total - prop_total
#         discrepancy_pct = (discrepancy / prop_total) * 100 if prop_total != 0 else 0

#         st.metric(
#             label=f"{selected_value} vs Property ({metric})",
#             value=f"{round(discrepancy, 2)}",
#             delta=f"{round(discrepancy_pct, 2)} %"
#         )

#     else:
#         st.info("Select Property sheet + at least one breakdown sheet")

# else:
#     st.info("Upload an Excel file to begin")



# # ----------------------------------------------------------------------------------------------------------------------------------------------



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
        # 🔢 OVERALL DISCREPANCY (LEVEL vs PROPERTY)
        # =====================================================
        st.subheader("🔢 Overall Discrepancy")

        property_sheet = selected_sheets[0]

        breakdown_level = st.selectbox(
        "Select breakdown level",
        options=["Room Class", "Room Type", "Forecast Group", "Market Segment"]
        )

        metric = st.selectbox(
            "Select metric",
            [
                "Occupancy On Books This Year",
                "Booked Room Revenue This Year"
            ]
        )

        prop_total = sheet_tables[property_sheet][metric].sum()
        level_total = sheet_tables[breakdown_level][metric].sum()

        discrepancy = level_total - prop_total
        discrepancy_pct = (
            (discrepancy / prop_total) * 100 if prop_total != 0 else 0
        )

        st.metric(
            label=f"{breakdown_level} vs Property ({metric})",
            value=f"{discrepancy:,.2f}",
            delta=f"{discrepancy_pct:.2f} %"
        )

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
