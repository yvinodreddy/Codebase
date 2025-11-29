#!/bin/bash

################################################################################
# CLAUDE CODE WEB UI - NETLIFY DEPLOYMENT
################################################################################
# Deploys the application to Netlify (paragroupcli.netlify.app)
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
echo -e "${BLUE}║           CLAUDE CODE WEB UI - NETLIFY DEPLOYMENT              ║${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Navigate to project directory
BASE_DIR="/home/user01/claude-test/ClaudePrompt/web-ui-implementation"
cd "$BASE_DIR"

################################################################################
# PRE-DEPLOYMENT CHECKS
################################################################################

echo -e "${YELLOW}Running pre-deployment checks...${NC}"

# Check if .env.production exists
if [ ! -f ".env.production" ]; then
    echo -e "${RED}✗ .env.production not found${NC}"
    echo ""
    echo "Please run the setup wizard first:"
    echo "  ${GREEN}./scripts/setup-wizard.sh${NC}"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ .env.production found${NC}"

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo -e "${YELLOW}⚠ Netlify CLI not found${NC}"
    echo "Installing Netlify CLI..."
    npm install -g netlify-cli
    echo -e "${GREEN}✓ Netlify CLI installed${NC}"
else
    echo -e "${GREEN}✓ Netlify CLI found${NC}"
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠ Git not initialized${NC}"
    read -p "Initialize git repository? (y/n): " GIT_CHOICE
    if [ "$GIT_CHOICE" = "y" ] || [ "$GIT_CHOICE" = "Y" ]; then
        git init
        echo -e "${GREEN}✓ Git initialized${NC}"
    fi
fi

echo ""

################################################################################
# DEPLOYMENT METHOD SELECTION
################################################################################

echo -e "${BLUE}Choose deployment method:${NC}"
echo ""
echo "  1) Deploy via GitHub (Recommended)"
echo "     - Connects to your GitHub account"
echo "     - Automatic deployments on git push"
echo "     - Easier to manage"
echo ""
echo "  2) Direct deploy via Netlify CLI"
echo "     - Deploys from your local machine"
echo "     - Manual deployments only"
echo "     - Good for testing"
echo ""
read -p "Enter choice (1 or 2): " DEPLOY_METHOD

################################################################################
# METHOD 1: GITHUB DEPLOYMENT
################################################################################

if [ "$DEPLOY_METHOD" = "1" ]; then
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}GITHUB DEPLOYMENT SETUP${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Check if remote is set
    if git remote get-url origin &> /dev/null; then
        REMOTE_URL=$(git remote get-url origin)
        echo -e "${GREEN}✓ Git remote found: $REMOTE_URL${NC}"
    else
        echo "You need to create a GitHub repository first."
        echo ""
        echo "Steps:"
        echo "1. Go to https://github.com/new"
        echo "2. Create a new repository (e.g., 'claude-code-web-ui')"
        echo "3. Copy the repository URL"
        echo ""
        read -p "Enter your GitHub repository URL: " GITHUB_URL

        if [ -n "$GITHUB_URL" ]; then
            git remote add origin "$GITHUB_URL"
            echo -e "${GREEN}✓ Git remote added${NC}"
        else
            echo -e "${RED}✗ No URL provided${NC}"
            exit 1
        fi
    fi

    echo ""
    echo "Committing files..."
    git add .
    git commit -m "Initial commit - Para Group Web UI" || echo "Nothing to commit"

    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main || git push -u origin master || echo "Push failed - you may need to set up authentication"

    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║                  NEXT STEPS FOR GITHUB DEPLOY                  ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "1. Go to: ${GREEN}https://app.netlify.com${NC}"
    echo ""
    echo "2. Click 'Add new site' → 'Import an existing project'"
    echo ""
    echo "3. Connect to GitHub and select your repository"
    echo ""
    echo "4. Build settings (should auto-detect):"
    echo "   - Build command: ${GREEN}npm run build${NC}"
    echo "   - Publish directory: ${GREEN}.next${NC}"
    echo ""
    echo "5. Add environment variables:"
    echo "   (Copy from DEPLOYMENT_CHECKLIST.txt)"
    cat DEPLOYMENT_CHECKLIST.txt
    echo ""
    echo "6. Click 'Deploy site'"
    echo ""
    echo "7. After deployment, update your site name to 'paragroupcli'"
    echo "   (Site settings → Change site name)"
    echo ""
    echo "8. Your site will be live at:"
    echo "   ${GREEN}https://paragroupcli.netlify.app${NC}"
    echo ""

################################################################################
# METHOD 2: DIRECT DEPLOYMENT
################################################################################

elif [ "$DEPLOY_METHOD" = "2" ]; then
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}DIRECT DEPLOYMENT${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""

    echo "Logging in to Netlify..."
    netlify login

    echo ""
    echo "Building application..."
    npm run build

    echo ""
    echo "Deploying to Netlify..."

    # Check if site is already linked
    if [ -f ".netlify/state.json" ]; then
        echo "Site already linked, deploying..."
        netlify deploy --prod
    else
        echo "First-time deployment..."
        netlify deploy --prod --site paragroupcli || netlify deploy --prod
    fi

    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║                    DEPLOYMENT COMPLETE!                        ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANT: Add environment variables in Netlify dashboard${NC}"
    echo ""
    echo "1. Go to your Netlify dashboard"
    echo "2. Select your site"
    echo "3. Go to Site settings → Environment variables"
    echo "4. Add these variables:"
    echo ""
    cat DEPLOYMENT_CHECKLIST.txt
    echo ""
    echo "5. After adding variables, go back to Deploys and click 'Trigger deploy'"
    echo ""

else
    echo -e "${RED}Invalid choice${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Your app should be live at:"
echo -e "  ${GREEN}https://paragroupcli.netlify.app${NC}"
echo ""
echo "Don't forget to:"
echo "  1. Add environment variables in Netlify dashboard"
echo "  2. Verify Google OAuth redirect URI includes:"
echo "     ${GREEN}https://paragroupcli.netlify.app/api/auth/callback${NC}"
echo ""
