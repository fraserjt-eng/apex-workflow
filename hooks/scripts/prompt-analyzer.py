#!/usr/bin/env python3
"""
Prompt Analysis Hook
Analyzes user prompts and suggests appropriate APEX agents

This hook runs when the user submits a prompt to suggest
which APEX agents might be helpful for the task.
"""

import sys
import re

# Agent routing keywords - maps keywords to agents
AGENT_TRIGGERS = {
    'apex-orchestrator': [
        'coordinate', 'multi-team', 'complex', 'portfolio', 'strategic',
        'delegate', 'multiple', 'across teams'
    ],
    'grant-writer': [
        'grant', 'funding', 'proposal', 'application', 'rfp',
        'narrative', 'foundation', 'federal', 'title i'
    ],
    'compliance-specialist': [
        'compliance', 'essa', 'title', 'mde', 'audit', 'regulation',
        'requirement', 'allowable', 'reporting'
    ],
    'budget-analyst': [
        'budget', 'fiscal', 'expenditure', 'cost', 'allocation',
        'indirect', 'amendment'
    ],
    'justice-centered-communicator': [
        'email', 'message', 'communicate', 'announce', 'newsletter',
        'stakeholder', 'memo', 'letter'
    ],
    'presentation-designer': [
        'presentation', 'slides', 'deck', 'board presentation',
        'powerpoint', 'keynote', 'visual'
    ],
    'stakeholder-strategist': [
        'stakeholder', 'political', 'relationship', 'coalition',
        'board', 'union', 'navigate'
    ],
    'curriculum-designer': [
        'curriculum', 'pd', 'session', 'workshop', 'training',
        'learning experience', 'professional development'
    ],
    'principal-coach': [
        'coaching', 'principal', 'leadership', 'reflective',
        'supervision', 'feedback', '1:1', 'one-on-one'
    ],
    'pd-facilitator': [
        'facilitation', 'facilitate', 'protocol', 'group',
        'interactive', 'discussion', 'activity'
    ],
    'apps-script-developer': [
        'automation', 'script', 'apps script', 'google sheets',
        'google forms', 'automate', 'trigger'
    ],
    'data-analyst': [
        'data', 'analysis', 'dashboard', 'disaggregate', 'metrics',
        'visualization', 'trends', 'mca', 'star', 'map'
    ],
    'system-integrator': [
        'integration', 'api', 'sync', 'connect', 'platform',
        'sis', 'lms', 'clever', 'skyward'
    ],
    'equity-auditor': [
        'equity audit', 'disproportionality', 'discipline data',
        'opportunity gap', 'access', 'disparity'
    ],
    'systems-change-analyst': [
        'systems change', 'theory of action', 'change management',
        'transformation', 'strategic planning'
    ],
    'academic-framework-researcher': [
        'research', 'literature', 'framework', 'theory', 'evidence',
        'citation', 'academic', 'what does research say'
    ],
    'quality-control-lead': [
        'review', 'quality', 'final check', 'high-stakes',
        'verify', 'validate', 'before sending'
    ],
}

# Team mapping for grouped suggestions
TEAM_AGENTS = {
    'Grant Strategy': ['grant-writer', 'compliance-specialist', 'budget-analyst'],
    'Strategic Communication': ['justice-centered-communicator', 'presentation-designer', 'stakeholder-strategist'],
    'Professional Learning': ['curriculum-designer', 'principal-coach', 'pd-facilitator'],
    'Workflow Automation': ['apps-script-developer', 'data-analyst', 'system-integrator'],
    'Equity & Justice': ['equity-auditor', 'systems-change-analyst', 'academic-framework-researcher'],
    'Quality Control': ['quality-control-lead'],
}


def analyze_prompt(prompt):
    """Analyze prompt and return matching agents."""
    prompt_lower = prompt.lower()
    matches = []

    for agent, keywords in AGENT_TRIGGERS.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                if agent not in [m['agent'] for m in matches]:
                    matches.append({
                        'agent': agent,
                        'keyword': keyword
                    })
                break

    return matches


def get_team_for_agent(agent):
    """Get the team name for an agent."""
    for team, agents in TEAM_AGENTS.items():
        if agent in agents:
            return team
    return None


def main():
    """Main entry point for hook."""
    try:
        # Read prompt from stdin
        prompt = sys.stdin.read() if not sys.stdin.isatty() else ""

        if not prompt or len(prompt) < 10:
            sys.exit(0)

        matches = analyze_prompt(prompt)

        if matches:
            print("\n💡 APEX Agent Suggestions")
            print("─" * 40)

            # Group by team
            teams_suggested = {}
            for match in matches:
                team = get_team_for_agent(match['agent'])
                if team not in teams_suggested:
                    teams_suggested[team] = []
                teams_suggested[team].append(match['agent'])

            for team, agents in teams_suggested.items():
                if team:
                    print(f"\n{team}:")
                for agent in agents:
                    print(f"  • {agent}")

            print("\n─" * 40)

    except Exception as e:
        # Don't crash the workflow on hook errors
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
