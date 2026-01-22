import sys
import os
import runpod
from .auditor import AstraeaAuditor
from .report_gen import generate_pdf_report

# Warm-start the auditor to avoid reloading per request
try:
    AUDITOR_INSTANCE = AstraeaAuditor()
except Exception as e:
    print(f"🔥 CRITICAL INIT ERROR: {e}")
    sys.exit(1)

# Vector definitions
DIAGNOSTIC_VECTORS = [
    "Indirect Prompt Injection",
    "Jailbreak Attempt",
    "PII Leakage"
]

FULL_AUDIT_VECTORS = DIAGNOSTIC_VECTORS + [
    "ASCII Smuggling",
    "Recursive Loop (DoW)",
    "Context Hijacking",
    "Vector DB Poisoning",
    "Output Formatting Attack",
    "Latent Backdoor Trigger",
    "Cross-Session Memory Leak"
]


def handler(job):
    """RunPod serverless entry point."""
    job_input = job.get("input", {})

    # Parameters
    client_name = job_input.get("client_name", "Unknown_Client")
    mode = job_input.get("mode", "diagnostic").lower()
    scenario_type = job_input.get("scenario", "STANDARD_BANKING")

    # Vector selection (scenario override for FINTECH_AML)
    target_vectors = DIAGNOSTIC_VECTORS
    if scenario_type == "FINTECH_AML":
        target_vectors = [
            "Document Poisoning (Malicious Kbis)",
            "Indirect Prompt Injection",
            "Sanctions Bypass"
        ]
    elif mode == "full_audit":
        target_vectors = FULL_AUDIT_VECTORS

    print(f"🚀 STARTING AUDIT: Client={client_name} | Mode={mode} | Scenario={scenario_type}")

    try:
        results = []
        for vector in target_vectors:
            audit_data = AUDITOR_INSTANCE.run_audit_simulation(vector)
            results.append(audit_data)

        report_path = generate_pdf_report(results, client_name, scenario_key=scenario_type)

        return {
            "status": "completed",
            "client": client_name,
            "scenario": scenario_type,
            "critical_failures": sum(1 for r in results if r['risk_level'] == "CRITICAL"),
            "report_url": report_path,
            "local_path": os.path.abspath(report_path)
        }

    except Exception as e:
        print(f"❌ EXECUTION ERROR: {str(e)}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    print("🔧 Running in Local CLI Mode...")
    test_job = {
        "input": {
            "client_name": "Swan_Test_Local",
            "mode": "diagnostic",
            "scenario": "FINTECH_AML"
        }
    }
    response = handler(test_job)
    print(f"\n✅ DONE. Output: {response}")

# Enable RunPod serverless if deployed
runpod.serverless.start({"handler": handler})