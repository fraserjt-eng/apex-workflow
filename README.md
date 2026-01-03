# APEX Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-v1.0.33+-blue.svg)](https://claude.ai/code)

**APEX: Autonomous Portfolio Execution & Strategic eXpert**

A Claude Code plugin for justice-centered educational transformation, featuring 21 specialized agents across 6 functional teams, 12 equity-focused skills, and production-grade automation hooks.

## Overview

APEX is designed for educational leaders doing equity work. It brings together specialized AI agents that understand justice-centered pedagogy, educational compliance, grant writing, and organizational transformation.

**Core Frameworks Integrated:**
- Four Pivots (Shawn Ginwright)
- Street Data (Shane Safir & Jamila Dugan)
- Culturally Responsive Teaching (Zaretta Hammond)
- MnMTSS (Minnesota Multi-tiered System of Supports)
- Restorative Practices
- Clear & Care (BCCS)

## Installation

```bash
# Clone the repository
git clone https://github.com/fraserjt-eng/apex-workflow.git

# Use with Claude Code
claude --plugin-dir ./apex-workflow
```

Or add to your project's `.claude/settings.json`:

```json
{
  "plugins": {
    "enabled": ["apex-workflow"]
  }
}
```

## 21 Specialized Agents

### Team 01: Grant Strategy (3 agents)
| Agent | Focus |
|-------|-------|
| `grant-writer` | Proposal development, narratives, RFP responses |
| `compliance-specialist` | ESSA, Title programs, MDE requirements |
| `budget-analyst` | Grant budgets, fiscal compliance |

### Team 02: Strategic Communication (3 agents)
| Agent | Focus |
|-------|-------|
| `justice-centered-communicator` | Multi-stakeholder messaging |
| `presentation-designer` | Board presentations, slides |
| `stakeholder-strategist` | Political navigation, relationships |

### Team 03: Professional Learning (3 agents)
| Agent | Focus |
|-------|-------|
| `curriculum-designer` | PD sessions, curriculum development |
| `principal-coach` | Leadership coaching, reflective practice |
| `pd-facilitator` | Facilitation protocols, adult learning |

### Team 04: Workflow Automation (3 agents)
| Agent | Focus |
|-------|-------|
| `apps-script-developer` | Google Apps Script automation |
| `data-analyst` | Data analysis, visualization, dashboards |
| `system-integrator` | Cross-system workflows, integrations |

### Team 05: Equity & Justice (3 agents)
| Agent | Focus |
|-------|-------|
| `equity-auditor` | Disproportionality analysis, equity audits |
| `systems-change-analyst` | Theory of action, change management |
| `academic-framework-researcher` | Research base, citations, frameworks |

### Team 06: Quality Control (5 agents)
| Agent | Focus |
|-------|-------|
| `quality-control-lead` | Final review, standards enforcement |
| `confirmation-bias-detector` | Challenge assumptions, find blind spots |
| `ai-hallucination-validator` | Verify facts, data, citations |
| `source-verification-agent` | Primary source validation |
| `ai-detection-specialist` | Ensure authentic voice |

### Master Orchestrator
| Agent | Focus |
|-------|-------|
| `apex-orchestrator` | AI Chief of Staff - coordinates all teams with Working Genius alignment |

## Commands

| Command | Description |
|---------|-------------|
| `/apex:scan` | Monday portfolio scan - reviews priorities |
| `/apex:assign` | Route task to specific team |
| `/apex:validate` | Trigger QC review |
| `/apex:report` | Generate portfolio report |
| `/apex:pedagogy` | Activate J Fraser pedagogy protocol |
| `/apex:equity` | Apply equity lens analysis |
| `/apex:strategic` | Strategic planning mode (board-ready, long-term thinking) |
| `/apex:coaching` | Reflective coaching mode (questions before answers) |
| `/apex:review` | Quality review mode (structured feedback) |
| `/apex:rapid` | Fast execution mode (essential standards only) |

## Skills

The plugin includes 12 knowledge skills with progressive disclosure:

| Skill | Description |
|-------|-------------|
| `j-fraser-pedagogy` | Signature pedagogical approach with session templates |
| `four-pivots` | Ginwright's healing-centered framework |
| `street-data` | Safir & Dugan's qualitative methodology |
| `culturally-responsive` | Hammond's Ready for Rigor |
| `mtss-implementation` | Multi-tiered system of supports |
| `equity-audit` | Systematic equity analysis with Python scripts |
| `restorative-practices` | Community and harm repair |
| `clear-and-care` | BCCS organizational culture |
| `apps-script` | Google Apps Script automation patterns |
| `bccs-communications` | Justice-centered stakeholder communications |
| `grant-strategy` | Grant writing and compliance |
| `data-visualization` | Equity-focused data visualization |

