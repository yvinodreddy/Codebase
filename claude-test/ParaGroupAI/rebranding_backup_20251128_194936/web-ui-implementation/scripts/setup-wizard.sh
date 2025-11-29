#!/bin/bash

################################################################################
# CLAUDE CODE WEB UI - SETUP WIZARD
################################################################################
# This interactive wizard sets up everything you need
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}║          CLAUDE CODE WEB UI - SETUP WIZARD                     ║${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "This wizard will set up everything you need to run the app."
echo "Estimated time: 5 minutes"
echo ""

# Navigate to project directory
BASE_DIR="/home/user01/claude-test/ClaudePrompt/web-ui-implementation"
cd "$BASE_DIR"

################################################################################
# STEP 1: CHECK NODE.JS
################################################################################

echo -e "${YELLOW}Step 1/5: Checking Node.js installation...${NC}"

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js is installed: $NODE_VERSION${NC}"

    # Check version is >= 18
    MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$MAJOR_VERSION" -lt 18 ]; then
        echo -e "${RED}✗ Node.js version must be 18 or higher${NC}"
        echo "  Current version: $NODE_VERSION"
        echo "  Please upgrade Node.js: https://nodejs.org/"
        exit 1
    fi
else
    echo -e "${RED}✗ Node.js is not installed${NC}"
    echo "  Please install Node.js 18 or higher: https://nodejs.org/"
    exit 1
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm is installed: $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm is not installed${NC}"
    exit 1
fi

echo ""

################################################################################
# STEP 2: INSTALL DEPENDENCIES
################################################################################

echo -e "${YELLOW}Step 2/5: Installing dependencies...${NC}"
echo "This may take 2-3 minutes..."
echo ""

if npm install; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

echo ""

################################################################################
# STEP 3: GOOGLE OAUTH SETUP
################################################################################

echo -e "${YELLOW}Step 3/5: Google OAuth Configuration${NC}"
echo ""
echo "You need Google OAuth credentials so users can log in with Gmail."
echo "This is a ONE-TIME setup (takes 5 minutes)."
echo ""
echo -e "${BLUE}Have you already created Google OAuth credentials?${NC}"
echo "  1) Yes, I have them ready"
echo "  2) No, show me how to get them"
echo ""
read -p "Enter choice (1 or 2): " OAUTH_CHOICE

if [ "$OAUTH_CHOICE" = "2" ]; then
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}HOW TO GET GOOGLE OAUTH CREDENTIALS${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "1. Open this URL in your browser:"
    echo "   ${GREEN}https://console.cloud.google.com${NC}"
    echo ""
    echo "2. Create a new project:"
    echo "   - Click 'Select a project' (top left)"
    echo "   - Click 'NEW PROJECT'"
    echo "   - Project name: 'Para Group Web UI'"
    echo "   - Click 'CREATE'"
    echo ""
    echo "3. Enable OAuth:"
    echo "   - Left sidebar: 'APIs & Services' → 'Credentials'"
    echo "   - Click 'CONFIGURE CONSENT SCREEN'"
    echo "   - Choose 'External' → Click 'CREATE'"
    echo "   - Fill in app name, your email"
    echo "   - Click 'SAVE AND CONTINUE' (3 times)"
    echo ""
    echo "4. Create OAuth credentials:"
    echo "   - Click 'CREATE CREDENTIALS' → 'OAuth 2.0 Client ID'"
    echo "   - Application type: 'Web application'"
    echo "   - Name: 'Para Group Web UI'"
    echo "   - Authorized redirect URIs:"
    echo "     * Add: ${GREEN}http://localhost:3000/api/auth/callback${NC}"
    echo "     * Add: ${GREEN}https://paragroupcli.netlify.app/api/auth/callback${NC}"
    echo "   - Click 'CREATE'"
    echo ""
    echo "5. Copy the Client ID and Client Secret"
    echo ""
    echo -e "${YELLOW}Press Enter when you have your credentials ready...${NC}"
    read
    echo ""
fi

echo "Enter your Google OAuth credentials:"
echo ""
read -p "Client ID: " GOOGLE_CLIENT_ID
echo ""
read -p "Client Secret: " GOOGLE_CLIENT_SECRET
echo ""

if [ -z "$GOOGLE_CLIENT_ID" ] || [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo -e "${RED}✗ Client ID and Secret are required${NC}"
    exit 1
fi

echo -e "${GREEN}✓ OAuth credentials received${NC}"
echo ""

################################################################################
# STEP 4: GENERATE JWT SECRET
################################################################################

echo -e "${YELLOW}Step 4/5: Generating security keys...${NC}"

JWT_SECRET=$(openssl rand -base64 32)
echo -e "${GREEN}✓ JWT secret generated${NC}"

################################################################################
# STEP 5: CREATE CONFIGURATION FILES
################################################################################

echo -e "${YELLOW}Step 5/5: Creating configuration files...${NC}"

# Create .env.local for local development
cat > .env.local << EOF
# Application URL (for local development)
NEXT_PUBLIC_APP_URL=http://localhost:3000

# JWT Secret (auto-generated)
JWT_SECRET=$JWT_SECRET

# Google OAuth Credentials
GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET

# Note: Users will provide their Claude API keys through the UI
# You don't need to set ANTHROPIC_API_KEY here
EOF

echo -e "${GREEN}✓ .env.local created${NC}"

# Create .env.production for production deployment
cat > .env.production << EOF
# Application URL (for production on Netlify)
NEXT_PUBLIC_APP_URL=https://paragroupcli.netlify.app

# JWT Secret (same as local - will be set in Netlify dashboard)
JWT_SECRET=$JWT_SECRET

# Google OAuth Credentials (will be set in Netlify dashboard)
GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET
EOF

echo -e "${GREEN}✓ .env.production created${NC}"

# Create deployment checklist
cat > DEPLOYMENT_CHECKLIST.txt << EOF
NETLIFY ENVIRONMENT VARIABLES
==============================

When deploying to Netlify, add these environment variables in the Netlify dashboard:

1. NEXT_PUBLIC_APP_URL=https://paragroupcli.netlify.app
2. JWT_SECRET=$JWT_SECRET
3. GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID
4. GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET

HOW TO ADD:
1. Go to your Netlify dashboard
2. Select your site
3. Go to Site settings → Environment variables
4. Click "Add a variable" for each one above
5. Copy-paste the values exactly as shown

GOOGLE OAUTH REDIRECT URI:
Make sure you added this URI in Google Cloud Console:
https://paragroupcli.netlify.app/api/auth/callback
EOF

echo -e "${GREEN}✓ Deployment checklist created${NC}"

echo ""

################################################################################
# VALIDATION
################################################################################

echo -e "${YELLOW}Validating configuration...${NC}"

# Check if files exist
if [ -f ".env.local" ]; then
    echo -e "${GREEN}✓ .env.local exists${NC}"
else
    echo -e "${RED}✗ .env.local not found${NC}"
    exit 1
fi

if [ -f "package.json" ]; then
    echo -e "${GREEN}✓ package.json exists${NC}"
else
    echo -e "${RED}✗ package.json not found${NC}"
    exit 1
fi

if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓ node_modules exists${NC}"
else
    echo -e "${RED}✗ node_modules not found${NC}"
    exit 1
fi

echo ""

################################################################################
# SUCCESS
################################################################################

echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                                ║${NC}"
echo -e "${GREEN}║                    ✓ SETUP COMPLETE!                           ║${NC}"
echo -e "${GREEN}║                                                                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Your Para Group Web UI is ready!"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Test locally:"
echo "   ${GREEN}./scripts/run-local.sh${NC}"
echo "   Then open: http://localhost:3000"
echo ""
echo "2. Deploy to production:"
echo "   ${GREEN}./scripts/deploy-to-netlify.sh${NC}"
echo ""
echo -e "${YELLOW}Important Files Created:${NC}"
echo "  - .env.local (local development config)"
echo "  - .env.production (production config)"
echo "  - DEPLOYMENT_CHECKLIST.txt (Netlify setup instructions)"
echo ""
echo -e "${YELLOW}Troubleshooting:${NC}"
echo "  If something doesn't work, run:"
echo "  ${GREEN}./scripts/diagnose.sh${NC}"
echo ""
