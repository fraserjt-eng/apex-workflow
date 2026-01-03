#!/bin/bash
# APEX Session Initialization
# Runs at the start of each Claude Code session

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/../..}"
LOG_DIR="${PLUGIN_ROOT}/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log session start
echo "$(date '+%Y-%m-%d %H:%M:%S') - APEX Session Started" >> "$LOG_DIR/sessions.log"

# Display welcome message
cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   █████╗ ██████╗ ███████╗██╗  ██╗                            ║
║  ██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝                            ║
║  ███████║██████╔╝█████╗   ╚███╔╝                             ║
║  ██╔══██║██╔═══╝ ██╔══╝   ██╔██╗                             ║
║  ██║  ██║██║     ███████╗██╔╝ ██╗                            ║
║  ╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝                            ║
║                                                               ║
║  Autonomous Portfolio Execution & Strategic eXpert            ║
║  Justice-Centered Educational Transformation                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

🚀 APEX Workflow Initialized

📋 21 agents available across 6 teams:
   • Grant Strategy (3)
   • Strategic Communication (3)
   • Professional Learning (3)
   • Workflow Automation (3)
   • Equity & Justice (3)
   • Quality Control (5)
   • APEX Orchestrator (1)

⚡ Quick Commands:
   /apex:scan      - Monday portfolio scan
   /apex:pedagogy  - Activate J Fraser pedagogy protocol
   /apex:equity    - Apply equity lens
   /apex:validate  - Trigger QC review
   /apex:report    - Generate portfolio report

💡 The system prioritizes:
   • High Warmth + High Structure
   • Experience → Analysis → Framework
   • Street Data alongside Satellite Data
   • Justice-centered language

EOF
