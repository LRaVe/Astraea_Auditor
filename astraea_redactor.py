import re
import json
import sys
import os

class AstraeaRedactor:
    """
    Client-Side PII Scrubber for Astraea Audit Compliance.
    Run this locally on your logs before uploading to the Audit Environment.
    """
    def __init__(self):
        # Industrial-grade Regex patterns for European Fintech Data
        self.patterns = {
            # GDPR Critical Data (most specific patterns first)
            "IBAN": r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}(?:[A-Z0-9]?){0,16}\b',
            "CREDIT_CARD": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b',
            "PHONE_EU": r'\+\d{1,3}\s?(?:\(?\d{1,4}\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,9}\b',
            
            # Contextual PII (JSON key-value pairs)
            "JSON_NAME_FIELD": r'("name"\s*:\s*")[^"]*(")',
            "JSON_EMAIL_FIELD": r'("email"\s*:\s*")[^"]*(")'
        }

    def redact_text(self, text):
        """
        Replaces sensitive patterns with [REDACTED_TYPE].
        """
        redacted = text
        
        # 1. Redact specific regex patterns
        for label, pattern in self.patterns.items():
            if "JSON" in label:
                # Handle JSON key-value pairs specifically to keep valid JSON structure
                redacted = re.sub(pattern, r'\1[REDACTED_PII]\2', redacted)
            else:
                # General text replacement
                redacted = re.sub(pattern, f"[{label}_REDACTED]", redacted)
                
        return redacted

    def process_file(self, input_path):
        if not os.path.exists(input_path):
            print(f"❌ Error: File {input_path} not found.")
            return

        print(f"🛡️  Astraea Redactor: Scanning {input_path}...")
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Attempt to parse as JSON first for safer redaction
            try:
                data = json.loads(content)
                # If it's a list of logs, dump it to string, redact, then reload (simplified approach)
                # In a full production version, we would iterate keys.
                # For this diagnostic tool, string-level regex is sufficient and faster.
                clean_content = self.redact_text(json.dumps(data, indent=2))
            except json.JSONDecodeError:
                # It's a plain text log file
                clean_content = self.redact_text(content)

            output_path = f"REDACTED_{os.path.basename(input_path)}"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)

            print(f"✅ Success! Sensitive data scrubbed.")
            print(f"📂 Output saved to: {output_path}")
            print(f"👉 You may now securely upload '{output_path}' to the Astraea Audit Portal.")

        except Exception as e:
            print(f"❌ Critical Error: {str(e)}")

if __name__ == "__main__":
    # Simple CLI usage
    if len(sys.argv) < 2:
        print("Usage: python astraea_redactor.py <path_to_log_file>")
    else:
        redactor = AstraeaRedactor()
        redactor.process_file(sys.argv[1])
