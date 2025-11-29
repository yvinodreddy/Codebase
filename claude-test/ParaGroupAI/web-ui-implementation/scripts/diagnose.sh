#!/bin/bash

################################################################################
# CLAUDE CODE WEB UI - DIAGNOSTIC TOOL
################################################################################
# Checks your setup and identifies issues
################################################################################

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}║              CLAUDE CODE WEB UI - DIAGNOSTICS                  ║${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Navigate to project directory
BASE_DIR="/home/user01/claude-test/ClaudePrompt/web-ui-implementation"
cd "$BASE_DIR"

ISSUES_FOUND=0

################################################################################
# CHECK 1: Node.js and npm
################################################################################

echo -e "${YELLOW}[CHECK 1] Node.js and npm${NC}"

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js installed: $NODE_VERSION${NC}"

    MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$MAJOR_VERSION" -lt 18 ]; then
        echo -e "${RED}✗ Node.js version must be 18 or higher${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${RED}✗ Node.js not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm installed: $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

echo ""

################################################################################
# CHECK 2: Required Files
################################################################################

echo -e "${YELLOW}[CHECK 2] Required Files${NC}"

if [ -f "package.json" ]; then
    echo -e "${GREEN}✓ package.json exists${NC}"
else
    echo -e "${RED}✗ package.json not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ -f ".env.local" ]; then
    echo -e "${GREEN}✓ .env.local exists${NC}"
else
    echo -e "${RED}✗ .env.local not found${NC}"
    echo "  Solution: Run ./scripts/setup-wizard.sh"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ -f "next.config.js" ]; then
    echo -e "${GREEN}✓ next.config.js exists${NC}"
else
    echo -e "${RED}✗ next.config.js not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ -f "tsconfig.json" ]; then
    echo -e "${GREEN}✓ tsconfig.json exists${NC}"
else
    echo -e "${RED}✗ tsconfig.json not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

echo ""

################################################################################
# CHECK 3: Dependencies
################################################################################

echo -e "${YELLOW}[CHECK 3] Dependencies${NC}"

if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓ node_modules exists${NC}"

    # Check key dependencies
    if [ -d "node_modules/next" ]; then
        echo -e "${GREEN}✓ Next.js installed${NC}"
    else
        echo -e "${RED}✗ Next.js not installed${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if [ -d "node_modules/react" ]; then
        echo -e "${GREEN}✓ React installed${NC}"
    else
        echo -e "${RED}✗ React not installed${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if [ -d "node_modules/@anthropic-ai/sdk" ]; then
        echo -e "${GREEN}✓ Anthropic SDK installed${NC}"
    else
        echo -e "${RED}✗ Anthropic SDK not installed${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${RED}✗ node_modules not found${NC}"
    echo "  Solution: Run npm install"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

echo ""

################################################################################
# CHECK 4: Environment Variables
################################################################################

echo -e "${YELLOW}[CHECK 4] Environment Variables${NC}"

if [ -f ".env.local" ]; then
    if grep -q "GOOGLE_CLIENT_ID" .env.local; then
        echo -e "${GREEN}✓ GOOGLE_CLIENT_ID is set${NC}"
    else
        echo -e "${RED}✗ GOOGLE_CLIENT_ID not found in .env.local${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if grep -q "GOOGLE_CLIENT_SECRET" .env.local; then
        echo -e "${GREEN}✓ GOOGLE_CLIENT_SECRET is set${NC}"
    else
        echo -e "${RED}✗ GOOGLE_CLIENT_SECRET not found in .env.local${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if grep -q "JWT_SECRET" .env.local; then
        echo -e "${GREEN}✓ JWT_SECRET is set${NC}"
    else
        echo -e "${RED}✗ JWT_SECRET not found in .env.local${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if grep -q "NEXT_PUBLIC_APP_URL" .env.local; then
        echo -e "${GREEN}✓ NEXT_PUBLIC_APP_URL is set${NC}"
    else
        echo -e "${RED}✗ NEXT_PUBLIC_APP_URL not found in .env.local${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${RED}✗ .env.local not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

echo ""

################################################################################
# CHECK 5: Source Files
################################################################################

echo -e "${YELLOW}[CHECK 5] Source Files${NC}"

if [ -f "src/lib/auth.ts" ]; then
    echo -e "${GREEN}✓ auth.ts exists${NC}"
else
    echo -e "${RED}✗ auth.ts not found${NC}"
    echo "  Solution: Run ./scripts/generate-all-files.sh"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ -f "src/lib/claude-client.ts" ]; then
    echo -e "${GREEN}✓ claude-client.ts exists${NC}"
else
    echo -e "${RED}✗ claude-client.ts not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ -f "src/pages/api/auth/oauth.ts" ]; then
    echo -e "${GREEN}✓ API routes exist${NC}"
else
    echo -e "${RED}✗ API routes not found${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

echo ""

################################################################################
# CHECK 6: Port Availability
################################################################################

echo -e "${YELLOW}[CHECK 6] Port Availability${NC}"

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    PID=$(lsof -t -i:3000)
    echo -e "${YELLOW}⚠ Port 3000 is in use (PID: $PID)${NC}"
    echo "  Solution: Kill the process with: kill -9 $PID"
else
    echo -e "${GREEN}✓ Port 3000 is available${NC}"
fi

echo ""

################################################################################
# CHECK 7: Git Configuration
################################################################################

echo -e "${YELLOW}[CHECK 7] Git Configuration${NC}"

if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git initialized${NC}"

    if git remote get-url origin &> /dev/null; then
        REMOTE_URL=$(git remote get-url origin)
        echo -e "${GREEN}✓ Git remote set: $REMOTE_URL${NC}"
    else
        echo -e "${YELLOW}⚠ Git remote not set${NC}"
        echo "  Not required for local testing"
    fi
else
    echo -e "${YELLOW}⚠ Git not initialized${NC}"
    echo "  Not required for local testing"
fi

echo ""

################################################################################
# SUMMARY
################################################################################

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}DIAGNOSTIC SUMMARY${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║              ✓ ALL CHECKS PASSED!                              ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Your setup is ready!"
    echo ""
    echo "To start the local server:"
    echo "  ${GREEN}./scripts/run-local.sh${NC}"
    echo ""
    echo "To deploy to production:"
    echo "  ${GREEN}./scripts/deploy-to-netlify.sh${NC}"
    echo ""
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}║              ✗ ISSUES FOUND: $ISSUES_FOUND                                 ║${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Please fix the issues above."
    echo ""
    echo "Common solutions:"
    echo "  - Run setup wizard: ${GREEN}./scripts/setup-wizard.sh${NC}"
    echo "  - Install dependencies: ${GREEN}npm install${NC}"
    echo "  - Generate files: ${GREEN}./scripts/generate-all-files.sh${NC}"
    echo ""
fi
