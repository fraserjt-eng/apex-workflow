#!/usr/bin/env python3
"""
Equity Language Check Hook
Flags deficit-based language and suggests asset-based alternatives

This hook runs after Edit/Write operations to provide guidance
on using justice-centered, asset-based language.
"""

import sys
import re
import os
from pathlib import Path

# Deficit terms and their asset-based alternatives
DEFICIT_TERMS = {
    # Student descriptors
    r'\bat[- ]?risk\b': {
        'term': 'at-risk',
        'alternative': 'students experiencing systemic barriers',
        'context': 'Shifts focus from student deficit to system failure'
    },
    r'\blow[- ]?performing\b': {
        'term': 'low-performing',
        'alternative': 'under-resourced / underserved',
        'context': 'Acknowledges resource inequity, not student ability'
    },
    r'\bachievement\s+gap\b': {
        'term': 'achievement gap',
        'alternative': 'opportunity gap / education debt',
        'context': 'Gloria Ladson-Billings: gaps result from denied opportunities'
    },
    r'\bfailing\s+students?\b': {
        'term': 'failing students',
        'alternative': 'students not yet meeting standards',
        'context': 'Growth mindset framing, avoids labeling'
    },

    # Family/community descriptors
    r'\bdisadvantaged\b': {
        'term': 'disadvantaged',
        'alternative': 'historically marginalized / under-resourced',
        'context': 'Names systemic cause, not inherent condition'
    },
    r'\bminority\b': {
        'term': 'minority',
        'alternative': 'historically excluded / global majority / BIPOC',
        'context': 'Minority implies lesser; many groups are global majorities'
    },
    r'\bbroken\s+home\b': {
        'term': 'broken home',
        'alternative': 'diverse family structure',
        'context': 'Non-nuclear families are not broken'
    },
    r'\binner[- ]?city\b': {
        'term': 'inner-city',
        'alternative': 'urban / under-invested community',
        'context': 'Avoids coded racial language'
    },
    r'\bhard[- ]?to[- ]?reach\s+(?:families|parents)\b': {
        'term': 'hard-to-reach families',
        'alternative': 'families underserved by traditional outreach',
        'context': 'Problem is our outreach methods, not families'
    },
    r'\blow[- ]?income\b': {
        'term': 'low-income',
        'alternative': 'families experiencing economic barriers',
        'context': 'Temporary condition, not identity'
    },
    r'\bpoor\s+(?:families|students|communities)\b': {
        'term': 'poor families/students',
        'alternative': 'families experiencing poverty / economic hardship',
        'context': 'Person-first, condition not identity'
    },

    # Behavior/discipline
    r'\bdropout\b': {
        'term': 'dropout',
        'alternative': 'pushed out / early leaver',
        'context': 'Acknowledges systemic push-out factors'
    },
    r'\bbad\s+(?:kid|student|behavior)\b': {
        'term': 'bad kid/student',
        'alternative': 'student experiencing challenges',
        'context': 'Behavior is not identity'
    },
    r'\bproblem\s+student\b': {
        'term': 'problem student',
        'alternative': 'student with unmet needs',
        'context': 'Reframes as needs, not deficits'
    },
    r'\bchronic\s+absentee\b': {
        'term': 'chronic absentee',
        'alternative': 'student with attendance barriers',
        'context': 'Acknowledges barriers vs. choice'
    },

    # Education descriptors
    r'\bgap\s+(?:closing|students|groups)\b': {
        'term': 'gap students',
        'alternative': 'opportunity-focused students',
        'context': 'Avoid labeling students by gaps'
    },
    r'\bremedial\b': {
        'term': 'remedial',
        'alternative': 'foundational / accelerated support',
        'context': 'Remedial implies fixing deficiency'
    },
    r'\bbelow\s+grade\s+level\b': {
        'term': 'below grade level',
        'alternative': 'working toward grade-level mastery',
        'context': 'Growth-oriented framing'
    },

    # Special populations
    r'\bESL\s+students?\b': {
        'term': 'ESL students',
        'alternative': 'multilingual learners / emergent bilinguals',
        'context': 'Asset-based: highlights bilingual strength'
    },
    r'\bLEP\b': {
        'term': 'LEP (Limited English Proficient)',
        'alternative': 'English learners / multilingual learners',
        'context': 'Avoid limiting language'
    },
    r'\bspecial\s+needs\b': {
        'term': 'special needs',
        'alternative': 'students with disabilities / IEP-supported',
        'context': 'Person-first, specific language'
    },

    # Outdated terms
    r'\bcolor[- ]?blind\b': {
        'term': 'colorblind',
        'alternative': 'race-conscious / equity-focused',
        'context': 'Ignoring race ignores racism'
    },
}

