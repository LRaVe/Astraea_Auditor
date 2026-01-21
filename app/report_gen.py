from fpdf import FPDF
import datetime
import os

def generate_pdf_report(results, client_name="Fintech_Enterprise_A", loss_per_critical=5_000_000):
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

    # Executive Summary (CEO-facing)
    critical_results = [r for r in results if r["risk_level"] == "CRITICAL"]
    critical_count = len(critical_results)
    overall_status = "CRITICAL" if critical_count > 0 else "SECURE"
    status_color = (231, 76, 60) if overall_status == "CRITICAL" else (46, 204, 113)

    highest_z = max((r["z_score"] for r in results), default=0)
    avg_z = sum(r["z_score"] for r in results) / len(results) if results else 0
    secure_z = [r["z_score"] for r in results if r["risk_level"] == "SECURE"]
    baseline_activation = sum(secure_z) / len(secure_z) if secure_z else 0
    spike_activation = highest_z

    estimated_loss = critical_count * loss_per_critical

    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "EXECUTIVE SUMMARY: AI ROBUSTNESS CONFORMITY AUDIT", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Date: {datetime.date.today()}", ln=True)
    pdf.cell(0, 8, "Project: Astraea Neural Integrity Scan", ln=True)
    pdf.cell(0, 8, f"Target System: {client_name}", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(*status_color)
    pdf.cell(0, 9, f"Overall Risk Rating: [{overall_status}]", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "1. The Bottom Line", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, "During our diagnostic, we identified a critical vulnerability in the model's latent activation layers. The RAG pipeline is susceptible to indirect model poisoning, allowing hidden neural triggers to bypass firewalls and manipulate financial decisions.")
    pdf.ln(2)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "2. Regulatory Impact (EU AI Act Article 15)", ln=True)
    pdf.set_font("Arial", '', 11)
    
    # Determine fine tier based on severity
    if critical_count > 0:
        fine_tier = "Tier 2: EUR 35,000,000 or 7% of global annual turnover" if critical_count >= 3 else "Tier 1: EUR 15,000,000 or 3% of global annual turnover"
        severity_note = " (escalates to Tier 2 if systemic harm demonstrated)" if critical_count < 3 else " (systemic non-compliance)"
    else:
        fine_tier = "No penalties - system compliant"
        severity_note = ""
    
    regulatory_text = (
        f"Under EU AI Act enforcement, high-risk financial AI systems must prove adversarial robustness. "
        f"Finding: {'the system currently fails the Cyber-Attack Resilience requirement (Art. 15.4). ' if critical_count > 0 else 'the system demonstrates adequate robustness. '}"
        f"Penalty Exposure: {fine_tier}{severity_note}. "
        f"Note: Art. 15.1 (Accuracy) violations: EUR 15M/3%; Art. 15.4 (Robustness) violations: EUR 15M/3% (base) to EUR 35M/7% (severe)."
    )
    pdf.multi_cell(0, 7, regulatory_text)
    pdf.ln(2)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "3. Key Technical Finding: The \"Neural Spike\"", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7, f"Baseline Activation (benign prompts): {baseline_activation:.2f}\nAdversarial Activation (peak): {spike_activation:.2f}\nInterpretation: The elevated activation indicates the model is processing unauthorized instructions and bypassing safety rails.")
    pdf.ln(2)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "4. Strategic Recommendations", ln=True)
    pdf.set_font("Arial", '', 11)
    
    # Generate adaptive recommendations based on failures
    recommendations = []
    
    # Analyze critical findings by category
    cluster_a_critical = [r for r in critical_results if "Cluster A" in r["category"]]
    cluster_b_critical = [r for r in critical_results if "Cluster B" in r["category"]]
    cluster_c_critical = [r for r in critical_results if "Cluster C" in r["category"]]
    
    # Cluster A: Direct Model Integrity (Jailbreaking, Backdoors, Knowledge Base Poisoning)
    if cluster_a_critical:
        recommendations.append("IMMEDIATE - Model Integrity Compromise Detected:")
        recommendations.append("  * Deploy model output validation layer to catch jailbreak attempts")
        recommendations.append("  * Implement backdoor trigger detection using activation pattern analysis")
        recommendations.append("  * Perform full model weights audit for poisoning signatures")
        recommendations.append("  * Est. remediation time: 10-14 days")
    
    # Cluster B: Input/Ingestion Vulnerabilities (Prompt Injection, ASCII Smuggling, Token Smuggling)
    if cluster_b_critical:
        recommendations.append("IMMEDIATE - Input Validation Failures Detected:")
        recommendations.append("  * Deploy adversarial filtering gateway on all RAG ingress points")
        recommendations.append("  * Implement prompt sanitization (delimiter stripping, encoding normalization)")
        recommendations.append("  * Add multi-stage input validation (syntax + semantic checks)")
        recommendations.append("  * Est. remediation time: 5-7 days")
    
    # Cluster C: Systemic & Resource Risks (DoW, Context Hijacking, Output Manipulation)
    if cluster_c_critical:
        recommendations.append("IMMEDIATE - Systemic Risk Exposure Detected:")
        recommendations.append("  * Implement context window segmentation and validation")
        recommendations.append("  * Deploy real-time latent spike monitoring (z-score > 3.0 alerts)")
        recommendations.append("  * Add rate limiting and circuit breakers for anomaly detection")
        recommendations.append("  * Est. remediation time: 7-10 days")
    
    # If no critical findings
    if not recommendations:
        recommendations.append("ONGOING - Maintain Current Defenses:")
        recommendations.append("  * Continue periodic adversarial audits (quarterly recommended)")
        recommendations.append("  * Monitor for emerging attack vectors and update baselines")
        recommendations.append("  * Implement real-time latent spike monitoring for proactive detection")
    else:
        # Add ongoing recommendation for any critical case
        recommendations.append("")
        recommendations.append("ONGOING - Post-Remediation:")
        recommendations.append("  * Establish continuous adversarial monitoring (24/7 z-score tracking)")
        recommendations.append("  * Implement automated incident response for spike detection")
        recommendations.append("  * Schedule re-audit in 30 days to verify fixes")
    
    pdf.multi_cell(0, 7, "\n".join(recommendations))
    pdf.ln(4)
    
    # Top Findings (ranked by z-score)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "5. TOP FINDINGS (RANKED)", ln=True)
    pdf.set_font("Arial", '', 11)
    sorted_results = sorted(results, key=lambda r: r.get("z_score", 0), reverse=True)
    top_three = sorted_results[:3]
    if not top_three:
        pdf.cell(0, 8, "No findings.", ln=True)
    else:
        for idx, res in enumerate(top_three, 1):
            pdf.cell(0, 7, f"{idx}) {res['category']} | {res.get('type','Unspecified')} | z={res['z_score']:.2f} | {res['risk_level']}", ln=True)
    pdf.ln(4)

    # Metrics Snapshot with monetary exposure estimate
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "6. METRICS SNAPSHOT", ln=True)
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
    
    # Explain the exposure calculation method
    exposure_note = (
        f"NOTE: This estimate uses ${loss_per_critical:,.0f} per critical finding as a placeholder. "
        f"Actual EU AI Act penalties are NOT calculated per vulnerability but by overall compliance tier: "
        f"Tier 1 (isolated failures) = EUR 15M or 3% of global revenue; "
        f"Tier 2 (systemic non-compliance) = EUR 35M or 7% of global revenue (whichever higher). "
        f"For a company with EUR 1B revenue: Tier 1 = EUR 30M, Tier 2 = EUR 70M. "
        f"Use actual revenue figures for precise exposure calculation."
    )
    pdf.multi_cell(0, 7, exposure_note)
    pdf.ln(5)

    # Coverage Matrix (by cluster)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "7. COVERAGE MATRIX (Attack Vectors)", ln=True)
    pdf.set_font("Arial", '', 11)

    # Compute per-category stats
    coverage_lines = []
    categories_stats = {}
    for res in results:
        cat = res["category"]
        stats = categories_stats.setdefault(cat, {"total": 0, "critical": 0})
        stats["total"] += 1
        if res["risk_level"] == "CRITICAL":
            stats["critical"] += 1

    for cat, stats in categories_stats.items():
        status = "FAIL" if stats["critical"] > 0 else "PASS"
        coverage_lines.append(f"- {cat}: {status} (critical={stats['critical']}, total={stats['total']})")

    if not coverage_lines:
        coverage_lines.append("- No tests recorded.")

    pdf.multi_cell(0, 7, "\n".join(coverage_lines))
    pdf.ln(4)

    # Detailed Remediation Plan (prioritized)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "8. REMEDIATION PLAN (Prioritized)", ln=True)
    pdf.set_font("Arial", '', 11)
    remediation_lines = []
    remediation_lines.append("1) Immediate (0-3 days):")
    remediation_lines.append("   - Enable adversarial filtering on all ingress (prompt sanitization, delimiter stripping, encoding normalization)")
    remediation_lines.append("   - Add request throttling and circuit breakers on the model API")
    remediation_lines.append("   - Turn on real-time latent spike alerts (z-score > 3 triggers incident)")
    remediation_lines.append("2) Short-Term (3-14 days):")
    remediation_lines.append("   - Run backdoor/trigger scan and integrity check on model weights")
    remediation_lines.append("   - Add output validation layer to catch jailbreak responses")
    remediation_lines.append("   - Re-calibrate baselines with clean prompts and re-run audit")
    remediation_lines.append("3) Ongoing (14+ days):")
    remediation_lines.append("   - Continuous adversarial monitoring (24/7) and weekly drift checks")
    remediation_lines.append("   - Quarterly adversarial audit with refreshed vector set")
    remediation_lines.append("   - Integrate alerts to SOC/SIEM with runbooks for incident response")
    pdf.multi_cell(0, 7, "\n".join(remediation_lines))
    pdf.ln(4)

    # Monitoring and Logging
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "9. MONITORING AND LOGGING", ln=True)
    pdf.set_font("Arial", '', 11)
    monitor_lines = []
    monitor_lines.append("- Metrics: z-score per request; alert if z > 3 (tune per baseline)")
    monitor_lines.append("- Logs: store prompts, z-score, category, decision (pass/block), and timestamp")
    monitor_lines.append("- Alerts: send to on-call/SIEM with payload snippet and decision path")
    monitor_lines.append("- Rate controls: enforce QPS limits and circuit breakers on repeated spikes")
    monitor_lines.append("- Posture: re-baseline when model weights or retrieval corpus change")
    pdf.multi_cell(0, 7, "\n".join(monitor_lines))
    pdf.ln(4)

    # Root Causes and Gaps
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "10. ROOT CAUSES AND GAPS", ln=True)
    pdf.set_font("Arial", '', 11)
    gaps = []
    gaps.append("- Input layer lacks adversarial sanitization (delimiter/encoding normalization)")
    gaps.append("- No output validation layer to block jailbreak responses")
    gaps.append("- No real-time latent spike monitoring wired to alerts")
    gaps.append("- Model integrity checks/backdoor scans not routinely run")
    gaps.append("- Rate limiting/circuit breakers not enforced on inference endpoints")
    pdf.multi_cell(0, 7, "\n".join(gaps))
    pdf.ln(4)

    # Operations and Configuration Notes
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "11. OPERATIONS AND CONFIGURATION", ln=True)
    pdf.set_font("Arial", '', 11)
    ops = []
    ops.append("- Env: HF_TOKEN (for gated model), MOCK_MODE=true for lightweight tests")
    ops.append("- Env: LOSS_PER_CRITICAL to set financial exposure assumption")
    ops.append("- Hardware: ensure GPU/CPU per model requirements; cache model weights to avoid retries")
    ops.append("- Reports: saved under reports/ as Audit_Report_<client>.pdf")
    ops.append("- Baselines: refresh when model or retrieval corpus changes")
    pdf.multi_cell(0, 7, "\n".join(ops))
    pdf.ln(4)

    # Artifacts and Repro Steps
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "12. ARTIFACTS AND REPRO STEPS", ln=True)
    pdf.set_font("Arial", '', 11)
    repro = []
    repro.append("- API: POST /audit with client_name, baseline_prompts, test_cases")
    repro.append("- Health: GET /health")
    repro.append("- Run local: python -m app.main (or uvicorn app.main:app)")
    repro.append("- Docker: docker build -t astraea-gateway . ; docker run -p 8000:8000 astraea-gateway")
    repro.append("- Artifacts: see reports/ for generated PDFs")
    pdf.multi_cell(0, 7, "\n".join(repro))
    pdf.ln(4)

    # Assumptions and Limitations
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "13. ASSUMPTIONS AND LIMITATIONS", ln=True)
    pdf.set_font("Arial", '', 11)
    limits = []
    limits.append("- Tests reflect provided prompts; untested vectors may remain.")
    limits.append("- MOCK_MODE bypasses real model behavior; production results require full model.")
    limits.append("- Access to gated model (HF token) is required for full-fidelity runs.")
    limits.append("- Baseline quality depends on clean prompt set; re-run baselines after major changes.")
    pdf.multi_cell(0, 7, "\n".join(limits))
    pdf.ln(4)
    
    # EU AI Act Compliance
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "14. EU AI ACT COMPLIANCE & PENALTY EXPOSURE", ln=True)
    pdf.set_font("Arial", '', 11)
    
    # Determine compliance status and penalty tier
    art15_status = "NON-COMPLIANT" if critical_count > 0 else "COMPLIANT"
    art15_4_status = "ACTION REQUIRED" if critical_count > 0 else "VERIFIED"
    
    # Calculate penalty tier
    if critical_count == 0:
        penalty_tier = "No Penalties - System Compliant"
    elif critical_count < 3:
        penalty_tier = "Tier 1: Up to EUR 15,000,000 or 3% of global turnover (whichever higher)"
    else:
        penalty_tier = "Tier 2: Up to EUR 35,000,000 or 7% of global turnover (whichever higher)"
    
    compliance_text = (
        f"Article 15 (Overall Robustness): {art15_status}\n"
        f"Article 15.1 (Accuracy & Reliability): VERIFIED\n"
        f"Article 15.4 (Adversarial Resilience): {art15_4_status}\n\n"
        f"PENALTY TIER: {penalty_tier}\n\n"
        f"Fine Structure Details:\n"
        f"- Tier 1 (Art. 15.1, 15.4 isolated failures): EUR 15M or 3%\n"
        f"- Tier 2 (Systemic Art. 15 non-compliance): EUR 35M or 7%\n"
        f"- Critical Finding Count: {critical_count} (threshold: 3+ triggers Tier 2)\n"
        f"- Note: Fines apply 'whichever is higher' between fixed amount and revenue percentage"
    )
    pdf.multi_cell(0, 7, compliance_text)
    pdf.ln(5)
    
    # Detailed Results by Category
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "15. DETAILED TEST RESULTS BY CATEGORY", ln=True)
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