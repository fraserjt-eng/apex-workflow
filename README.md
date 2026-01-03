# APEX Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-v1.0.33+-blue.svg)](https://claude.ai/code)

**APEX: Autonomous Portfolio Execution & Strategic eXpert**

A Claude Code plugin for justice-centered educational transformation, featuring 21 specialized agents across 6 functional teams.

## Overview

APEX is designed for educational leaders doing equity work. It brings together specialized AI agents that understand justice-centered pedagogy, educational compliance, grant writing, and organizational transformation.

**Core Frameworks Integrated:**
- Four Pivots (Shawn Ginwright)
- Street Data (Shane Safir & Jamila Dugan)
- Culturally Responsive Teaching (Zaretta Hammond)
- MnMTSS (Minnesota Multi-tiered System of Supports)
- Restorative Practices

## Installation

```bash
# Clone the repository
git clone https://github.com/jfraser/apex-workflow.git

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

### Grant Strategy Team (3 agents)
| Agent | Focus |
|-------|-------|
| `grant-writer` | Proposal development, narratives, RFP responses |
| `compliance-specialist` | ESSA, Title programs, MDE requirements |
| `budget-analyst` | Grant budgets, fiscal compliance |

### Strategic Communication Team (3 agents)
| Agent | Focus |
|-------|-------|
| `justice-centered-communicator` | Multi-stakeholder messaging |
| `presentation-designer` | Board presentations, slides |
| `stakeholder-strategist` | Political navigation, relationships |

### Professional Learning Team (3 agents)
| Agent | Focus |
|-------|-------|
| `curriculum-designer` | PD sessions, curriculum development |
| `principal-coach` | Leadership coaching, reflective practice |
| `pd-facilitator` | Facilitation protocols, adult learning |

### Workflow Automation Team (3 agents)
| Agent | Focus |
|-------|-------|
| `apps-script-developer` | Google Apps Script automation |
| `data-analyst` | Data analysis, visualization, dashboards |
| `system-integrator` | Cross-system workflows, integrations |

### Equity & Justice Team (3 agents)
| Agent | Focus |
|-------|-------|
| `equity-auditor` | Disproportionality analysis, equity audits |
| `systems-change-analyst` | Theory of action, change management |
| `academic-framework-researcher` | Research base, citations, frameworks |

### Quality Control Team (5 agents)
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
| `apex-orchestrator` | AI Chief of Staff - coordinates all teams |

## Commands

| Command | Description |
|---------|-------------|
| `/apex:scan` | Monday portfolio scan - reviews priorities |
| `/apex:assign` | Route task to specific team |
| `/apex:validate` | Trigger QC review |
| `/apex:report` | Generate portfolio report |
| `/apex:pedagogy` | Activate J Fraser pedagogy protocol |
| `/apex:equity` | Apply equity lens analysis |

## Skills

The plugin includes 8 knowledge skills:

| Skill | Description |
|-------|-------------|
| `j-fraser-pedagogy` | Signature pedagogical approach |
| `four-pivots` | Ginwright's healing-centered framework |
| `street-data` | Safir & Dugan's qualitative methodology |
| `culturally-responsive` | Hammond's Ready for Rigor |
| `mtss-implementation` | Multi-tiered system of supports |
| `equity-audit` | Systematic equity analysis |
| `restorative-practices` | Community and harm repair |
| `clear-and-care` | BCCS organizational culture |

## Hooks

APEX includes automated hooks that run at key moments:

| Hook | Trigger | Function |
|------|---------|----------|
| Session Init | Session start | Welcome message, agent overview |
| Prompt Analyzer | User input | Suggests relevant agents |
| FERPA Check | Before file write | Scans for student PII |
| Pedagogy Check | After file write | Validates pedagogy protocol |
| Equity Language | After file write | Flags deficit language |
| Session Summary | Session end | Closing summary |

## Core Principles

All APEX agents operate on these principles:

### High Warmth + High Structure
Both are required. Never sacrifice one for the other.

### Experience → Analysis → Framework
Start with concrete experience, then analyze, THEN introduce frameworks. Never lecture first.

### Mirror Before Lens
Personal reflection before systemic critique. "What patterns do I perpetuate?"

### Street Data Weighted Equally
Qualitative, experiential data matters as much as quantitative. Always include both.

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
│   └── plugin.json          # Plugin metadata
├── agents/                   # 21 agent definitions
│   ├── apex-orchestrator.md
│   ├── grant-writer.md
│   └── ...
├── commands/                 # 6 slash commands
│   ├── portfolio-scan.md
│   ├── pedagogy.md
│   └── ...
├── hooks/
│   ├── hooks.json           # Hook configuration
│   └── scripts/             # Hook scripts
│       ├── ferpa-check.py
│       └── ...
├── skills/                   # 8 knowledge skills
│   ├── j-fraser-pedagogy/
│   ├── four-pivots/
│   └── ...
├── PERMISSIONS.md            # Permission templates
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

## License

MIT License - Adapted from [CloudAI-X/claude-workflow](https://github.com/CloudAI-X/claude-workflow)

## Acknowledgments

- **Shawn Ginwright** - Four Pivots framework
- **Shane Safir & Jamila Dugan** - Street Data methodology
- **Zaretta Hammond** - Culturally Responsive Teaching
- **CloudAI-X** - Original claude-workflow plugin architecture

---

> "You can't have transformation through just transactional relationships."
> — Shawn Ginwright
