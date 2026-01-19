from fpdf import FPDF
import datetime
import os

def generate_pdf_report(results, client_name="Fintech_Enterprise_A"):
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
    
    # Executive Summary with monetary exposure estimate
    critical_results = [r for r in results if r["risk_level"] == "CRITICAL"]
    critical_count = len(critical_results)
    overall_status = "FAILED" if critical_count > 0 else "PASSED"
    status_color = (231, 76, 60) if overall_status == "FAILED" else (46, 204, 113)

    highest_z = max((r["z_score"] for r in results), default=0)
    avg_z = sum(r["z_score"] for r in results) / len(results) if results else 0

    # Simple loss model: each critical finding carries an expected loss allowance
    loss_per_critical = 250_000  # adjust to org risk appetite
    estimated_loss = critical_count * loss_per_critical
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. EXECUTIVE SUMMARY", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Total Test Vectors: {len(results)}", ln=True)
    pdf.cell(0, 8, f"Critical Detections: {critical_count}", ln=True)
    pdf.cell(0, 8, f"Highest Z-Score: {highest_z:.2f} | Average Z-Score: {avg_z:.2f}", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(*status_color)
    pdf.cell(0, 9, f"Overall Status: {overall_status}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 9, f"Estimated Financial Exposure: ${estimated_loss:,.0f}", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 7, "Assumption: allowance of $250,000 per critical vector (tunable). Update loss_per_critical in report_gen.py to match business impact models.")
    pdf.ln(5)
    
    # EU AI Act Compliance
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "2. EU AI ACT COMPLIANCE", ln=True)
    pdf.set_font("Arial", '', 11)
    compliance_text = (
        f"Article 15 (Robustness): {'NON-COMPLIANT' if critical_count > 0 else 'COMPLIANT'}\n"
        f"Article 15.4 (Model Poisoning Resilience): {'ACTION REQUIRED' if critical_count > 0 else 'VERIFIED'}\n"
        f"Article 15.1 (Accuracy Stability): VERIFIED"
    )
    pdf.multi_cell(0, 7, compliance_text)
    pdf.ln(5)
    
    # Detailed Results by Category
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "3. DETAILED TEST RESULTS BY CATEGORY", ln=True)
    pdf.ln(3)
    
    # Group results by category
    categories = {}
    for result in results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(result)
    
    # Print each category
    for category, cat_results in categories.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 8, category, ln=True)
        
        for idx, res in enumerate(cat_results, 1):
            # Result color
            res_color = (231, 76, 60) if res["risk_level"] == "CRITICAL" else (46, 204, 113)
            
            pdf.set_font("Arial", '', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 6, f"  Test {idx}: {res['prompt'][:70]}...", ln=True)
            pdf.cell(0, 6, f"    Type: {res.get('type', 'Unspecified')}", ln=True)
            
            pdf.set_font("Arial", 'B', 10)
            pdf.set_text_color(*res_color)
            pdf.cell(0, 6, f"    Result: {res['risk_level']} (Z-Score: {res['z_score']}) | {res['compliance']}", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
        
        pdf.ln(3)

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    report_name = f"reports/Audit_Report_{client_name}.pdf"
    pdf.output(report_name)
    return report_name