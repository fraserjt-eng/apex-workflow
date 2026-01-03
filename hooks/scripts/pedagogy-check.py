#!/usr/bin/env python3
"""
Pedagogy Protocol Check Hook
Validates PD and learning content against J Fraser pedagogy protocol

This hook runs on Stop to validate teaching/learning content
follows Experience -> Analysis -> Framework sequence and includes
required elements like mirror work.
"""

import sys
import re
import os
from pathlib import Path

# Indicators of teaching/learning content
LEARNING_CONTENT_INDICATORS = [
    r'professional\s+development',
    r'PD\s+session',
    r'workshop',
    r'training',
    r'facilitat',
    r'learning\s+(?:objective|outcome|goal)',
    r'participant',
    r'agenda',
    r'session\s+(?:outline|plan)',
    r'debrief',
]

# Required elements for pedagogy compliance
REQUIRED_ELEMENTS = {
    'experiential_entry': {
        'patterns': [
            r'experiential?\s+(?:entry|opening|activity)',
            r'opening\s+activity',
            r'hands[- ]on',
            r'ice\s*breaker',
            r'warm[- ]?up\s+activity',
            r'begin\s+with\s+(?:activity|experience)',
            r'participants\s+will\s+(?:try|do|engage|experience)',
        ],
        'description': 'Experiential Entry (begin with activity, not lecture)',
        'weight': 'required'
    },
    'collaborative_analysis': {
        'patterns': [
            r'collaborativ',
            r'small\s+group',
            r'pair\s+share',
            r'discussion',
            r'process(?:ing)?',
            r'debrief',
            r'what\s+did\s+you\s+notice',
            r'patterns\s+(?:emerge|emerging)',
        ],
        'description': 'Collaborative Analysis (process experience together)',
        'weight': 'required'
    },
    'framework_after': {
        'patterns': [
            r'framework',
            r'theory',
            r'research\s+(?:says|shows|base)',
            r'according\s+to',
            r'(?:introduce|introducing)\s+(?:concept|framework|theory)',
            r'key\s+concept',
        ],
        'description': 'Framework Introduction (theory AFTER experience)',
        'weight': 'required'
    },
    'mirror_work': {
        'patterns': [
            r'mirror\s+work',
            r'self[- ]?(?:reflect|examination|assess)',
            r'personal\s+reflection',
            r'your\s+own\s+(?:patterns?|practice|assumptions?)',
            r'examine\s+(?:your|our|my)',
            r'complicit',
            r'where\s+do\s+(?:I|you|we)\s+show\s+up',
        ],
        'description': 'Mirror Work (self-examination before system critique)',
        'weight': 'required'
    },
    'high_warmth': {
        'patterns': [
            r'welcom',
            r'validat',
            r'appreciat',
            r'acknowledg',
            r'honor',
            r'relationship',
            r'connect(?:ion)?',
            r'care\s+for',
            r'support',
        ],
        'description': 'High Warmth indicators',
        'weight': 'check'
    },
    'high_structure': {
        'patterns': [
            r'expectation',
            r'clear\s+(?:outcome|goal|objective)',
            r'accountab',
            r'timeline',
            r'(?:by|within)\s+\d+\s+minutes',
            r'step\s+\d',
            r'agenda',
            r'schedule',
        ],
        'description': 'High Structure indicators',
        'weight': 'check'
    },
    'application': {
        'patterns': [
            r'application',
            r'practice',
            r'try\s+(?:it|this)',
            r'apply\s+(?:to|in)',
            r'real[- ]?work',
            r'action\s+planning',
            r'next\s+steps',
        ],
        'description': 'Application/Practice opportunity',
        'weight': 'recommended'
    },
}

# Anti-patterns to flag
ANTI_PATTERNS = {
    'lecture_first': {
        'patterns': [
            r'^(?:the\s+)?(?:research|theory|framework)\s+(?:shows|says|tells)',
            r'(?:let\s+me|I\'ll)\s+(?:explain|tell\s+you|present)',
            r'first,?\s+(?:understand|learn\s+about)',
        ],
        'warning': 'May be starting with lecture instead of experience'
    },
    'no_participant_voice': {
        'patterns': [
            r'(?:students|participants)\s+will\s+(?:learn|understand|know)',
        ],
        'warning': 'Passive learning objectives (use action verbs: analyze, create, apply)'
    },
}


def is_learning_content(content: str) -> bool:
    """Check if content appears to be teaching/learning material."""
    content_lower = content.lower()
    matches = sum(1 for pattern in LEARNING_CONTENT_INDICATORS
                  if re.search(pattern, content_lower))
    return matches >= 2  # Need at least 2 indicators


