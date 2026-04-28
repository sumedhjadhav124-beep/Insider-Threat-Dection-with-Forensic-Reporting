from fpdf import FPDF
import os

class OverviewPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'ITD.CORE - Insider Threat Detection Platform', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Project Overview & Architecture Summary', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, f'  {title}', 0, 1, 'L', fill=True)
        self.ln(4)

    def section_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(6)

    def bullet_point(self, point):
        self.set_font('Arial', '', 11)
        self.cell(5, 6, "-", 0, 0)
        self.multi_cell(0, 6, point)
        self.ln(2)

def generate_pdf():
    pdf = OverviewPDF()
    pdf.add_page()

    pdf.section_title('1. Executive Summary')
    pdf.section_body(
        "The Insider Threat Detection (ITD.CORE) Platform is a production-ready, SOC-style cybersecurity "
        "application designed to monitor internal activities, detect anomalous behavior using AI (Isolation Forest), "
        "and generate investigation-ready forensic reports. It employs a Zero-Trust approach to identify logic bombs, "
        "data exfiltration, and unauthorized access by employees in real time."
    )

    pdf.section_title('2. Core Features & Capabilities')
    pdf.bullet_point("Real-Time Activity Stream: Live logging of all user actions including login/logout events, file access, and page navigation.")
    pdf.bullet_point("AI Anomaly Detection: Utilizes an Isolation Forest machine learning model to score actions and flag deviations from baseline behavior.")
    pdf.bullet_point("Dynamic Risk Scoring: Users maintain a dynamic risk score that fluctuates based on detected anomalies, helping analysts prioritize high-risk profiles.")
    pdf.bullet_point("Forensic Case Management: Converts automated alerts into structured investigation cases where SOC analysts can track status, update notes, and take action.")
    pdf.bullet_point("Immutable Forensic Vault: Automatically generates and stores cryptographically hashed evidence reports as PDFs, maintaining a strict chain of custody.")
    pdf.bullet_point("Employee Portal: Functions as the monitored 'stealth' interface where employees interact with company files, unaware of the deep telemetry happening in the background.")
    pdf.ln(4)

    pdf.section_title('3. Technology Stack')
    pdf.bullet_point("Backend: Python 3, Flask framework for robust API and routing capabilities.")
    pdf.bullet_point("Frontend: HTML5, Tailwind CSS, Javascript, offering a premium dark-themed cyber aesthetic.")
    pdf.bullet_point("Real-Time Engine: Flask-SocketIO (WebSockets) for pushing live telemetry and alerts to the SOC dashboard.")
    pdf.bullet_point("Machine Learning: Scikit-learn (Isolation Forest) for rapid anomaly scoring.")
    pdf.bullet_point("Database: SQLite structured via SQLAlchemy ORM for relational persistence.")
    pdf.bullet_point("Reporting: FPDF library for dynamic generation of forensic evidence PDFs.")
    pdf.ln(4)

    pdf.section_title('4. System Architecture')
    pdf.section_body(
        "The platform is divided into two primary interfaces:\n\n"
        "1. Security Operations Center (SOC) Dashboard: Restricted to Super Admins and Investigators. "
        "Provides a bird's-eye view of the organization's risk landscape, active cases, and the forensic vault.\n\n"
        "2. Employee Portal: The functional workspace for standard users. Telemetry is gathered passively "
        "from every interaction here (files downloaded, time of login, IP address) and funneled to the AI engine."
    )

    pdf.section_title('5. Investigation Workflow')
    pdf.section_body(
        "1. Event Ingestion: User actions are captured and routed to the telemetry pipeline.\n"
        "2. AI Scoring: The Isolation Forest model evaluates the event context. If anomalous, an Alert is generated.\n"
        "3. Case Creation: Alerts are promoted to Cases for human investigation.\n"
        "4. Mitigation: Analysts can review the activity timeline, append notes, suspend accounts, and download the full PDF evidence brief."
    )

    output_path = os.path.join(os.getcwd(), 'ITD_Project_Overview.pdf')
    pdf.output(output_path)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
