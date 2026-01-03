# APEX Workflow Permissions

This document provides recommended permission templates for your `.claude/settings.local.json` file when using the APEX workflow plugin.

## Permission Levels

### Minimum (Read-Only Analysis)

Use this for exploratory work where you only need to read and analyze without writing files.

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Bash(python3:*analysis*)"
    ]
  }
}
```

### Standard (Most APEX Work)

Recommended for typical day-to-day APEX operations including document creation and data analysis.

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(docs/**)",
      "Edit(outputs/**)",
      "Edit(drafts/**)",
      "Write(outputs/**)",
      "Write(drafts/**)",
      "Bash(python3:*)",
      "Bash(node:*)",
      "Bash(git:status)",
      "Bash(git:diff)",
      "Bash(git:log)"
    ],
    "deny": [
      "Write(.env*)",
      "Write(**/credentials*)",
      "Write(**/*.key)",
      "Edit(.git/**)"
    ]
  }
}
```

### Full (All APEX Capabilities)

For power users who need full APEX functionality including automation development.

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(**)",
      "Write(**)",
      "Bash(*)"
    ],
    "deny": [
      "Bash(rm:-rf:*)",
      "Bash(sudo:*)",
      "Write(.env*)",
      "Write(**/credentials*)",
      "Write(**/*.key)",
      "Write(**/*secret*)",
      "Edit(.git/**)"
    ]
  }
}
```

## FERPA Compliance Permissions

When working with student data, use these additional restrictions:

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(analysis/**)",
      "Write(analysis/**)"
    ],
    "deny": [
      "Write(**/student*)",
      "Write(**/roster*)",
      "Write(**/pii*)",
      "Write(**/grades*)",
      "Write(exports/**)",
      "Edit(**/student*)"
    ]
  }
}
```

### FERPA Best Practices

1. **Never allow Write permissions** to directories containing student PII
2. **Use the FERPA hook** to scan for sensitive data patterns
3. **Keep student data analysis outputs** in secure, non-synced directories
4. **Review outputs before sharing** to ensure no PII leaked through
5. **Use aggregated data** whenever possible instead of individual records

## Agent-Specific Permissions

### Grant Strategy Team

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(grants/**)",
      "Write(grants/**)",
      "Edit(budgets/**)",
      "Write(budgets/**)"
    ]
  }
}
```

### Workflow Automation Team

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(scripts/**)",
      "Write(scripts/**)",
      "Bash(node:*)",
      "Bash(python3:*)",
      "Bash(npm:*)"
    ]
  }
}
```

### Quality Control Team

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "WebSearch(*)",
      "WebFetch(*)"
    ]
  }
}
```

## Project-Level Auto-Permissions

To auto-enable APEX for team members, add this to your project's `.claude/settings.json`:

```json
{
  "plugins": {
    "enabled": [
      "apex-workflow"
    ]
  }
}
```

## Security Recommendations

### Always Deny

These patterns should always be denied for security:

```json
{
  "deny": [
    "Bash(rm:-rf:*)",
    "Bash(sudo:*)",
    "Bash(chmod:777:*)",
    "Write(.env*)",
    "Write(**/*.pem)",
    "Write(**/*.key)",
    "Write(**/credentials*)",
    "Write(**/secrets*)",
    "Write(**/password*)",
    "Edit(.git/**)"
  ]
}
```

### Audit Logging

Consider enabling command logging for sensitive operations:

```json
{
  "hooks": {
    "Bash": {
      "command": "echo \"$(date): $@\" >> ~/.claude/audit.log"
    }
  }
}
```

## Troubleshooting

### "Permission denied" errors

1. Check your `.claude/settings.local.json` for typos
2. Ensure patterns match the file paths correctly
3. Use more specific patterns if wildcards are too broad

### Hooks not running

1. Ensure Python 3 is installed and accessible
2. Check that hook scripts are executable (`chmod +x`)
3. Verify `${CLAUDE_PLUGIN_ROOT}` is resolving correctly

### Agent not available

1. Verify the agent file exists in `agents/` directory
2. Check the agent's YAML frontmatter for syntax errors
3. Ensure the agent name matches how you're calling it
