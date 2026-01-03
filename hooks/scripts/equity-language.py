#!/usr/bin/env python3
"""
Equity Language Checker Hook
Flags deficit-based language and suggests asset-based alternatives

This hook runs after Edit/Write operations to suggest more
justice-centered language.
"""

import sys
import re

# Deficit-based terms to flag with asset-based alternatives
DEFICIT_TERMS = {
    r'\bat[-\s]?risk\b': 'students who experience systemic barriers / underserved',
    r'\bachievement\s+gap\b': 'opportunity gap / education debt',
    r'\blow[-\s]?performing\b': 'under-resourced / underserved by current practices',
    r'\bdisadvantaged\b': 'historically marginalized / under-resourced',
    r'\bminority\b': 'historically excluded / global majority / specific group name',
    r'\bbroken\s+home\b': 'diverse family structure',
    r'\bdrop[-\s]?out\b': 'pushed out / early leaver',
    r'\binner[-\s]?city\b': 'urban / under-resourced community',
    r'\bhard[-\s]?to[-\s]?reach\b': 'underserved by traditional outreach',
    r'\bat[-\s]?grade[-\s]?level\b': 'meeting grade-level expectations',
    r'\bbelow[-\s]?grade[-\s]?level\b': 'not yet meeting grade-level expectations',
    r'\bgap\s+students?\b': 'students underserved by current practices',
    r'\blacks?\s+motivation\b': 'not yet engaged / needs different approach',
    r'\bdeficient\b': 'not yet developed / needs support',
    r'\bunable\s+to\b': 'not yet able to / working toward',
    r'\bthese\s+kids\b': '[specific, asset-based descriptor]',
    r'\bthose\s+students\b': '[specific, named group]',
}

# Patterns to flag as potentially problematic framing
FRAMING_CONCERNS = [
    (r'\bparents?\s+(don\'t|do not)\s+care\b',
     'Consider: What barriers might families face?'),
    (r'\bthey\s+just\s+need\s+to\b',
     'Consider: What systemic supports are missing?'),
    (r'\bif\s+only\s+(they|students|parents)\b',
     'Consider: What would it take for the system to change?'),
    (r'\bculturally?\s+deprived\b',
     'Consider: What cultural assets are being overlooked?'),
]


def check_equity_language(content):
    """Check content for deficit-based language."""
    issues = []

    # Check deficit terms
    for pattern, alternative in DEFICIT_TERMS.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            issues.append({
                'type': 'deficit_language',
                'term': matches[0],
                'alternative': alternative,
                'count': len(matches)
            })

    # Check framing concerns
    for pattern, suggestion in FRAMING_CONCERNS:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({
                'type': 'framing',
                'pattern': pattern,
                'suggestion': suggestion
            })

    return issues


def main():
    """Main entry point for hook."""
    try:
        # Read input
        input_data = sys.stdin.read() if not sys.stdin.isatty() else ""

        if not input_data:
            sys.exit(0)

        issues = check_equity_language(input_data)

        if issues:
            print("\n📝 EQUITY LANGUAGE SUGGESTIONS")
            print("═" * 50)

            # Deficit language
            deficit_issues = [i for i in issues if i['type'] == 'deficit_language']
            if deficit_issues:
                print("\n⚠️  Deficit-based language detected:")
                for issue in deficit_issues:
                    print(f"\n   '{issue['term']}'")
                    print(f"   → Consider: {issue['alternative']}")

            # Framing concerns
            framing_issues = [i for i in issues if i['type'] == 'framing']
            if framing_issues:
                print("\n💭 Framing considerations:")
                for issue in framing_issues:
                    print(f"\n   {issue['suggestion']}")

            print("\n" + "─" * 50)
            print("Justice-centered language:")
            print("  • Asset-based, not deficit-focused")
            print("  • Names systems, not individuals")
            print("  • Centers community voice and agency")
            print("═" * 50 + "\n")

    except Exception as e:
        # Don't crash the workflow on hook errors
        pass

    # Don't block, just suggest
    sys.exit(0)


if __name__ == "__main__":
    main()
