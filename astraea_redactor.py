import re
import json
import os
import argparse


class AstraeaRedactor:
    """
    Client-Side PII Scrubber for Astraea Audit Compliance.

    PURPOSE:
    Sanitize log files of Sensitive Personal Data (PII) locally
    before uploading to the Audit Environment.

    TARGETS:
    - Emails
    - IBANs (European Standard)
    - Credit Card Numbers
    - Phone Numbers (international and French formats)
    - JSON specific fields ("name", "email", etc.)
    """

    def __init__(self):
        # Regex patterns for fintech-relevant data
        self.patterns = {
            # 1. Network and ID
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
            "IP_ADDRESS": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",

            # 2. Financial
            "IBAN": r"\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}\b",
            "CREDIT_CARD": r"\b(?:\d[ -]*?){13,19}\b",

            # 3. Contact
            "PHONE": r"\b(?:\+?\d{1,3})?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b",

            # 4. JSON contextual heuristics
            "JSON_NAME": r"(\"name\"\s*:\s*\")([^\"]*)(\")",
            "JSON_FULLNAME": r"(\"fullName\"\s*:\s*\")([^\"]*)(\")",
            "JSON_CLIENT": r"(\"client_id\"\s*:\s*\")([^\"]*)(\")",
        }

    def redact_text(self, text):
        """Replace matches with redacted tokens."""
        redacted = text

        for label, pattern in self.patterns.items():
            if "JSON" in label:
                redacted = re.sub(pattern, r"\1[REDACTED_PII]\3", redacted, flags=re.IGNORECASE)
            else:
                redacted = re.sub(pattern, f"[{label}_REDACTED]", redacted)

        return redacted

    def process_file(self, input_path):
        if not os.path.exists(input_path):
            print(f"Error: File '{input_path}' not found.")
            return

        print(f"Astraea Redactor: Scanning '{input_path}'...")

        try:
            with open(input_path, "r", encoding="utf-8") as file_handle:
                content = file_handle.read()

            try:
                data = json.loads(content)
                text_content = json.dumps(data, indent=2)
            except json.JSONDecodeError:
                text_content = content

            clean_content = self.redact_text(text_content)

            directory, filename = os.path.split(input_path)
            output_filename = f"REDACTED_{filename}"
            output_path = os.path.join(directory, output_filename)

            with open(output_path, "w", encoding="utf-8") as file_handle:
                file_handle.write(clean_content)

            print("Redaction complete.")
            print(f"Original Size: {len(content)} chars")
            print(f"Cleaned Size:  {len(clean_content)} chars")
            print(f"Output saved to: {output_path}")
            print("Please verify the output locally before transmitting.")

        except Exception as exc:  # noqa: BLE001
            print(f"Critical error during processing: {exc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Astraea Client-Side Redactor")
    parser.add_argument("file", help="Path to the log file (JSON or Text) to redact")
    args = parser.parse_args()

    redactor = AstraeaRedactor()
    redactor.process_file(args.file)