def check_element(content: str, element_config: dict) -> tuple:
    """Check for presence of a required element."""
    content_lower = content.lower()
    found = False
    match_count = 0

    for pattern in element_config['patterns']:
        matches = re.findall(pattern, content_lower)
        if matches:
            found = True
            match_count += len(matches)

    return found, match_count


def check_sequence(content: str) -> dict:
    """Check if Experience -> Analysis -> Framework sequence is maintained."""
    content_lower = content.lower()

    # Find positions of key elements
    positions = {}

    experience_patterns = REQUIRED_ELEMENTS['experiential_entry']['patterns']
    for pattern in experience_patterns:
        match = re.search(pattern, content_lower)
        if match:
            positions['experience'] = match.start()
            break

    framework_patterns = REQUIRED_ELEMENTS['framework_after']['patterns']
    for pattern in framework_patterns:
        match = re.search(pattern, content_lower)
        if match:
            positions['framework'] = match.start()
            break

    # Check sequence
    if 'experience' in positions and 'framework' in positions:
        if positions['experience'] < positions['framework']:
            return {'correct': True, 'message': 'Experience precedes Framework'}
        else:
            return {'correct': False, 'message': 'WARNING: Framework may appear before Experience'}

    return {'correct': None, 'message': 'Could not verify sequence'}


def format_report(results: dict, filepath: str = '') -> str:
    """Format the pedagogy check report."""
    lines = []
    lines.append("")
    lines.append("=" * 65)
    lines.append("  J FRASER PEDAGOGY PROTOCOL CHECK")
    lines.append("=" * 65)

    if filepath:
        lines.append(f"File: {Path(filepath).name}")

    lines.append("")

    # Summary scores
    required_met = sum(1 for k, v in results['elements'].items()
                       if REQUIRED_ELEMENTS[k]['weight'] == 'required' and v['found'])
    required_total = sum(1 for k in results['elements']
                         if REQUIRED_ELEMENTS[k]['weight'] == 'required')

    lines.append(f"  Required elements: {required_met}/{required_total}")
    lines.append("")

    # Sequence check
    seq = results.get('sequence', {})
    if seq.get('correct') is True:
        lines.append("  Sequence: Experience -> Framework")
    elif seq.get('correct') is False:
        lines.append("  Sequence: Check order - framework may precede experience")
    lines.append("")

    lines.append("-" * 65)

    # Required elements
    lines.append("\nREQUIRED ELEMENTS:")
    for key, config in REQUIRED_ELEMENTS.items():
        if config['weight'] != 'required':
            continue
        result = results['elements'].get(key, {})
        status = "PRESENT" if result.get('found') else "MISSING"
        indicator = "" if result.get('found') else "  <-- Add this"
        lines.append(f"  [{status}] {config['description']}{indicator}")

    # Check elements (warmth/structure)
    lines.append("\nWARMTH + STRUCTURE CHECK:")
    warmth = results['elements'].get('high_warmth', {})
    structure = results['elements'].get('high_structure', {})

    warmth_score = warmth.get('count', 0)
    structure_score = structure.get('count', 0)

    if warmth_score >= 3 and structure_score >= 3:
        lines.append("  Both High Warmth and High Structure present")
    elif warmth_score < 3:
        lines.append("  Consider adding more warmth indicators")
    elif structure_score < 3:
        lines.append("  Consider adding more structure indicators")

    # Recommendations
    lines.append("\nRECOMMENDED (Optional):")
    for key, config in REQUIRED_ELEMENTS.items():
        if config['weight'] != 'recommended':
            continue
        result = results['elements'].get(key, {})
        status = "Present" if result.get('found') else "Could add"
        lines.append(f"  [{status}] {config['description']}")

    # Anti-patterns
    if results.get('warnings'):
        lines.append("\nWARNINGS:")
        for warning in results['warnings']:
            lines.append(f"  ! {warning}")

    lines.append("")
    lines.append("-" * 65)
    lines.append("REMEMBER: Experience -> Analysis -> Framework (never reverse)")
    lines.append("-" * 65)
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

        # Only check learning content
        if not is_learning_content(content):
            sys.exit(0)

        # Check all elements
        results = {'elements': {}, 'warnings': []}

        for key, config in REQUIRED_ELEMENTS.items():
            found, count = check_element(content, config)
            results['elements'][key] = {'found': found, 'count': count}

        # Check sequence
        results['sequence'] = check_sequence(content)

        # Check for anti-patterns
        for key, config in ANTI_PATTERNS.items():
            for pattern in config['patterns']:
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    results['warnings'].append(config['warning'])
                    break

        # Format and print report
        report = format_report(results, filepath)
        print(report, file=sys.stderr)

    except Exception as e:
        # Don't crash the workflow on hook errors
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