# Positive terms to acknowledge (not flag)
ASSET_TERMS = [
    'historically marginalized', 'opportunity gap', 'education debt',
    'multilingual learners', 'emergent bilinguals', 'under-resourced',
    'systemically excluded', 'global majority', 'justice-centered',
    'asset-based', 'culturally responsive', 'healing-centered',
]


def check_content(content: str) -> list:
    """Check content for deficit language."""
    findings = []

    for pattern, info in DEFICIT_TERMS.items():
        for match in re.finditer(pattern, content, re.IGNORECASE):
            # Get line number and context
            line_num = content[:match.start()].count('\n') + 1
            line_start = content.rfind('\n', 0, match.start()) + 1
            line_end = content.find('\n', match.end())
            if line_end == -1:
                line_end = len(content)
            line_context = content[line_start:line_end].strip()

            findings.append({
                'term': info['term'],
                'found': match.group(),
                'alternative': info['alternative'],
                'context': info['context'],
                'line': line_num,
                'line_text': line_context[:80] + '...' if len(line_context) > 80 else line_context
            })

    return findings


def count_asset_terms(content: str) -> int:
    """Count asset-based terms already in use."""
    count = 0
    for term in ASSET_TERMS:
        count += len(re.findall(re.escape(term), content, re.IGNORECASE))
    return count


def format_report(findings: list, asset_count: int, filepath: str = '') -> str:
    """Format the feedback report."""
    lines = []
    lines.append("")
    lines.append("=" * 65)
    lines.append("  EQUITY LANGUAGE REVIEW")
    lines.append("=" * 65)

    if filepath:
        lines.append(f"File: {Path(filepath).name}")

    lines.append("")

    if asset_count > 0:
        lines.append(f"  Asset-based terms found: {asset_count}")

    if findings:
        lines.append(f"  Deficit terms to review:  {len(findings)}")
        lines.append("")
        lines.append("-" * 65)
        lines.append("")

        # Group by term
        seen_terms = set()
        for finding in findings:
            if finding['term'] in seen_terms:
                continue
            seen_terms.add(finding['term'])

            lines.append(f"  FOUND: \"{finding['term']}\"")
            lines.append(f"  USE:   \"{finding['alternative']}\"")
            lines.append(f"  WHY:   {finding['context']}")
            lines.append(f"  Line {finding['line']}: {finding['line_text']}")
            lines.append("")

        lines.append("-" * 65)
        lines.append("LANGUAGE PRINCIPLES:")
        lines.append("  - Name systems, not student/family deficits")
        lines.append("  - Lead with assets, then address challenges")
        lines.append("  - Use person-first, growth-oriented language")
        lines.append("  - Be specific rather than using coded terms")
        lines.append("-" * 65)
    else:
        lines.append("")
        lines.append("  No deficit language detected.")
        if asset_count > 0:
            lines.append("  Document uses asset-based framing.")
        lines.append("")

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
        findings = check_content(content)
        asset_count = count_asset_terms(content)

        if findings:
            report = format_report(findings, asset_count, filepath)
            print(report, file=sys.stderr)

    except Exception as e:
        # Don't crash the workflow on hook errors
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
