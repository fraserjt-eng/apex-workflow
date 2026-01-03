#!/usr/bin/env python3
"""
Pedagogy Protocol Validation Hook
Checks professional development and teaching content for J Fraser protocol compliance

This hook runs after Edit/Write operations on PD-related files to
ensure adherence to the J Fraser pedagogical approach.
"""

import sys
import re
import os

# Files that should follow pedagogy protocol
PEDAGOGY_FILE_PATTERNS = [
    r'pd[-_\s]',
    r'session[-_\s]',
    r'curriculum[-_\s]',
    r'workshop[-_\s]',
    r'training[-_\s]',
    r'facilitation[-_\s]',
    r'lesson[-_\s]',
    r'learning[-_\s]',
    r'professional[-_\s]development',
]

# Required elements in pedagogy-related content
REQUIRED_ELEMENTS = {
    'experiential_entry': [
        r'experience\s+first',
        r'begin\s+with',
        r'start\s+with.*experience',
        r'opening\s+activity',
        r'experiential',
        r'engage.*before.*framework',
        r'concrete\s+experience',
    ],
    'mirror_work': [
        r'mirror\s+work',
        r'self[-\s]?reflect',
        r'examine.*own',
        r'your\s+patterns',
        r'complicity',
        r'personal\s+reflection',
        r'look\s+inward',
    ],
    'high_warmth_structure': [
        r'high\s+warmth',
        r'high\s+structure',
        r'warmth.*structure',
        r'thriving\s+communit',
        r'clear\s+and\s+care',
        r'warm\s+demander',
    ],
    'street_data': [
        r'street\s+data',
        r'qualitative',
        r'community\s+voice',
        r'lived\s+experience',
        r'student\s+voice',
        r'listening',
    ],
}

def is_pedagogy_file(filepath):
    """Check if file is pedagogy-related based on name."""
    if not filepath:
        return False
    filename = os.path.basename(filepath).lower()
    return any(
        re.search(pattern, filename, re.IGNORECASE)
        for pattern in PEDAGOGY_FILE_PATTERNS
    )


def check_pedagogy_compliance(content):
    """Check content for pedagogy protocol compliance."""
    content_lower = content.lower()

    missing_elements = []
    present_elements = []

    for element, patterns in REQUIRED_ELEMENTS.items():
        found = any(re.search(p, content_lower) for p in patterns)
        if found:
            present_elements.append(element)
        else:
            missing_elements.append(element)

    return present_elements, missing_elements


def format_element_name(element):
    """Format element name for display."""
    return element.replace('_', ' ').title()


def main():
    """Main entry point for hook."""
    try:
        # Read input
        input_data = sys.stdin.read() if not sys.stdin.isatty() else ""

        if not input_data:
            sys.exit(0)

        # Check for pedagogy content markers in the content itself
        content_lower = input_data.lower()
        is_pedagogy = any(
            marker in content_lower
            for marker in ['professional development', 'pd session', 'workshop',
                          'facilitation', 'learning experience', 'curriculum']
        )

        if not is_pedagogy:
            sys.exit(0)

        # Check compliance
        present, missing = check_pedagogy_compliance(input_data)

        if missing:
            print("\n📝 PEDAGOGY PROTOCOL CHECK")
            print("═" * 50)
            print("Teaching/learning content detected.\n")

            if present:
                print("✅ Elements present:")
                for elem in present:
                    print(f"   • {format_element_name(elem)}")
                print()

            print("⚠️  Consider adding:")
            for elem in missing:
                print(f"   • {format_element_name(elem)}")

            print("\n" + "─" * 50)
            print("J Fraser Pedagogy Protocol elements:")
            print("  1. Experience → Analysis → Framework")
            print("  2. Mirror work before lens work")
            print("  3. High warmth + high structure")
            print("  4. Street data alongside satellite data")
            print("═" * 50 + "\n")

    except Exception as e:
        # Don't crash the workflow on hook errors
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
