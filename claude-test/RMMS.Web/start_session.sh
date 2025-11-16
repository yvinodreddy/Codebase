#!/bin/bash

# RMMS Implementation - Session Start Script
# This script automates your session startup routine

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  RMMS Implementation - Session Start                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Change to project directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)

echo "📁 Project Directory: $PROJECT_DIR"
echo ""

# Function to show colored output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Check Git Status
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔍 Checking Git Status...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d ".git" ]; then
    git status -s
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Git repository OK${NC}"
    else
        echo -e "${RED}✗ Git repository has issues${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Not a git repository - initializing...${NC}"
    git init
    git add .
    git commit -m "Initial commit - baseline"
    git tag "baseline-before-phase1"
fi
echo ""

# 2. Show Current Session State
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📍 CURRENT SESSION STATE${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "CURRENT_SESSION.md" ]; then
    echo -e "${GREEN}Current Step:${NC}"
    grep "Current Step:" CURRENT_SESSION.md | head -1
    echo ""

    echo -e "${GREEN}Last Completed:${NC}"
    grep "Last Completed:" CURRENT_SESSION.md -A 1 | head -2
    echo ""

    echo -e "${GREEN}Next Action:${NC}"
    grep "Next Action:" CURRENT_SESSION.md -A 3 | head -4
    echo ""
else
    echo -e "${YELLOW}⚠ CURRENT_SESSION.md not found${NC}"
    echo "Creating default CURRENT_SESSION.md..."
    cat > CURRENT_SESSION.md << 'EOF'
# Current Session State
**Last Updated:** $(date '+%Y-%m-%d %H:%M:%S')
**Current Step:** 1.1
**Last Completed:** None
**Next Action:** Start Step 1.1 - Database Foundation Setup
EOF
    echo -e "${GREEN}✓ Created CURRENT_SESSION.md${NC}"
fi
echo ""

# 3. Show Overall Progress
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📊 OVERALL PROGRESS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "PROGRESS_TRACKER.md" ]; then
    grep "Overall Progress:" PROGRESS_TRACKER.md | head -1
    echo ""
    grep "Sprint 1" PROGRESS_TRACKER.md | head -3
else
    echo -e "${YELLOW}⚠ PROGRESS_TRACKER.md not found${NC}"
fi
echo ""

# 4. Review Yesterday's Work
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📅 YESTERDAY'S WORK${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

YESTERDAY=$(date -d "yesterday" '+%Y-%m-%d' 2>/dev/null || date -v-1d '+%Y-%m-%d')
YESTERDAY_LOG="implementation_logs/${YESTERDAY}.md"

if [ -f "$YESTERDAY_LOG" ]; then
    echo -e "${GREEN}Yesterday's Log Found: $YESTERDAY_LOG${NC}"
    echo ""
    echo "Last 10 lines:"
    tail -10 "$YESTERDAY_LOG"
