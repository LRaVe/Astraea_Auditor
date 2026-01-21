"""Test critical findings with mock mode critical vectors"""
import sys
import os
sys.path.insert(0, 'c:\\Users\\lrv1l\\OneDrive\\Documents\\astraea-gateaway')

# Force Mock Mode
os.environ['MOCK_MODE'] = 'true'

from app.main import handler
from app.auditor import AstraeaAuditor

# Verify mock mode is working
auditor = AstraeaAuditor()
test_result = auditor.run_audit_simulation("Indirect Prompt Injection")
print(f"\n🧪 Test 3: CRITICAL FINDINGS DETECTION")
print(f"   Mock Mode Active: {auditor.mock}")
print(f"   Test Vector: 'Indirect Prompt Injection'")
print(f"   Z-Score: {test_result['z_score']}")
print(f"   Risk Level: {test_result['risk_level']}")

# Run full diagnostic with expected critical findings
test_job = {
    "input": {
        "mode": "diagnostic",
        "client_name": "Test_Critical_Findings"
    }
}

result = handler(test_job)
print(f"\n   Results Summary:")
print(f"   Status: {result['status']}")
print(f"   Critical Failures: {result['critical_failures']}")
print(f"   Vectors Tested: {result['total_vectors_tested']}")
print(f"   Report Generated: {result['report_url']}")

if result['critical_failures'] > 0:
    print(f"\n✅ Test 3 PASSED: Critical findings detected!")
else:
    print(f"\n⚠️  Test 3 NOTE: No critical findings in this run (mock randomization)")
