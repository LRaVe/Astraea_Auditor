"""
Astraea Redactor: Client-Side PII Scrubber
Removes sensitive data before audit ingestion (Zero-Trust Privacy Model)

Usage:
    python astraea_redactor.py --input raw_logs.json --output redacted_logs.json
"""

import re
import json
import argparse
from typing import Dict, List, Any


class AstraeaRedactor:
    """Redacts PII from audit inputs using pattern-based detection."""

    # Regex patterns for common PII
    PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
        "iban": r"\b[A-Z]{2}\d{2}(?:\s?\w{4}){2,4}\b",
        "account_number": r"\b\d{8,17}\b",
        "person_name": r"\b(?:[A-Z][a-z]+ ){1,3}[A-Z][a-z]+\b",  # Simple heuristic
        "ip_address": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
        "api_key": r"(?:api[_-]?key|token|secret)[\s:=]+['\"]?([a-zA-Z0-9\-_]{20,})['\"]?",
    }

    def __init__(self, strict_mode=False):
        """
        Initialize redactor.
        
        Args:
            strict_mode: If True, masks more aggressively (may over-redact)
        """
        self.strict_mode = strict_mode
        self.redaction_count = {}

    def redact_text(self, text: str) -> str:
        """
        Redact PII from text.
        
        Args:
            text: Raw text to redact
            
        Returns:
            Redacted text with PII replaced
        """
        if not isinstance(text, str):
            return text

        redacted = text
        for pii_type, pattern in self.PATTERNS.items():
            matches = re.finditer(pattern, redacted, re.IGNORECASE)
            for match in matches:
                self.redaction_count[pii_type] = self.redaction_count.get(pii_type, 0) + 1
                placeholder = f"[REDACTED_{pii_type.upper()}]"
                redacted = redacted.replace(match.group(0), placeholder, 1)

        return redacted

    def redact_dict(self, data: Dict[str, Any], keys_to_redact=None) -> Dict[str, Any]:
        """
        Recursively redact PII from dictionary.
        
        Args:
            data: Dictionary to redact
            keys_to_redact: Specific keys to always redact (e.g., 'email', 'name')
            
        Returns:
            Redacted dictionary
        """
        if keys_to_redact is None:
            keys_to_redact = ['email', 'phone', 'name', 'customer_id', 'account', 'ssn', 'iban']

        redacted = {}
        for key, value in data.items():
            if key.lower() in keys_to_redact:
                redacted[key] = f"[REDACTED_{key.upper()}]"
            elif isinstance(value, str):
                redacted[key] = self.redact_text(value)
            elif isinstance(value, dict):
                redacted[key] = self.redact_dict(value, keys_to_redact)
            elif isinstance(value, list):
                redacted[key] = [
                    self.redact_dict(item, keys_to_redact) if isinstance(item, dict)
                    else self.redact_text(item) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                redacted[key] = value

        return redacted

    def redact_json_file(self, input_path: str, output_path: str, keys_to_redact=None):
        """
        Redact PII from JSON file.
        
        Args:
            input_path: Path to raw JSON file
            output_path: Path to save redacted JSON
            keys_to_redact: Specific keys to always redact
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        redacted_data = self.redact_dict(data, keys_to_redact)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(redacted_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Redaction complete: {input_path} → {output_path}")
        print(f"   Redactions applied: {self.redaction_count}")
        return redacted_data


def main():
    parser = argparse.ArgumentParser(
        description="Astraea Redactor: Client-Side PII Scrubber for Zero-Trust Audits"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input JSON file with raw logs"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output JSON file (redacted)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode (more aggressive redaction)"
    )

    args = parser.parse_args()

    redactor = AstraeaRedactor(strict_mode=args.strict)
    redactor.redact_json_file(args.input, args.output)


if __name__ == "__main__":
    main()