else
    echo -e "${YELLOW}No log found for yesterday ($YESTERDAY)${NC}"

    # Find most recent log
    LATEST_LOG=$(ls -t implementation_logs/*.md 2>/dev/null | head -1)
    if [ -n "$LATEST_LOG" ]; then
        echo -e "${BLUE}Most recent log: $LATEST_LOG${NC}"
        echo ""
        echo "Last 5 lines:"
        tail -5 "$LATEST_LOG"
    fi
fi
echo ""

# 5. Create Today's Log
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📝 TODAY'S SESSION LOG${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TODAY=$(date '+%Y-%m-%d')
TODAY_LOG="implementation_logs/${TODAY}.md"

# Create logs directory if it doesn't exist
mkdir -p implementation_logs

if [ -f "$TODAY_LOG" ]; then
    echo -e "${YELLOW}Today's log already exists: $TODAY_LOG${NC}"
    echo "Appending new session entry..."
    cat >> "$TODAY_LOG" << EOF

---

## New Session: $(date '+%H:%M:%S')

### Resume Point:
$(grep "Next Action:" CURRENT_SESSION.md -A 3 | head -4)

EOF
else
    echo -e "${GREEN}Creating today's log: $TODAY_LOG${NC}"
    cat > "$TODAY_LOG" << EOF
# Session Log: $TODAY
## Start Time: $(date '+%H:%M:%S')

---

## 📋 Session Information

**Date:** $TODAY
**Day:** $(date '+%A')
**Developer:** [Your Name]

---

## 🎯 Today's Goal

$(cat CURRENT_SESSION.md | grep "TODAY'S PLAN" -A 10 2>/dev/null || echo "No plan found in CURRENT_SESSION.md")

---

## 🔄 Starting Context

**Current Step:**
$(grep "Current Step:" CURRENT_SESSION.md 2>/dev/null || echo "Unknown")

**Next Action:**
$(grep "Next Action:" CURRENT_SESSION.md -A 3 2>/dev/null || echo "Unknown")

---

## ⏰ Work Log

### $(date '+%H:%M') - Session Start
- Reviewed CURRENT_SESSION.md
- Reviewed PROGRESS_TRACKER.md
- Created today's session log
- Ready to start work

EOF
fi
echo ""

# 6. Show Recent Commits
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔖 RECENT GIT COMMITS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git log --oneline -5 2>/dev/null || echo "No git commits yet"
echo ""

# 7. Check Database Connectivity (optional)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🗄️  DATABASE CHECK${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v sqlcmd &> /dev/null; then
    sqlcmd -S localhost -d RMMS_Production -Q "SELECT TOP 1 'Database Connected' AS Status" -h -1 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Database connection OK${NC}"
    else
        echo -e "${YELLOW}⚠ Database connection failed (this may be normal if not set up yet)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ sqlcmd not found - skipping database check${NC}"
fi
echo ""

# 8. Quick Actions Menu
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🚀 QUICK ACTIONS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "What would you like to do?"
echo ""
echo "1) Open VS Code and start working"
echo "2) View detailed implementation guide for current step"
echo "3) View progress tracker"
echo "4) Build and run the application"
echo "5) View today's log in editor"
echo "6) Exit (I'll set up myself)"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo -e "${GREEN}Opening VS Code...${NC}"
        code .
        ;;
    2)
        CURRENT_STEP=$(grep "Current Step:" CURRENT_SESSION.md | cut -d: -f2 | xargs | cut -d' ' -f1)
        echo -e "${GREEN}Showing implementation guide for step $CURRENT_STEP${NC}"
        grep "STEP $CURRENT_STEP" IMPLEMENTATION_GUIDE_STEP_BY_STEP.md -A 100 | head -100
        ;;
    3)
        echo -e "${GREEN}Opening Progress Tracker...${NC}"
        less PROGRESS_TRACKER.md
        ;;
    4)
        echo -e "${GREEN}Building application...${NC}"
        dotnet build
        if [ $? -eq 0 ]; then
            echo ""
            read -p "Build successful! Run the application? (y/n): " run_choice
            if [ "$run_choice" = "y" ]; then
                echo -e "${GREEN}Running application... (Press Ctrl+C to stop)${NC}"
                dotnet run
            fi
        fi
        ;;
    5)
        echo -e "${GREEN}Opening today's log in editor...${NC}"
        ${EDITOR:-nano} "$TODAY_LOG"
        ;;
    6)
        echo -e "${GREEN}✓ Session initialized. Happy coding!${NC}"
        ;;
    *)
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ Session Start Complete${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Quick Reference:"
echo "  - View current state: cat CURRENT_SESSION.md"
echo "  - View progress: cat PROGRESS_TRACKER.md"
echo "  - View today's log: cat $TODAY_LOG"
echo "  - Open VS Code: code ."
echo ""
echo "🎯 Your next action:"
cat CURRENT_SESSION.md | grep "Next Action:" -A 5 | head -6
echo ""
echo "Good luck! 🚀"
echo ""
