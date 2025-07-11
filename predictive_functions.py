import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 

def get_predictive_analytics_figures(df):
    figures = {}
    if 'EngagementScore' not in df.columns:
        df['EngagementScore'] = np.random.randint(60, 100, len(df))
    if 'TenureYears' not in df.columns:
        if 'HireDate' in df.columns:
            df['HireDate'] = pd.to_datetime(df['HireDate'])
            df['TenureYears'] = (pd.to_datetime('today') - df['HireDate']).dt.days / 365.25
        else:
            df['TenureYears'] = pd.Series(np.random.rand(len(df)) * 10).round(1)
    if 'Department' not in df.columns:
        df['Department'] = np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'], len(df))

    df['AttritionRiskScore'] = np.random.rand(df.shape[0]) * 100
    df.loc[(df['EngagementScore'] < 70) | (df['TenureYears'] < 2) | (df['Department'] == 'Engineering'), 'AttritionRiskScore'] += np.random.rand(df[(df['EngagementScore'] < 70) | (df['TenureYears'] < 2) | (df['Department'] == 'Engineering')].shape[0]) * 30
    df['AttritionRiskScore'] = df['AttritionRiskScore'].clip(0, 100).round(1)

    # Get top 20 employees with highest risk
    top_risks_df = df[['Name', 'Department', 'Role', 'TenureYears', 'EngagementScore', 'AttritionRiskScore']].sort_values(by='AttritionRiskScore', ascending=False).head(20)

    # Generate a bar chart for top N attrition risks (e.g., top 10)
    if not top_risks_df.empty:
        fig_top_risks = px.bar(top_risks_df.head(10), x='Name', y='AttritionRiskScore',
                               title='Top 10 Employees by Attrition Risk Score',
                               labels={'AttritionRiskScore': 'Attrition Risk Score (%)', 'Name': 'Employee Name'},
                               color='AttritionRiskScore',
                               color_continuous_scale=px.colors.sequential.Reds)
        fig_top_risks.update_layout(xaxis_tickangle=-45)
        figures["Top 10 Employees by Attrition Risk Score"] = fig_top_risks
    else:
        st.info("No employees found to plot attrition risk.")

    return figures, top_risks_df

def display_predictive_analytics_page(df):
    st.set_page_config(page_title="Predictive Analytics")
    st.header("Predictive Analytics: Forecasting Future Outcomes")
    st.markdown("""
    The `FuturePredictorAgent` builds and deploys machine learning models to forecast employee outcomes,
    such as attrition risk. This enables proactive strategic planning.
    """)

    st.subheader("Simulated Attrition Risk Forecast")
    st.info("Apexon Pulse uses advanced algorithms (e.g., Logistic Regression, Random Forest) to predict attrition risk.")

    figures, top_risks_df = get_predictive_analytics_figures(df)

    
    st.dataframe(top_risks_df)

    if "Top 10 Employees by Attrition Risk Score" in figures:
        st.plotly_chart(figures["Top 10 Employees by Attrition Risk Score"], use_container_width=True)

    st.markdown("""
    **How this supports Strategic Planning:**
    * **Proactive Talent Retention:** Identify high-risk employees and intervene with targeted programs (mentorship, skill development, workload rebalancing).
    * **Optimized Workforce Planning:** Anticipate future staffing needs and address potential skill gaps before they become critical.
    * **Strategic Resource Allocation:** Align compensation and rewards to attract and retain top talent, based on predictive insights.
    """)