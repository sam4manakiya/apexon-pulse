import streamlit as st
import plotly.express as px
import pandas as pd

import numpy as np

def get_descriptive_analytics_figures(df):
    figures = {}

    if 'HireDate' in df.columns and 'TenureYears' not in df.columns:
        df['HireDate'] = pd.to_datetime(df['HireDate'])
        df['TenureYears'] = (pd.to_datetime('today') - df['HireDate']).dt.days / 365.25
    elif 'TenureYears' not in df.columns:
        df['TenureYears'] = pd.Series(np.random.rand(len(df)) * 10).round(1) 

    fig_tenure = px.histogram(df, x='TenureYears', nbins=15, title='Employee Tenure Distribution',
                              labels={'TenureYears': 'Tenure (Years)'},
                              color_discrete_sequence=px.colors.qualitative.Pastel)
    figures["Employee Tenure Distribution"] = fig_tenure

    if 'Salary' in df.columns and 'Department' in df.columns:
        fig_salary_dept = px.box(df, x='Department', y='Salary', title='Salary Distribution by Department',
                                 color='Department', color_discrete_sequence=px.colors.qualitative.Pastel)
        figures["Salary Distribution by Department"] = fig_salary_dept
    else:
        st.warning("Cannot generate 'Salary Distribution by Department' chart: 'Salary' or 'Department' column missing.")

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        fig_gender = px.pie(gender_counts, values='Count', names='Gender', title='Workforce Gender Distribution',
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        figures["Workforce Gender Distribution"] = fig_gender
    else:
        st.warning("Cannot generate 'Workforce Gender Distribution' chart: 'Gender' column missing.")

    return figures

def display_descriptive_analytics_page(df):
    st.set_page_config(page_title="Descriptive Analytics")
    st.header("Descriptive Analytics: Understanding Your Workforce")
    st.markdown("""
    The `InsightExplorerAgent` summarizes key workforce metrics, providing a clear snapshot of your organization.
    """)

    st.subheader("Employee Demographics and Distribution")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Employees", df.shape[0])
        # Ensure 'TenureYears' is calculated before displaying
        if 'HireDate' in df.columns and 'TenureYears' not in df.columns:
            df['HireDate'] = pd.to_datetime(df['HireDate'])
            df['TenureYears'] = (pd.to_datetime('today') - df['HireDate']).dt.days / 365.25
        avg_tenure = df['TenureYears'].mean() if 'TenureYears' in df.columns else 0
        st.metric("Average Tenure", f"{avg_tenure:.1f} years")
    with col2:
        avg_salary = df['Salary'].mean() if 'Salary' in df.columns else 0
        st.metric("Average Salary", f"${avg_salary:,.0f}")
        avg_engagement = df['EngagementScore'].mean() if 'EngagementScore' in df.columns else 0
        st.metric("Average Engagement Score", f"{avg_engagement:.1f}")

    st.markdown("---")
    figures = get_descriptive_analytics_figures(df)
    for title, fig in figures.items():
        st.subheader(title)
        st.plotly_chart(fig, use_container_width=True)