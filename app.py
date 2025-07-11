import streamlit as st
import pandas as pd
import base64
import os
from data_utils import generate_dummy_data
from EDA_functions import display_descriptive_analytics_page, get_descriptive_analytics_figures    
from diagnostic_functions import display_diagnostic_analytics_page, get_diagnostic_analytics_figures
from predictive_functions import display_predictive_analytics_page, get_predictive_analytics_figures
from report_generation import generate_full_report_pdf
from Data_Inegestion import dispaly_data_ingestion
from utils import display_footer
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Apexon Pulse",
    page_icon="Images/logo.jpg",  
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.apexon.com/contact',
        'Report a Bug': 'https://github.com/yourusername/yourrepo/issues',
        'About': """
        # Apexon Pulse
        This is a demo application showcasing AI-driven employee analytics by **The Mavericks**.
        Version: 1.0.0
        """
    }
)

header_col1, header_col2 = st.columns([0.15, 0.85]) 

with header_col1:
    logo_path = "Images/logo.jpg"
    try:
        st.image(logo_path, width=100)  # Adjust width for main header logo
    except FileNotFoundError:
        st.warning(f"Main logo image not found at '{logo_path}'. Please ensure 'logo.jpg' is in the same directory.")
        st.image("https://placehold.co/100x30/ADD8E6/000000?text=Logo+Missing", width=100)

with header_col2:
    st.title("Apexon Pulse: AI-Driven Employee Analytics")

st.markdown("""
Welcome to the interactive demo of **Apexon Pulse**, a revolutionary system designed to transform HR with AI-driven insights.
This demonstration simulates how Apexon Pulse leverages your employee data to provide comprehensive analytics,
predict future trends, and automate reporting.
""")

with st.sidebar:
    page = option_menu(
        menu_title="Navigation", 
        options=["Home", "Data Ingestion", "Descriptive Analytics", "Diagnostic Analytics", "Predictive Analytics", "Automated Reporting"],  # required
        icons=["house", "cloud-upload", "bar-chart", "search", "graph-up", "file-earmark-text"], 
        menu_icon="cast",  
        default_index=0,  
        orientation="vertical",
    )

    st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 280px;
            max-width: 350px;
        }
    </style>
    """,
    unsafe_allow_html=True
    )
    if 'employee_data' not in st.session_state or st.session_state['employee_data'] is None:
        st.session_state['employee_data'] = generate_dummy_data()

if page == "Home":
    st.header("Transforming HR with AI-Driven Employee Analytics")
    hero_image_path = "Images/heroimage.png"
    try:
        st.image(hero_image_path, caption="Apexon Pulse: AI-Driven HR Transformation", use_container_width=True)
    except FileNotFoundError:
        st.warning(f"Hero image not found at '{hero_image_path}'. Please ensure 'heroimage.png' is in the same directory.")
        st.image("https://placehold.co/1200x400/ADD8E6/000000?text=Hero+Image+Missing", caption="Placeholder Image", use_column_width=True)

    st.markdown("""
    The modern workforce faces challenges like fragmented HR data, manual analysis, and reactive decision-making.
    Apexon Pulse addresses these by providing deep insights into employee data, automating workflows, and enabling proactive strategies.

    Explore the different sections using the navigation bar on the left.
    """)
    display_footer()

elif page == "Data Ingestion":
    dispaly_data_ingestion(st.session_state['employee_data'])
    display_footer()

elif page == "Descriptive Analytics":
    display_descriptive_analytics_page(st.session_state['employee_data'])
    display_footer()

elif page == "Diagnostic Analytics":
    display_diagnostic_analytics_page(st.session_state['employee_data'])
    display_footer()

elif page == "Predictive Analytics":
    display_predictive_analytics_page(st.session_state['employee_data'])
    display_footer()

elif page == "Automated Reporting":
    st.header("Automated Reporting & Distribution")
    st.markdown("""
    The `ReportSynthesizerAgent` compiles clear, actionable reports with integrated charts and professional formatting,
    and the system automates their distribution.
    """)

    st.subheader("HR Quarterly Review Report - Q2 2025")

    # Display all analysis sections with charts directly on the page
    st.markdown("### 1. Descriptive Analytics")
    desc_figs = get_descriptive_analytics_figures(st.session_state['employee_data'])
    for title, fig in desc_figs.items():
        st.subheader(title)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 2. Diagnostic Analytics")
    diag_figs = get_diagnostic_analytics_figures(st.session_state['employee_data'])
    for title, fig in diag_figs.items():
        st.subheader(title)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    **Apexon Pulse's Recommendations for Engineering:**
    * Implement targeted retention programs for employees in their early career stages.
    * Conduct deeper surveys to understand specific pain points affecting engagement in Engineering.
    * Review workload and career development opportunities within the department.
    """)

    st.markdown("### 3. Predictive Analytics")
    pred_figs, top_risks_df = get_predictive_analytics_figures(st.session_state['employee_data'])
    for title, fig in pred_figs.items():
        st.subheader(title)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### Top 20 Employees with Highest Attrition Risk:")
    st.dataframe(top_risks_df)
    st.markdown("""
    **How this supports Strategic Planning:**
    * **Proactive Talent Retention:** Identify high-risk employees and intervene with targeted programs (mentorship, skill development, workload rebalancing).
    * **Optimized Workforce Planning:** Anticipate future staffing needs and address potential skill gaps before they become critical.
    * **Strategic Resource Allocation:** Align compensation and rewards to attract and retain top talent, based on predictive insights.
    """)

    st.markdown("---")
    st.subheader("Generate and Download Report")

    # NEW: Add the download PDF button
    if st.button("Download Full Report (PDF)"):
        with st.spinner("Generating PDF report... This may take a moment."):
            pdf_bytes = generate_full_report_pdf(st.session_state['employee_data'])
            if pdf_bytes:
                st.download_button(
                    label="Click to Download PDF",
                    data=pdf_bytes,
                    file_name="HR_Quarterly_Review_Report.pdf",
                    mime="application/pdf"
                )
                st.success("PDF report generated and ready for download!")
            else:
                st.error("Failed to generate PDF report.")

    st.markdown("""
    **Benefits of Automated Reporting:**
    * **Time-Saving:** Eliminates manual report generation, freeing up HR teams.
    * **Consistency:** Ensures standardized, professional reports every time.
    * **Timely Insights:** Stakeholders receive critical information promptly.
    * **Seamless Distribution:** Reports are automatically shared through Teams channels, Outlook, and SharePoint uploads.
    """)
    display_footer() 