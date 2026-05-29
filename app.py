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

Strategic Student Success Indicators:

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

    total_students = len(df)

    total_variables = len(df.columns)

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
        total_students
    )

    col2.metric(
        "Variables",
        total_variables
    )

    col3.metric(
        "Data Completeness",
        f"{completeness}%"
    )

    st.divider()

    # =====================================================
    # HELPER FUNCTIONS
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

        total_row = pd.DataFrame({
            "Response": ["TOTAL"],
            "Frequency": [freq["Frequency"].sum()],
            "Percentage": [100.0]
        })

        freq = pd.concat(
            [freq, total_row],
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
            height=550,
            showlegend=False
        )

        return fig

    st.success(
        "Part 1A loaded successfully."
    )
        # =====================================================
    # DATASET DIAGNOSTICS
    # =====================================================

    st.header("Dataset Diagnostics")

    st.write("Checking Strategic Indicator Variables")

    first_generation_column = (
        "25. Have any of your close family members attended university?"
    )

    rural_urban_column = (
        "27. How would you describe the place in which your home is situated?"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write("First Generation Variable Found:")

        st.write(
            first_generation_column in df.columns
        )

    with col2:

        st.write("Rural/Urban Variable Found:")

        st.write(
            rural_urban_column in df.columns
        )

    st.divider()

    # =====================================================
    # FIRST-GENERATION UNIVERSITY STUDENTS
    # =====================================================

    if first_generation_column in df.columns:

        st.header(
            "First-Generation University Students"
        )

        freq = create_profile_table(
            df,
            first_generation_column
        )

        left, right = st.columns([1, 2])

        with left:

            st.dataframe(
                freq,
                use_container_width=True
            )

            download_table(
                freq,
                "First_Generation_Students.csv",
                "📥 Download First-Generation Student Data"
            )

        with right:

            fig = executive_chart(
                freq,
                "First-Generation University Students (%)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    # =====================================================
    # RURAL VS URBAN BACKGROUND
    # =====================================================

    if rural_urban_column in df.columns:

        st.header(
            "Rural versus Urban Background"
        )

        freq = create_profile_table(
            df,
            rural_urban_column
        )

        left, right = st.columns([1, 2])

        with left:

            st.dataframe(
                freq,
                use_container_width=True
            )

            download_table(
                freq,
                "Rural_Urban_Background.csv",
                "📥 Download Rural versus Urban Data"
            )

        with right:

            fig = executive_chart(
                freq,
                "Rural versus Urban Background (%)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    st.success(
        "Part 1B loaded successfully."
    )

else:

    st.info(
        "Please upload the FTEN Biographical Questionnaire dataset."
    )
