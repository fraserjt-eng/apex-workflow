---
name: data-visualization
description: "Create equity-focused data visualizations and dashboards. Use when building board presentations, equity reports, MTSS dashboards, or any data display requiring disaggregation and justice-centered framing. Ensures visualizations tell accurate stories without reinforcing deficit narratives."
---

# Equity Data Visualization

Create visualizations that illuminate systemic patterns while centering community voice and avoiding deficit framing.

## Core Principles

### 1. Disaggregate by Default

Never show aggregate data without breakdowns by:
- Race/ethnicity
- Gender
- Special education status
- English learner status
- Economic status (when available)
- Intersections where sample size allows

**Why:** Aggregate data hides disparities. "All students improved" may mask that some groups declined.

### 2. Context Over Numbers

- Always include systemic context
- Compare to opportunity, not just outcome
- Show trends, not just snapshots
- Include qualitative alongside quantitative
- Explain what numbers mean in human terms

**Example:**
Instead of: "65% proficiency rate"
Write: "65% of students met proficiency, up from 58% last year. Black students showed the largest gains (+12 points), reflecting our targeted intervention work."

### 3. Asset-Based Framing

- Lead with strengths where they exist
- Frame gaps as opportunities, not deficits
- Avoid colors that code students as "good/bad"
- Use neutral, accessible color palettes
- Celebrate progress, not just achievement

**Avoid:** "Students failed to meet standards"
**Use:** "Opportunity for growth remains" or "Students approaching proficiency"

### 4. Accessible Design

- Clear labels (no jargon)
- Appropriate for audience
- Mobile-friendly when digital
- Print-friendly when needed
- Color-blind accessible
- Alt text for screen readers

## Chart Selection Guide

| Data Type | Recommended | Avoid |
|-----------|-------------|-------|
| Comparisons across groups | Grouped bar, dot plot | Pie charts, 3D |
| Trends over time | Line chart, slope graph | Area charts (can mislead) |
| Part of whole | Stacked bar, treemap | Pie charts (hard to compare) |
| Relationships | Scatter plot | Overly complex bubble |
| Geographic | Choropleth with legend | Unlabeled maps |
| Distributions | Histogram, box plot | Overly simplified bar |
| Progress toward goal | Bullet chart, progress bar | Gauges, dials |

## Color Palette Guidelines

### BCCS Brand Colors
- Primary: #1E3A5F (BCCS Blue)
- Secondary: #4A90A4 (Teal)
- Accent: #F5A623 (Gold)
- Neutral: Grays for supporting elements

### Sequential Data (low to high)
Use single-hue progression:
```
Light Teal → Medium Teal → Dark Teal
#E0F4F7 → #4A90A4 → #1E5F6B
```

### Diverging Data (below/above target)
Use neutral center:
```
Orange (below) → Gray (at target) → Blue (above)
#E07B39 → #9CA3AF → #4A90A4
```

### Categorical Data
Distinct, accessible hues:
```
Blue: #4A90A4
Gold: #F5A623
Teal: #2D9CDB
Coral: #EB5757
Purple: #9B51E0
Green: #27AE60
```

### Avoid
- Red/green combinations (color blindness)
- Traffic light metaphors (judgmental)
- Colors that code students as "good" or "bad"
- More than 6 categories without grouping

## Dashboard Design Patterns

### Executive Dashboard (Board)
```
┌─────────────────────────────────────────────┐
│ KEY METRIC SUMMARY (3-4 big numbers)        │
├──────────────────────┬──────────────────────┤
│ TREND OVER TIME      │ COMPARISON BY GROUP  │
│ (line chart)         │ (bar chart)          │
├──────────────────────┴──────────────────────┤
│ PROGRESS TOWARD GOALS (bullet charts)       │
├─────────────────────────────────────────────┤
│ CONTEXT / STREET DATA (qualitative quotes)  │
└─────────────────────────────────────────────┘
```

### Equity Dashboard (Staff)
```
┌─────────────────────────────────────────────┐
│ DISPROPORTIONALITY INDICATORS (risk ratios) │
├──────────────────────┬──────────────────────┤
│ DEMOGRAPHIC BREAKDOWN │ OUTCOME BY GROUP     │
├──────────────────────┴──────────────────────┤
│ TREND ANALYSIS (are gaps closing?)          │
├─────────────────────────────────────────────┤
│ ACTION ITEMS (what we're doing about it)    │
└─────────────────────────────────────────────┘
```

### MTSS Dashboard (Teams)
```
┌─────────────────────────────────────────────┐
│ TIER DISTRIBUTION (% at each tier)          │
├─────────────────────────────────────────────┤
│ MOVEMENT BETWEEN TIERS (Sankey or flow)     │
├──────────────────────┬──────────────────────┤
│ BY DEMOGRAPHIC       │ BY INTERVENTION      │
├──────────────────────┴──────────────────────┤
│ STUDENTS NEEDING ATTENTION (actionable)     │
└─────────────────────────────────────────────┘
```

## Annotation Best Practices

Every visualization should include:

1. **Title:** Clear, descriptive, not clickbait
2. **Subtitle:** Context or key takeaway
3. **Source:** Where data came from, when collected
4. **Note:** Any caveats, sample size issues, methodology

**Example:**
```
Title: Math Proficiency by Race/Ethnicity, Grades 3-8
Subtitle: Black and Latinx students show strongest year-over-year gains
Source: MCA-III, Spring 2024 (n=1,247)
Note: Students with <95% attendance excluded per state methodology
```

## Scripts Available

Generate equity dashboard:
```bash
python scripts/equity_dashboard.py --data students.csv --metrics "attendance,discipline,grades"
```

Create disproportionality visualization:
```bash
python scripts/disprop_chart.py --data discipline.csv --group race --outcome suspended
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why Harmful | Better Approach |
|--------------|-------------|-----------------|
| Pie charts for comparison | Hard to compare slices | Use bar charts |
| 3D effects | Distorts perception | Keep it flat |
| Truncated y-axis | Exaggerates differences | Start at zero or label clearly |
| Red for low performers | Stigmatizing | Use neutral colors |
| "Achievement gap" framing | Deficit-focused | "Opportunity gap" or "education debt" |
| Aggregate only | Hides disparities | Always disaggregate |
| Data without context | Misleading | Include narrative |
| Too many categories | Overwhelming | Group or filter |

## Quality Checklist

Before presenting any visualization:

- [ ] Data is disaggregated by relevant demographics
- [ ] Context is provided (not just numbers)
- [ ] Framing is asset-based
- [ ] Colors are accessible and neutral
- [ ] Labels are clear (no jargon)
- [ ] Source and date are cited
- [ ] Story is told (not just data shown)
- [ ] Audience-appropriate complexity
- [ ] Mobile/print friendly as needed
- [ ] Street data included where possible

## Integration Points

- Use with `equity-audit` scripts for source data
- Apply `bccs-communications` language standards
- Follow `j-fraser-pedagogy` for presenting data in PD
- Consult `data-analyst` agent for complex analysis
