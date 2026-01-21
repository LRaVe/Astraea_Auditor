"""Test audit mode (full 10-vector suite)"""
import sys
sys.path.insert(0, 'c:\\Users\\lrv1l\\OneDrive\\Documents\\astraea-gateaway')

from app.main import handler

test_job = {
    "input": {
        "mode": "audit",
        "client_name": "Test_Full_Audit"
    }
}

result = handler(test_job)
print(f"\n✅ Test 2: AUDIT MODE")
print(f"   Status: {result['status']}")
print(f"   Mode: {result['mode']}")
print(f"   Critical Failures: {result['critical_failures']}")
print(f"   Vectors Tested: {result['total_vectors_tested']}")
print(f"   Report: {result['report_url']}")
