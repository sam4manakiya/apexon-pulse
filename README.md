Apexon Pulse: AI-Driven Employee Analytics
Apexon Pulse is a powerful, AI-driven HR analytics application built with Streamlit, designed to provide comprehensive insights into employee data and automate analytical workflows for proactive strategic decision-making within our organization.


Table of Contents
Features

Technologies Used

Project Structure

How to Run the App

Usage

Internal Support & Contact

Contributing

Acknowledgments


Features

Apexon Pulse offers:

Data Ingestion: Load from project CSV or upload new CSV.

Descriptive Analytics: Snapshot of key workforce metrics and demographics.

Diagnostic Analytics: Identifies root causes of HR trends (e.g., attrition) with insights.

Predictive Analytics: Simulates attrition risk forecasting to identify high-risk employees.

Automated Reporting: Consolidates all analysis with charts and tables, offering PDF report download.


Technologies Used

Python 3.x

Streamlit: Interactive web applications.

Pandas: Data manipulation.

Plotly Express: Interactive charts.

fpdf2 & Kaleido: PDF generation.

streamlit-option-menu: Enhanced navigation.


Project Structure

apexon-pulse/
├── app.py                      # Main application & entry point
├── data_utils.py               # Dummy data generation
├── EDA_functions.py            # Descriptive Analytics logic
├── diagnostic_functions.py     # Diagnostic Analytics logic
├── predictive_functions.py     # Predictive Analytics logic
├── report_generation.py        # Report generation (mock & PDF)
├── utils.py                    # General utilities
├── employee_data.csv           # Sample data
├── Images/                     # Application images
│   ├── logo.jpg
│   └── heroimage.png
└── README.md                   # This README file


How to Run the App

Clone the Repository:

git clone https://bitbucket.org/YOUR_BITBUCKET_ORG/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME


Install Dependencies:

pip install streamlit pandas numpy plotly fpdf2 kaleido streamlit-option-menu


Run:

streamlit run app.py


This will open the application in your default web browser.


Usage

Navigation: Use the sidebar menu to switch between sections.

Data Ingestion: Load sample CSV or upload your own. Click "Generate Analysis" to prepare data.

Analytics Pages: View interactive charts and insights based on loaded data.

Automated Reporting: See consolidated analysis and download a full PDF report.


Internal Support & Contact

For any issues, questions, or feature requests:

Raise a ticket: [Link to your internal ticketing system, e.g., Jira, ServiceNow]

Contact the development team: [Email address or internal chat channel/group name]

Refer to internal documentation: [Link to Confluence, SharePoint, or other internal wiki]


Contributing

Contributions from internal teams are highly encouraged!

Bug Reports: Raise a ticket in our [internal ticketing system].

Feature Requests: Submit via [internal ticketing system] or [team chat channel].

Code Contributions: Fork the repo, create a feature branch, commit changes, push to your fork, and create a Pull Request (PR) to main.


Acknowledgments

Developed by The Mavericks team.

Powered by Streamlit, Pandas, Plotly, and fpdf2.