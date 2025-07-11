import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def get_diagnostic_analytics_figures(df):
    figures = {}


    # Ensure 'TenureYears' and 'EngagementScore' are available
    if 'HireDate' in df.columns and 'TenureYears' not in df.columns:
        df['HireDate'] = pd.to_datetime(df['HireDate'])
        df['TenureYears'] = (pd.to_datetime('today') - df['HireDate']).dt.days / 365.25
    if 'EngagementScore' not in df.columns:
        df['EngagementScore'] = np.random.randint(60, 100, len(df)) 

    if 'Attrition' not in df.columns:
        df['Attrition'] = np.random.choice([0, 1], len(df), p=[0.9, 0.1]) 

    if 'Department' not in df.columns:
        df['Department'] = np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'], len(df)) 

    if 'EngagementScore' in df.columns and 'Department' in df.columns:
        fig_engagement = px.histogram(df, x='EngagementScore', color='Department',
                                      title='Engagement Score Distribution',
                                      labels={'EngagementScore': 'Engagement Score'},
                                      color_discrete_map={'Engineering': 'red', 'Sales': 'blue', 'Marketing': 'green', 'HR': 'purple', 'Finance': 'orange', 'Operations': 'brown'})
        figures["Engagement Score Distribution (Engineering vs. Others)"] = fig_engagement
    else:
        st.warning("Cannot generate 'Engagement Score Distribution' chart: 'EngagementScore' or 'Department' column missing.")

    if 'TenureYears' in df.columns and 'Attrition' in df.columns and 'Department' in df.columns:
        engineering_df = df[df['Department'] == 'Engineering']
        eng_attrition_df = engineering_df[engineering_df['Attrition'] == 1]
        if not eng_attrition_df.empty:
            fig_tenure_attrition = px.histogram(eng_attrition_df, x='TenureYears', nbins=10,
                                                title='Tenure of Employees with Attrition (Engineering)',
                                                labels={'TenureYears': 'Tenure (Years)'},
                                                color_discrete_sequence=px.colors.qualitative.Set1)
            figures["Tenure of Employees with Attrition (Engineering)"] = fig_tenure_attrition
        else:
            st.info("No attrition cases in Engineering department to plot tenure distribution.")
    else:
        st.warning("Cannot generate 'Tenure for Attrition Cases' chart: Required columns missing.")

    return figures

def display_diagnostic_analytics_page(df):
    st.set_page_config(page_title="Diagnostic Analytics")
    st.header("Diagnostic Analytics: Identifying Root Causes")
    st.markdown("""
    Beyond surface-level metrics, Apexon Pulse's `InsightExplorerAgent` helps identify the root causes behind trends,
    enabling proactive problem-solving.
    """)

    st.subheader("Case Study: High Attrition in Engineering Department")
    st.info("Apexon Pulse detects an anomaly: The Engineering department shows a significantly higher attrition rate.")

    if 'Department' in df.columns and 'Attrition' in df.columns:
        engineering_df = df[df['Department'] == 'Engineering']
        total_eng = engineering_df.shape[0]
        attrition_eng = engineering_df['Attrition'].sum()
        attrition_rate_eng = (attrition_eng / total_eng) * 100 if total_eng > 0 else 0

        st.markdown(f"""
        * **Engineering Department Attrition Rate:** **{attrition_rate_eng:.1f}%**
        * **Overall Company Attrition Rate:** **{(df['Attrition'].sum() / df.shape[0]) * 100:.1f}%**
        """)
    else:
        st.warning("Cannot calculate attrition rates: 'Department' or 'Attrition' column missing.")


    st.markdown("""
    The `DiagnosticAgent` then drills down to identify contributing factors:
    """)

    # Get and display figures
    figures = get_diagnostic_analytics_figures(df)
    col1, col2 = st.columns(2)
    with col1:
        if "Engagement Score Distribution (Engineering vs. Others)" in figures:
            st.subheader("Engagement Score Distribution (Engineering vs. Others)")
            st.plotly_chart(figures["Engagement Score Distribution (Engineering vs. Others)"], use_container_width=True)
            st.markdown("""
            * **Insight:** Engineering employees with attrition often show lower engagement scores.
            """)
    with col2:
        if "Tenure of Employees with Attrition (Engineering)" in figures:
            st.subheader("Tenure for Attrition Cases (Engineering)")
            st.plotly_chart(figures["Tenure of Employees with Attrition (Engineering)"], use_container_width=True)
            st.markdown("""
            * **Insight:** A significant portion of attrition in Engineering occurs within the 1-3 year tenure range.
            """)

    st.markdown("""
    **Apexon Pulse's Recommendations for Engineering:**
    * Implement targeted retention programs for employees in their early career stages.
    * Conduct deeper surveys to understand specific pain points affecting engagement in Engineering.
    * Review workload and career development opportunities within the department.
    """)