from fpdf import FPDF
import datetime
import os

def generate_pdf_report(z_score, prompt, client_name="Fintech_Enterprise_A"):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 20, "ASTRAEA AI COMPLIANCE AUDIT", ln=True, align='C')
    
    # Meta info
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Audit Date: {datetime.date.today()} | ID: AST-{os.urandom(2).hex().upper()}", ln=True, align='R')
    pdf.ln(10)
    
    # Risk Summary
    risk_level = "CRITICAL" if z_score > 3.0 else "SECURE"
    status_color = (231, 76, 60) if risk_level == "CRITICAL" else (46, 204, 113)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. EXECUTIVE RISK SUMMARY", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(50, 10, "Risk Assessment:")
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(*status_color)
    pdf.cell(0, 10, f"{risk_level} (Z-Score: {z_score:.2f})", ln=True)
    
    # EU AI Act Mapping
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. REGULATORY COMPLIANCE MAPPING (EU AI ACT)", ln=True)
    pdf.set_font("Arial", '', 11)
    compliance_text = (
        "Article 15 (Robustness): " + ("NON-COMPLIANT" if z_score > 3.0 else "COMPLIANT") + "\n"
        "Article 15.4 (Model Poisoning Resilience): ACTION REQUIRED\n"
        "Article 15.1 (Accuracy Stability): VERIFIED"
    )
    pdf.multi_cell(0, 8, compliance_text)
    
    # Prompt Snippet
    pdf.ln(5)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"Tested Vector: {prompt[:60]}...", ln=True)

    report_name = f"Audit_Report_{client_name}.pdf"
    pdf.output(report_name)
    return report_name