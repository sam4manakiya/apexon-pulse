from fpdf import FPDF 
import io
import os
import tempfile
import plotly.io as pio 

from EDA_functions import get_descriptive_analytics_figures
from diagnostic_functions import get_diagnostic_analytics_figures
from predictive_functions import get_predictive_analytics_figures


def generate_mock_report():
    report_content = """
    # HR Quarterly Performance Review - Q2 2025

    ## Executive Summary
    This report provides an overview of key HR metrics and trends for the second quarter of 2025, leveraging insights from Apexon Pulse. Our focus remains on optimizing workforce productivity, enhancing employee engagement, and mitigating attrition risks.

    ## Workforce Overview
    * **Total Employees:** 1,000
    * **Average Tenure:** 4.5 years
    * **Gender Distribution:** 48% Male, 48% Female, 4% Non-binary
    * **Average Salary:** $70,000

    ## Key Highlights
    * **Employee Engagement:** Overall engagement scores remain strong at an average of 85. However, a slight dip was observed in the Engineering department, prompting further investigation.
    * **Talent Acquisition:** Successfully onboarded 50 new employees this quarter, with a focus on critical roles in Sales and Product Development.
    * **Performance:** 75% of employees received a 'Meets Expectations' or 'Exceeds Expectations' rating in the recent performance cycle.

    ## Attrition Analysis (Powered by Predictive Analytics)
    Apexon Pulse's predictive models indicate a projected attrition rate of 12% for the upcoming quarter. Key factors contributing to higher attrition risk include:
    * Employees with tenure between 1-2 years.
    * Individuals with an engagement score below 70.
    * Specific roles within the Engineering department.

    **Recommendations:**
    1.  Implement targeted mentorship programs for employees in their first two years.
    2.  Conduct engagement surveys and focus groups in the Engineering department to address specific concerns.
    3.  Review compensation and career pathing for high-risk roles.

    ## Automated Report Distribution
    This report was automatically generated by the `ReportSynthesizerAgent` and distributed to relevant stakeholders via Teams, Outlook, and SharePoint.

    ---
    *Generated by Apexon Pulse - July 10, 2025*
    """
    return report_content

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Apexon Pulse: HR Quarterly Review Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln(5)

    def add_chart(self, fig, title, width=180):
        """Adds a Plotly figure to the PDF."""
        self.chapter_title(title)
        # Save Plotly figure to a temporary image file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            img_path = tmpfile.name
            pio.write_image(fig, img_path, format='png', width=800, height=500, scale=1) # Adjust width/height/scale as needed

        # Add image to PDF
        self.image(img_path, x=self.get_x() + 10, w=width) # Adjust x to center, w for width
        self.ln(5) # Add some space after the image

        # Clean up temporary image file
        os.unlink(img_path)


def generate_full_report_pdf(df):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.chapter_title("Executive Summary")
    summary_text = """
    This report provides an overview of key HR metrics and trends for the second quarter of 2025, leveraging insights from Apexon Pulse. Our focus remains on optimizing workforce productivity, enhancing employee engagement, and mitigating attrition risks.
    """
    pdf.chapter_body(summary_text)

    # --- Workforce Overview ---
    pdf.chapter_title("Workforce Overview")
    total_employees = df.shape[0]
    avg_tenure = df['TenureYears'].mean() if 'TenureYears' in df.columns else 0
    avg_salary = df['Salary'].mean() if 'Salary' in df.columns else 0
    avg_engagement = df['EngagementScore'].mean() if 'EngagementScore' in df.columns else 0

    workforce_overview_text = f"""
    * Total Employees: {total_employees:,}
    * Average Tenure: {avg_tenure:.1f} years
    * Average Salary: ${avg_salary:,.0f}
    * Average Engagement Score: {avg_engagement:.1f}
    """
    pdf.chapter_body(workforce_overview_text)


    # --- Descriptive Analytics ---
    pdf.chapter_title("1. Descriptive Analytics")
    desc_figs = get_descriptive_analytics_figures(df)
    for title, fig in desc_figs.items():
        pdf.add_chart(fig, title)
        pdf.ln(5) # Add some space between charts

    # --- Diagnostic Analytics ---
    pdf.chapter_title("2. Diagnostic Analytics")
    diag_figs = get_diagnostic_analytics_figures(df)

    # Attrition rates text
    if 'Department' in df.columns and 'Attrition' in df.columns:
        engineering_df = df[df['Department'] == 'Engineering']
        total_eng = engineering_df.shape[0]
        attrition_eng = engineering_df['Attrition'].sum()
        attrition_rate_eng = (attrition_eng / total_eng) * 100 if total_eng > 0 else 0
        overall_attrition_rate = (df['Attrition'].sum() / df.shape[0]) * 100 if df.shape[0] > 0 else 0

        pdf.chapter_body(f"""
        Apexon Pulse detects an anomaly: The Engineering department shows a significantly higher attrition rate.
        * Engineering Department Attrition Rate: {attrition_rate_eng:.1f}%
        * Overall Company Attrition Rate: {overall_attrition_rate:.1f}%
        The DiagnosticAgent then drills down to identify contributing factors:
        """)
    else:
        pdf.chapter_body("Diagnostic analytics insights could not be fully generated due to missing data.")


    for title, fig in diag_figs.items():
        pdf.add_chart(fig, title)
        pdf.ln(5)

    pdf.chapter_body("""
    **Apexon Pulse's Recommendations for Engineering:**
    * Implement targeted retention programs for employees in their early career stages.
    * Conduct deeper surveys to understand specific pain points affecting engagement in Engineering.
    * Review workload and career development opportunities within the department.
    """)

    # --- Predictive Analytics ---
    pdf.chapter_title("3. Predictive Analytics")
    pred_figs, top_risks_df = get_predictive_analytics_figures(df)

    pdf.chapter_body("""
    The `FuturePredictorAgent` builds and deploys machine learning models to forecast employee outcomes,
    such as attrition risk. This enables proactive strategic planning.
    """)

    if not top_risks_df.empty:
        pdf.chapter_body("Top 20 Employees with Highest Attrition Risk:")
        pdf.set_font('Arial', '', 8) # Keep font at 8 for the table
        available_width = pdf.w - pdf.l_margin - pdf.r_margin

        df_str = top_risks_df.to_string(index=False, max_colwidth=int(available_width / (pdf.font_size / 3)))

        # Split into lines and add to PDF, using the calculated available_width
        for line in df_str.split('\n'):
            
            pdf.multi_cell(available_width, 4, line)
        pdf.ln(5)
        pdf.set_font('Arial', '', 10) # Reset font to default for subsequent content

    for title, fig in pred_figs.items():
        pdf.add_chart(fig, title)
        pdf.ln(5)

    pdf.chapter_body("""
    **How this supports Strategic Planning:**
    * **Proactive Talent Retention:** Identify high-risk employees and intervene with targeted programs (mentorship, skill development, workload rebalancing).
    * **Optimized Workforce Planning:** Anticipate future staffing needs and address potential skill gaps before they become critical.
    * **Strategic Resource Allocation:** Align compensation and rewards to attract and retain top talent, based on predictive insights.
    """)

    # --- Conclusion ---
    pdf.chapter_title("Conclusion and Automated Distribution")
    pdf.chapter_body("""
    This report was automatically generated by the `ReportSynthesizerAgent` and is designed for seamless distribution to relevant stakeholders via Teams, Outlook, and SharePoint.
    """)

    return bytes(pdf.output(dest='S')) 