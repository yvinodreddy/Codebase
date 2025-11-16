#!/bin/bash

################################################################################
# CLAUDE CODE WEB UI - LOCAL DEVELOPMENT SERVER
################################################################################
# Starts the development server on http://localhost:3000
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}║            CLAUDE CODE WEB UI - LOCAL SERVER                   ║${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Navigate to project directory
BASE_DIR="/home/user01/claude-test/ClaudePrompt/web-ui-implementation"
cd "$BASE_DIR"

################################################################################
# PRE-FLIGHT CHECKS
################################################################################

echo -e "${YELLOW}Running pre-flight checks...${NC}"

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo -e "${RED}✗ .env.local not found${NC}"
    echo ""
    echo "Please run the setup wizard first:"
    echo "  ${GREEN}./scripts/setup-wizard.sh${NC}"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ .env.local found${NC}"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${RED}✗ node_modules not found${NC}"
    echo ""
    echo "Installing dependencies..."
    npm install
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

echo -e "${GREEN}✓ node_modules found${NC}"

# Check if port 3000 is already in use
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Port 3000 is already in use${NC}"
    echo ""
    read -p "Kill existing process and continue? (y/n): " KILL_CHOICE
    if [ "$KILL_CHOICE" = "y" ] || [ "$KILL_CHOICE" = "Y" ]; then
        echo "Killing process on port 3000..."
        kill -9 $(lsof -t -i:3000) 2>/dev/null || true
        sleep 1
        echo -e "${GREEN}✓ Port 3000 freed${NC}"
    else
        echo "Exiting..."
        exit 1
    fi
else
    echo -e "${GREEN}✓ Port 3000 is available${NC}"
fi

echo ""

################################################################################
# START SERVER
################################################################################

echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                ║${NC}"
echo -e "${GREEN}║                  STARTING DEVELOPMENT SERVER                   ║${NC}"
echo -e "${GREEN}║                                                                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Server will be available at:${NC}"
echo -e "  ${GREEN}http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""
echo "────────────────────────────────────────────────────────────────"
echo ""

# Start the development server
npm run dev
