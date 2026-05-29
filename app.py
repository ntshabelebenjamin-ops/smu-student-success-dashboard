import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="SMU Student Success Risk Dashboard 2025",
    layout="wide"
)

# =====================================================
# DASHBOARD TITLE
# =====================================================

st.title(
    "SMU Student Success Risk and Vulnerability Dashboard: 2025 FTEN Cohort"
)

st.caption(
    "Prepared by Benjamin Ntshabele | Institutional Planning and Quality Assurance | SMU"
)

st.markdown("""
This dashboard provides an executive-level analysis of student success risk factors among the 2025 First-Time Entering Students (FTEN) cohort.

The dashboard focuses on:

• First-Generation University Students

• Rural versus Urban Background

• Financial Vulnerability and NSFAS Dependency

• Language Diversity and Schooling Background

• Family Responsibilities

• Commuting Challenges
""")

st.divider()

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload FTEN Biographical Questionnaire Dataset",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)

    # =====================================================
    # EXECUTIVE OVERVIEW
    # =====================================================

    st.header("Executive Overview")

    total_cells = df.shape[0] * df.shape[1]

    completeness = round(
        (
            1 -
            (
                df.isnull().sum().sum() /
                total_cells
            )
        ) * 100,
        1
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "FTEN Students",
        len(df)
    )

    col2.metric(
        "Variables",
        len(df.columns)
    )

    col3.metric(
        "Data Completeness",
        f"{completeness}%"
    )

    st.divider()

    # =====================================================
    # HELPER FUNCTION
    # =====================================================

    def create_profile_table(
        dataframe,
        column_name
    ):

        freq = (
            dataframe[column_name]
            .fillna("Missing")
            .value_counts()
            .reset_index()
        )

        freq.columns = [
            "Response",
            "Frequency"
        ]

        freq["Percentage"] = round(
            freq["Frequency"] /
            freq["Frequency"].sum() * 100,
            1
        )

        total = pd.DataFrame({
            "Response": ["TOTAL"],
            "Frequency": [freq["Frequency"].sum()],
            "Percentage": [100.0]
        })

        freq = pd.concat(
            [freq, total],
            ignore_index=True
        )

        return freq

    def download_table(
        dataframe,
        filename,
        button_text
    ):

        csv = dataframe.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label=button_text,
            data=csv,
            file_name=filename,
            mime="text/csv"
        )

    def executive_chart(
        freq,
        title
    ):

        chart_data = freq[
            freq["Response"] != "TOTAL"
        ]

        fig = px.bar(
            chart_data,
            y="Response",
            x="Percentage",
            orientation="h",
            text="Percentage"
        )

        fig.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside"
        )

        fig.update_layout(

            title={
                "text": title,
                "font": {
                    "size": 16
                }
            },

            font={
                "size": 14
            },

            xaxis_title="Percentage (%)",
            yaxis_title="",

            plot_bgcolor="white",
            paper_bgcolor="white",

            height=500,

            showlegend=False
        )

        return fig

    st.success(
        "Dataset uploaded successfully. Proceed to Part 1B."
    )
