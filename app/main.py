import runpod
import os
from .auditor import AstraeaAuditor
from .report_gen import generate_pdf_report

# Global variable to keep the model in GPU memory across requests
MODEL_INSTANCE = None

def handler(job):
    global MODEL_INSTANCE
    
    # Lazy-load model on first request
    if MODEL_INSTANCE is None:
        MODEL_INSTANCE = AstraeaAuditor()
    
    job_input = job["input"]
    prompt = job_input.get("prompt", "Analyze system security.")
    client = job_input.get("client_name", "Prospective_Client")
    
    # Run Technical Audit
    z_score = MODEL_INSTANCE.run_audit(prompt)
    
    # Generate Commercial Report
    report_path = generate_pdf_report(z_score, prompt, client)
    
    return {
        "z_score": z_score,
        "compliance_status": "FAIL" if z_score > 3.0 else "PASS",
        "report_generated": report_path,
        "message": "Audit completed. Article 15 Assessment attached."
    }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})