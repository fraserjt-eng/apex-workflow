#!/usr/bin/env python3
"""
FERPA Compliance Check Hook
Scans for potential student PII before file writes

This hook runs before Edit/Write operations to catch potential
FERPA violations before they're written to files.
"""

import sys
import re
import os
import json

# Patterns that might indicate student PII
PII_PATTERNS = [
    (r'\b\d{3}-\d{2}-\d{4}\b', 'Social Security Number pattern'),
    (r'\b\d{9}\b', 'Potential Student ID (9 digits)'),
    (r'student[_\s]?(id|number|num)\s*[:=]\s*\d+', 'Student ID field'),
    (r'birth[_\s]?date\s*[:=]', 'Birth date field'),
    (r'ssn\s*[:=]', 'SSN field'),
    (r'parent[_\s]?(email|phone)', 'Parent contact field'),
    (r'medical|diagnosis|iep|504|sped', 'Special education/medical reference'),
    (r'discipline|suspension|expulsion.*student', 'Discipline record'),
]

# File patterns that should be extra careful
SENSITIVE_FILE_PATTERNS = [
    r'student',
    r'roster',
    r'grade',
    r'attendance',
    r'discipline',
    r'iep',
    r'sped',
]

def check_content(content, filepath=''):
    """Check content for potential PII patterns."""
    issues = []

    # Check file path for sensitivity indicators
    is_sensitive_file = any(
        re.search(pattern, filepath.lower())
        for pattern in SENSITIVE_FILE_PATTERNS
    )

    for pattern, description in PII_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append({
                'pattern': description,
                'count': len(matches),
                'sample': matches[0] if matches else None
            })

    return issues, is_sensitive_file


def main():
    """Main entry point for hook."""
    # Try to get input from stdin (hook provides file path and content)
    try:
        input_data = sys.stdin.read()
        if not input_data:
            sys.exit(0)

        # Check the content
        issues, is_sensitive = check_content(input_data)

        if issues:
            print("\n⚠️  FERPA COMPLIANCE WARNING")
            print("═" * 50)
            print("Potential student PII detected:\n")

            for issue in issues:
                print(f"  • {issue['pattern']}")
                if issue['count'] > 1:
                    print(f"    Found {issue['count']} instances")

            print("\n" + "═" * 50)
            print("Please ensure this content does not contain")
            print("identifiable student information before saving.")
            print("═" * 50 + "\n")

            # Warning only - don't block
            # To block, uncomment: sys.exit(1)

    except Exception as e:
        # Don't crash the workflow on hook errors
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
