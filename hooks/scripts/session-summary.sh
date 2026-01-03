#!/bin/bash
# APEX Session Summary
# Runs when Claude Code session ends

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/../..}"
LOG_DIR="${PLUGIN_ROOT}/logs"

# Log session end
echo "$(date '+%Y-%m-%d %H:%M:%S') - APEX Session Ended" >> "$LOG_DIR/sessions.log"

# Display closing message
cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║                   APEX Session Complete                       ║
╚═══════════════════════════════════════════════════════════════╝

📊 Remember to review any high-stakes deliverables with QC team.

💭 "You can't have transformation through just transactional
    relationships." — Shawn Ginwright

EOF
