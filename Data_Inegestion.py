import streamlit as st
import pandas as pd
import os 
from data_utils import generate_dummy_data 

def dispaly_data_ingestion(df):
    st.set_page_config(page_title="Data Ingestion")
   # ... (rest of your app.py code above this block) ..
    st.subheader("Load Data from Project Folder or Upload CSV")
    st.info("This section allows you to load employee data from a CSV file located in your project directory or upload a new CSV.")

    csv_file_path = "Data/employee_data.csv" 

    # Add a button to trigger data loading and display from project folder
    if st.button("Preview Data from Project CSV"):
        if os.path.exists(csv_file_path):
            try:
                df_loaded = pd.read_csv(csv_file_path)
                st.success(f"Data loaded successfully from '{csv_file_path}'!")
                st.markdown("Here's a preview of the data loaded from your project CSV:")
                st.dataframe(df_loaded.head(500))
                st.session_state['employee_data'] = df_loaded 
            except Exception as e:
                st.error(f"Error reading CSV file '{csv_file_path}': {e}")
                st.markdown("Please ensure the CSV file is correctly formatted and accessible.")
                st.session_state['employee_data'] = generate_dummy_data() # Fallback to dummy data on error
        else:
            st.warning(f"CSV file not found at '{csv_file_path}'. Please ensure the file exists in your project directory.")
            st.markdown("As a fallback, here's a preview of *simulated* employee data:")
            df_simulated = generate_dummy_data()
            st.dataframe(df_simulated.head(10))
            st.session_state['employee_data'] = df_simulated # Store fallback data
    else:
        st.markdown("Click the button above to load and preview data from the project CSV file.")

    st.markdown("---")
    st.subheader("Generate Analysis")
    if st.button("Generate Analysis"):
        if st.session_state['employee_data'] is not None and not st.session_state['employee_data'].empty:
            st.success("Data is ready! Navigate to 'Descriptive Analytics', 'Diagnostic Analytics', or 'Predictive Analytics' to view the analysis.")
            st.balloons() # A little visual flair
        else:
            st.warning("Please load data first using the options above before generating analysis.")


    st.markdown("""
    ---
    **Key Capabilities of Data Ingestion:**
    * **Automated Data Fetching:** Pulls Excel files directly from SharePoint/OneDrive via Microsoft Graph API.
    * **Data Cleaning & Standardization:** Handles missing values, inconsistencies, and formats data for analysis.
    * **Secure Ingestion:** Ensures data privacy and compliance during the ingestion process.
    """)