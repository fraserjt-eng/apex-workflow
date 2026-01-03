# Dependency Audit Report

**Date:** 2026-01-03
**Branch:** claude/audit-dependencies-mjxlfbqxn47zizcg-2DObK

## Executive Summary

This audit analyzes dependencies in the APEX Workflow plugin for outdated packages, security vulnerabilities, and unnecessary bloat.

| Category | Status | Action Required |
|----------|--------|-----------------|
| MCP Servers | Critical CVEs found | **Immediate** |
| Python Scripts | Clean (stdlib only) | None |
| Bash Scripts | Clean | None |
| Hook Configuration | 57% orphaned scripts | Cleanup needed |

---

## 1. MCP Server Dependencies

### Current Configuration (`.mcp.json`)

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-google-drive"]
    },
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-google-sheets"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem"]
    }
  }
}
```

### Issues Found

#### Critical: Security Vulnerabilities

**CVE-2025-53109 & CVE-2025-53110** - Filesystem MCP Server Sandbox Escape
- **CVSS Scores:** 8.4 / 7.3 (High)
- **Impact:** Path traversal and symlink attacks allow reading/writing files outside allowed directories
- **Affected:** All versions prior to 0.6.3
- **Fix:** Upgrade to version 0.6.3 or 2025.7.1

**CVE-2025-49596** - MCP Inspector RCE
- **CVSS Score:** 9.4 (Critical)
- **Impact:** Remote code execution via DNS rebinding when using MCP Inspector
- **Fix:** Ensure MCP Inspector version 0.14.1+ if used

#### High: Incorrect Package Names

The package names in `.mcp.json` appear to be incorrect:

| Current | Correct |
|---------|---------|
| `@anthropic/mcp-server-google-drive` | `@modelcontextprotocol/server-gdrive` |
| `@anthropic/mcp-server-google-sheets` | `@modelcontextprotocol/server-google-sheets` |
| `@anthropic/mcp-server-filesystem` | `@modelcontextprotocol/server-filesystem` |

#### Medium: No Version Pinning

Using `npx -y` without version specifiers means the latest version is always used, which could introduce breaking changes.

### Recommended `.mcp.json`

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive@latest"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "${GOOGLE_APPLICATION_CREDENTIALS}"
      },
      "description": "Access Google Drive files for APEX workflows"
    },
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-sheets@latest"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "${GOOGLE_APPLICATION_CREDENTIALS}"
      },
      "description": "Read/write Google Sheets for data analysis"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@0.6.3"],
      "env": {
        "ALLOWED_PATHS": "${HOME}/Documents/BCCS,${HOME}/Documents/APEX,${HOME}/Documents/Grants"
      },
      "description": "Access local files in allowed directories (pinned for security)"
    }
  }
}
```

---

## 2. Python Script Dependencies

### Analysis

All 10 Python scripts in `hooks/scripts/` use **only Python standard library modules**:

| Module | Scripts Using It |
|--------|-----------------|
| `sys` | All scripts |
| `os` | Most scripts |
| `re` | Pattern matching scripts |
| `json` | Hook input parsing |
| `pathlib` | File path handling |
| `fnmatch` | `protect-files.py` |
| `shutil` | `validate-environment.py` |
| `subprocess` | `format-on-edit.py` |

### Status: Excellent

- No external dependencies (pip packages) required
- No security vulnerabilities from third-party packages
- Easy to maintain and deploy

---

## 3. Bash Script Dependencies

### External Tools Used

| Tool | Script | Required | Fallback |
|------|--------|----------|----------|
| `jq` | `log-commands.sh` | No | grep/sed parsing |
| `notify-send` | `notify-*.sh` | No | Silent skip |
| `osascript` | `notify-*.sh` | No | Silent skip |

### Status: Good

All bash scripts handle missing tools gracefully with fallbacks or silent skips.

---

## 4. Orphaned Scripts (Bloat)

### Scripts Not Wired in `hooks.json`

| Script | Purpose | Lines | Recommendation |
|--------|---------|-------|----------------|
| `format-on-edit.py` | Auto-format after edits | 62 | Wire to PostToolUse or remove |
| `log-commands.sh` | Audit bash commands | 21 | Wire to PreToolUse:Bash or remove |
| `notify-complete.sh` | Desktop notification on complete | 27 | Wire to Stop or remove |
| `notify-input.sh` | Desktop notification for input | 27 | Wire to Notification or remove |
| `protect-files.py` | Block edits to sensitive files | 81 | **Wire to PreToolUse** (security) |
| `security-check.py` | Block commits with secrets | 91 | **Wire to PreToolUse** (security) |
| `validate-environment.py` | Check required tools | 77 | Wire to SessionStart or remove |
| `validate-prompt.py` | Agent routing hints | 77 | Wire to UserPromptSubmit or remove |

**Summary:** 8 of 14 scripts (57%) are not being used.

### Recommendations

1. **Enable security scripts** (high priority):
   ```json
   "PreToolUse": [
     {
       "matcher": "Edit|Write",
       "hooks": [
         {"type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/protect-files.py"},
         {"type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/security-check.py"},
         {"type": "command", "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/ferpa-check.py"}
       ]
     }
   ]
   ```

2. **Remove unused scripts** or wire them up based on your needs

---

## 5. format-on-edit.py Dependencies

This script assumes external formatters are available:

| Extension | Formatter | Install Command |
|-----------|-----------|-----------------|
| `.js`, `.ts`, `.json`, `.md` | Prettier | `npm install -g prettier` |
| `.py` | Black | `pip install black` |
| `.go` | gofmt | Included with Go |
| `.rs` | rustfmt | `rustup component add rustfmt` |

The script gracefully handles missing formatters (silent skip), but consider documenting these optional dependencies.

---

## 6. Action Items

### Critical (Do Immediately)

- [ ] Update `.mcp.json` with correct package names
- [ ] Pin `@modelcontextprotocol/server-filesystem` to version 0.6.3+
- [ ] Enable `security-check.py` in hooks.json

### High Priority

- [ ] Enable `protect-files.py` in hooks.json
- [ ] Verify MCP Inspector version if used (0.14.1+)

### Medium Priority

- [ ] Remove or wire up orphaned scripts
- [ ] Add environment validation on session start
- [ ] Document optional formatter dependencies

### Low Priority

- [ ] Consider enabling notification hooks for UX
- [ ] Add version pinning for all MCP servers

---

## References

- [CVE-2025-53109 & CVE-2025-53110 - Cymulate](https://cymulate.com/blog/cve-2025-53109-53110-escaperoute-anthropic/)
- [CVE-2025-49596 - Oligo Security](https://www.oligo.security/blog/critical-rce-vulnerability-in-anthropic-mcp-inspector-cve-2025-49596)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [MCP Security Best Practices](https://composio.dev/blog/mcp-vulnerabilities-every-developer-should-know)
