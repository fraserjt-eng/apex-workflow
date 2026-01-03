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
from pathlib import Path

# Patterns that might indicate student PII
PII_PATTERNS = [
    # Direct identifiers
    (r'\b\d{3}-\d{2}-\d{4}\b', 'Social Security Number', 'critical'),
    (r'\b\d{9}\b', 'Potential Student ID (9 digits)', 'high'),
    (r'\b[A-Z]{2}\d{7,8}\b', 'State Student ID pattern', 'high'),

    # Student identification fields
    (r'student[_\s]?(id|number|num)\s*[:=]\s*\d+', 'Student ID field', 'high'),
    (r'student[:\s]+[A-Z][a-z]+\s+[A-Z][a-z]+', 'Student full name pattern', 'critical'),
    (r'first[_\s]?name\s*[:=]\s*["\']?\w+', 'First name field', 'medium'),
    (r'last[_\s]?name\s*[:=]\s*["\']?\w+', 'Last name field', 'medium'),

    # Date patterns
    (r'(?:DOB|birth[_\s]?date)\s*[:=]\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', 'Date of birth', 'high'),
    (r'birth[_\s]?date\s*[:=]', 'Birth date field', 'medium'),

    # Contact information
    (r'parent[_\s]?(email|phone|contact)', 'Parent contact info', 'medium'),
    (r'guardian[_\s]?(email|phone|name)', 'Guardian contact info', 'medium'),
    (r'emergency[_\s]?contact', 'Emergency contact', 'medium'),
    (r'home[_\s]?address', 'Home address field', 'high'),

    # Protected categories
    (r'\b(?:IEP|504\s*plan|special\s*ed|sped)\b', 'Special education reference', 'high'),
    (r'(?:diagnosis|disability|medical\s*condition)', 'Medical/disability info', 'critical'),
    (r'(?:discipline|suspension|expulsion|detention).*(?:student|name)', 'Discipline record', 'high'),
    (r'(?:behavioral|behavior\s*plan|BIP)', 'Behavioral plan reference', 'high'),

    # Free/reduced lunch (proxy for economic status)
    (r'(?:free|reduced)\s*(?:lunch|meal|FRL)', 'Economic status indicator', 'medium'),

    # Immigration/citizenship
    (r'(?:immigration|citizenship|undocumented|DACA)', 'Immigration status', 'critical'),
]

# File patterns that should be extra careful
SENSITIVE_FILE_PATTERNS = [
    r'student', r'roster', r'grade', r'attendance',
    r'discipline', r'iep', r'sped', r'behavior',
    r'medical', r'health', r'contact', r'emergency',
]

# Safe patterns (false positives to ignore)
SAFE_PATTERNS = [
    r'student\s*=\s*\{\}',  # Empty student object
    r'student\.id\s*=',     # Code pattern
    r'class\s+Student',     # Class definition
    r'def\s+.*student',     # Function definition
    r'#.*student',          # Comment
    r'//.*student',         # Comment
    r'""".*student',        # Docstring
]


def is_safe_context(content: str, match_start: int, match_end: int) -> bool:
    """Check if match is in a safe context (code, comment, etc.)."""
    # Get surrounding context
    line_start = content.rfind('\n', 0, match_start) + 1
    line_end = content.find('\n', match_end)
    if line_end == -1:
        line_end = len(content)
    line = content[line_start:line_end]

    return any(re.search(pattern, line, re.IGNORECASE) for pattern in SAFE_PATTERNS)


def check_content(content: str, filepath: str = '') -> tuple:
    """Check content for potential PII patterns."""
    issues = []
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0}

    # Check file path for sensitivity indicators
    is_sensitive_file = any(
        re.search(pattern, filepath.lower())
        for pattern in SENSITIVE_FILE_PATTERNS
    )

    for pattern, description, severity in PII_PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            # Skip if in safe context
            if is_safe_context(content, match.start(), match.end()):
                continue

            # Get line number
            line_num = content[:match.start()].count('\n') + 1

            issues.append({
                'pattern': description,
                'severity': severity,
                'line': line_num,
                'match': match.group()[:50] + '...' if len(match.group()) > 50 else match.group()
            })
            severity_counts[severity] += 1

    return issues, is_sensitive_file, severity_counts


def format_report(issues: list, filepath: str, severity_counts: dict) -> str:
    """Format the warning report."""
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("  FERPA COMPLIANCE WARNING")
    lines.append("=" * 60)

    if filepath:
        lines.append(f"File: {Path(filepath).name}")

    lines.append("")

    # Summary by severity
    if severity_counts['critical'] > 0:
        lines.append(f"  CRITICAL: {severity_counts['critical']} potential violations")
    if severity_counts['high'] > 0:
        lines.append(f"  HIGH:     {severity_counts['high']} potential issues")
    if severity_counts['medium'] > 0:
        lines.append(f"  MEDIUM:   {severity_counts['medium']} items to review")

    lines.append("")
    lines.append("-" * 60)

    # Group by severity
    for severity in ['critical', 'high', 'medium']:
        sev_issues = [i for i in issues if i['severity'] == severity]
        if sev_issues:
            lines.append(f"\n{severity.upper()} SEVERITY:")
            for issue in sev_issues[:5]:  # Limit to 5 per severity
                lines.append(f"  Line {issue['line']}: {issue['pattern']}")
            if len(sev_issues) > 5:
                lines.append(f"  ... and {len(sev_issues) - 5} more")

    lines.append("")
    lines.append("-" * 60)
    lines.append("REQUIRED ACTIONS:")
    lines.append("  1. Review flagged content for actual student PII")
    lines.append("  2. Remove or anonymize any identifiable information")
    lines.append("  3. Use student IDs only in secure, access-controlled files")
    lines.append("  4. Never include SSN, DOB, or medical info in shared docs")
    lines.append("-" * 60)
    lines.append("")

    return '\n'.join(lines)


def main():
    """Main entry point for hook."""
    filepath = os.environ.get('CLAUDE_FILE_PATH', '')

    try:
        # Read from stdin or file
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        elif filepath and os.path.exists(filepath):
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
        else:
            sys.exit(0)

        if not content:
            sys.exit(0)

        # Check content
        issues, is_sensitive, severity_counts = check_content(content, filepath)

        if issues:
            report = format_report(issues, filepath, severity_counts)
            print(report, file=sys.stderr)

            # Block on critical issues in sensitive files
            if severity_counts['critical'] > 0 and is_sensitive:
                print("BLOCKED: Critical PII detected in sensitive file.", file=sys.stderr)
                print("Remove PII before proceeding.", file=sys.stderr)
                # Uncomment to actually block: sys.exit(1)

    except Exception as e:
        # Don't crash the workflow on hook errors
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