### Analysis Scripts

The `equity-audit` skill includes executable Python scripts:

```bash
# Calculate disproportionality ratios
python skills/equity-audit/scripts/disproportionality.py \
  --data discipline.csv --group race_ethnicity --outcome suspended

# Disaggregate data by demographics
python skills/equity-audit/scripts/disaggregate.py \
  --data students.csv --by "race,gender,sped,ell" --metric gpa
```

## Hooks

APEX includes production-grade automated hooks:

| Hook | Trigger | Function |
|------|---------|----------|
| Session Init | Session start | Welcome message, agent overview |
| Prompt Analyzer | User input | Suggests relevant agents |
| FERPA Check | Before file write | Scans for student PII with severity levels |
| Pedagogy Check | After file write | Validates Experience→Analysis→Framework sequence |
| Equity Language | After file write | Flags deficit language with alternatives |
| Session Summary | Session end | Closing summary |

## Core Principles

All APEX agents operate on these principles:

### High Warmth + High Structure
Both are required. Never sacrifice one for the other. Target: Thriving Communities quadrant.

### Experience → Analysis → Framework
Start with concrete experience, then analyze, THEN introduce frameworks. Never lecture first.

### Mirror Before Lens
Personal reflection before systemic critique. "What patterns do I perpetuate?"

### Street Data Weighted Equally
Qualitative, experiential data matters as much as quantitative. Always include both (40% weight).

### Asset-Based Without Avoidance
Lead with community strengths AND name specific harms. No toxic positivity, no deficit-only framing.

## Portfolio Structure

APEX is designed for multi-portfolio leadership:

| Portfolio | Allocation | Focus |
|-----------|------------|-------|
| BCCS District Leadership | 60-70% | Board, compliance, PD, systems |
| Creative Ventures | 15-20% | Coaching, writing, speaking |
| Business Development | 10-15% | Consulting, revenue |
| Non-Profit Planning | 5-10% | Community partnerships |

## File Structure

```
apex-workflow/
├── .claude-plugin/
│   ├── plugin.json              # Plugin metadata
│   └── marketplace.json         # Marketplace registry
├── agents/
│   ├── apex-orchestrator.md     # Master orchestrator with Working Genius
│   ├── team-01-grant-strategy/
│   │   ├── grant-writer.md
│   │   ├── compliance-specialist.md
│   │   └── budget-analyst.md
│   ├── team-02-strategic-comm/
│   ├── team-03-professional-learning/
│   ├── team-04-workflow-automation/
│   ├── team-05-equity-justice/
│   └── team-06-quality-control/
├── commands/                     # 10 slash commands
│   ├── portfolio-scan.md
│   ├── apex-rapid.md
│   └── ...
├── hooks/
│   ├── hooks.json               # Hook configuration
│   └── scripts/                 # Production-grade Python hooks
│       ├── ferpa-check.py
│       ├── equity-language.py
│       ├── pedagogy-check.py
│       └── ...
├── skills/                       # 12 knowledge skills
│   ├── j-fraser-pedagogy/
│   │   ├── SKILL.md
│   │   ├── references/          # Progressive disclosure
│   │   │   ├── four-pivots.md
│   │   │   └── warmth-structure.md
│   │   └── assets/
│   │       └── session-outline.md
│   ├── equity-audit/
│   │   ├── SKILL.md
│   │   └── scripts/             # Executable analysis tools
│   │       ├── disproportionality.py
│   │       └── disaggregate.py
│   ├── bccs-communications/
│   ├── grant-strategy/
│   ├── data-visualization/
│   └── ...
├── growth/                       # Dormant features for future
│   ├── frontend/
│   ├── payments/
│   ├── multi-model/
│   └── infrastructure/
├── PERMISSIONS.md
└── README.md
```

## Configuration

See [PERMISSIONS.md](PERMISSIONS.md) for detailed permission templates.

### Recommended Setup

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(docs/**)",
      "Write(outputs/**)",
      "Bash(python3:*)",
      "Bash(git:status)"
    ]
  }
}
```

## Contributing

Contributions welcome! Please ensure any additions:
- Follow justice-centered principles
- Include appropriate documentation
- Pass equity language review
- Use asset-based framing

## License

MIT License - Adapted from [CloudAI-X/claude-workflow](https://github.com/CloudAI-X/claude-workflow)

## Acknowledgments

- **Shawn Ginwright** - Four Pivots framework
- **Shane Safir & Jamila Dugan** - Street Data methodology
- **Zaretta Hammond** - Culturally Responsive Teaching
- **Patrick Lencioni** - Working Genius model
- **CloudAI-X** - Original claude-workflow plugin architecture
- **Anthropic** - Skills design patterns

---

> "You can't have transformation through just transactional relationships."
> — Shawn Ginwright
