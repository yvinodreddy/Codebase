# 🚀 SIMPLE SETUP GUIDE - CLAUDE CODE WEB UI

**Goal**: Get your web app running exactly like Para Group works for you locally.

================================================================================
❓ CONFUSED ABOUT AUTHENTICATION? READ THIS FIRST
================================================================================

## How Para Group Works (What You're Used To)

When you use Para Group on your local machine:
1. You logged in ONCE with your Gmail account
2. Para Group saved your login credentials
3. Now you just type commands and it works
4. **You never think about authentication again**

## How the Web App Will Work (Same Experience!)

When you deploy to paragroupcli.netlify.app:
1. Users visit the website
2. They click "Sign in with Google" (using their Gmail)
3. They enter their Claude API key (from Anthropic) **ONCE**
4. **Then it works just like Para Group - they're logged in!**
5. Session lasts 7 days, then they log in again

## Why Do We Need Google OAuth Setup?

**Short Answer**: So users can log in with Gmail (just like you did with Para Group).

**Technical Reason**:
- Para Group on your machine: Uses your saved credentials
- Para Group on the web: Needs Google to verify "yes, this is really user@gmail.com"
- Google OAuth is how websites verify Gmail accounts securely

**One-Time Setup**:
- You set up Google OAuth ONCE (5 minutes)
- After that, users just click "Sign in with Google" and it works forever
- It's like when YOU set up Para Group the first time

================================================================================
🎯 TWO PATHS: LOCAL TESTING vs PRODUCTION SERVER
================================================================================

## Path 1: TEST LOCALLY (Your Computer)

**What This Means**:
- Runs on YOUR computer only
- URL: http://localhost:3000
- Only YOU can access it
- For testing before deploying to server

**When to Use**:
- Testing if everything works
- Making changes to the code
- Debugging issues

## Path 2: PRODUCTION SERVER (Netlify)

**What This Means**:
- Runs on Netlify's servers (internet)
- URL: https://paragroupcli.netlify.app
- ANYONE can access it (after logging in with Google)
- For real use by you or your team

**When to Use**:
- After testing locally works
- When you want to use it from any computer
- When you want others to use it

================================================================================
🔧 AUTOMATED SETUP - JUST RUN THESE COMMANDS
================================================================================

I've created automated scripts that do everything for you!

### Step 1: Run the Setup Wizard (2 minutes)

```bash
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation
chmod +x scripts/setup-wizard.sh
./scripts/setup-wizard.sh
```

**What This Does**:
1. ✅ Checks if Node.js is installed
2. ✅ Installs all dependencies
3. ✅ Asks you for Google OAuth credentials
4. ✅ Creates .env.local file automatically
5. ✅ Validates everything is correct
6. ✅ Tells you exactly what to do next

**It Will Ask You**:
- "Do you have Google OAuth credentials?"
  - If NO: It shows you EXACTLY how to get them (with links)
  - If YES: It asks you to paste them

### Step 2: Test Locally (1 minute)

```bash
./scripts/run-local.sh
```

**What This Does**:
1. ✅ Starts the web server on your computer
2. ✅ Opens http://localhost:3000 in your browser
3. ✅ You can test the login flow
4. ✅ Press Ctrl+C to stop when done

### Step 3: Deploy to Production (2 minutes)

```bash
./scripts/deploy-to-netlify.sh
```

**What This Does**:
1. ✅ Checks if everything is ready
2. ✅ Builds the production version
3. ✅ Deploys to Netlify
4. ✅ Gives you the URL: paragroupcli.netlify.app

================================================================================
📋 WHAT YOU NEED TO PROVIDE (Only Once)
================================================================================

### Google OAuth Credentials

**Why**: So users can log in with Gmail (like you did with Para Group)

**How to Get** (5 minutes, one-time setup):

1. **Open Google Cloud Console**:
   ```
   https://console.cloud.google.com
   ```

2. **Create a New Project**:
   - Click "Select a project" (top left)
   - Click "NEW PROJECT"
   - Project name: "Para Group Web UI"
   - Click "CREATE"

3. **Enable OAuth**:
   - Wait for project to be created
   - In the left sidebar: "APIs & Services" → "Credentials"
   - Click "CONFIGURE CONSENT SCREEN"
   - Choose "External" → Click "CREATE"
   - Fill in:
     - App name: "Para Group Web UI"
     - User support email: YOUR EMAIL
     - Developer email: YOUR EMAIL
   - Click "SAVE AND CONTINUE" (3 times)
   - Click "BACK TO DASHBOARD"

4. **Create OAuth Credentials**:
   - Click "Credentials" in the left sidebar
   - Click "CREATE CREDENTIALS" → "OAuth 2.0 Client ID"
   - Application type: "Web application"
   - Name: "Para Group Web UI"
   - Authorized redirect URIs → Click "ADD URI":
     - Add: `http://localhost:3000/api/auth/callback`
     - Click "ADD URI" again
     - Add: `https://paragroupcli.netlify.app/api/auth/callback`
   - Click "CREATE"

5. **Copy Credentials**:
   - A popup shows "Client ID" and "Client Secret"
   - **COPY THESE** - you'll need them for the setup wizard
   - You can also download them as JSON

**That's It!** You never have to do this again.

### Your Claude API Key

**Why**: So the app can call Claude API (using YOUR $200/month plan)

**How to Get**:
1. Go to: https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-`)

**Note**: You'll enter this when you FIRST LOG IN to the web app, not during setup.

================================================================================
🏃 QUICK START - COPY AND PASTE THESE COMMANDS
================================================================================

### Complete Local Setup (5 Minutes)

```bash
# 1. Go to project directory
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation

# 2. Run setup wizard (will ask for Google OAuth credentials)
chmod +x scripts/setup-wizard.sh
./scripts/setup-wizard.sh

# 3. Start local server
chmod +x scripts/run-local.sh
./scripts/run-local.sh

# 4. Open browser to http://localhost:3000
```

### Deploy to Production (After Local Testing Works)

```bash
# 1. Make sure you're in the project directory
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation

# 2. Run deployment script
chmod +x scripts/deploy-to-netlify.sh
./scripts/deploy-to-netlify.sh

# 3. Follow the prompts (connects to Netlify)

# 4. Done! Your app is live at paragroupcli.netlify.app
```

================================================================================
🔍 WHAT HAPPENS BEHIND THE SCENES
================================================================================

### When You Run Local Server

```
Your Computer:
├── Node.js server starts (port 3000)
├── Reads .env.local for Google OAuth credentials
├── Waits for you to open http://localhost:3000
└── When you click "Sign in with Google":
    ├── Redirects to Google
    ├── Google asks "Allow access?"
    ├── You click "Allow"
    ├── Google sends you back to localhost:3000
    ├── App asks for Claude API key
    ├── You enter your key (from Anthropic)
    └── ✅ You're logged in! Now you can analyze folders
```

### When You Deploy to Netlify

```
Netlify Servers:
├── You run deploy script
├── Script builds production version
├── Uploads to Netlify servers
├── Netlify gives you URL: paragroupcli.netlify.app
└── Users can now access it from anywhere:
    ├── They visit paragroupcli.netlify.app
    ├── Click "Sign in with Google"
    ├── Enter their Claude API key
    └── ✅ They're logged in! Can analyze their folders
```

================================================================================
❓ FREQUENTLY ASKED QUESTIONS
================================================================================

### Q: Why can't it just use my Para Group login?

**A**: Para Group on your machine saves credentials locally. Web apps can't access your local files for security reasons. So we use Google OAuth (the standard way websites verify Gmail accounts).

### Q: Do I need to set up Google OAuth for BOTH local and production?

**A**: You set it up ONCE. The same credentials work for both:
- Local: Uses `http://localhost:3000/api/auth/callback`
- Production: Uses `https://paragroupcli.netlify.app/api/auth/callback`

You added BOTH URLs when creating OAuth credentials, so it works in both places!

### Q: Will I be charged for Google OAuth?

**A**: No! Google OAuth is FREE for this use case.

### Q: Will I be charged extra for Claude API calls?

**A**: No! The web app uses YOUR existing Claude API key (from your $200/month plan). Same as Para Group uses now.

### Q: Can I test without setting up Google OAuth?

**A**: No, authentication is required. But setup takes only 5 minutes and you never do it again.

### Q: What if I already deployed but forgot to update Google OAuth redirect URI?

**A**: Go back to Google Cloud Console, edit your OAuth credentials, add `https://paragroupcli.netlify.app/api/auth/callback`, save. That's it!

### Q: How do I know if it's working?

**A**: The setup wizard validates everything. If it says "✅ All checks passed", you're good to go!

### Q: What if something breaks?

**A**: Run the diagnostic script:
```bash
./scripts/diagnose.sh
```
It checks everything and tells you exactly what's wrong.

================================================================================
🎯 TROUBLESHOOTING - COMMON ISSUES
================================================================================

### "OAuth redirect URI mismatch"

**Problem**: Google OAuth redirect URI doesn't match.

**Solution**:
1. Go to Google Cloud Console
2. Edit your OAuth credentials
3. Make sure you have BOTH:
   - `http://localhost:3000/api/auth/callback` (for local)
   - `https://paragroupcli.netlify.app/api/auth/callback` (for production)
4. Save
5. Try again

### "Cannot connect to localhost:3000"

**Problem**: Server didn't start or crashed.

**Solution**:
```bash
# Check if Node.js is running
ps aux | grep node

# Kill any stuck processes
pkill -9 node

# Try starting again
./scripts/run-local.sh
```

### "Invalid Claude API key"

**Problem**: API key is wrong or expired.

**Solution**:
1. Go to https://console.anthropic.com/settings/keys
2. Create a new key
3. Try logging in again with the new key

### "Module not found" or build errors

**Problem**: Dependencies not installed correctly.

**Solution**:
```bash
# Clean everything
rm -rf node_modules
rm -rf .next

# Re-install
npm install

# Try again
npm run dev
```

================================================================================
✅ SUCCESS CHECKLIST
================================================================================

After running the setup wizard, verify:

**Local Testing**:
- [ ] Server starts without errors
- [ ] http://localhost:3000 opens in browser
- [ ] "Sign in with Google" button appears
- [ ] Clicking it redirects to Google
- [ ] After authorizing, returns to localhost
- [ ] Can enter Claude API key
- [ ] Dashboard loads after API key verification

**Production Deployment**:
- [ ] Deploy script completes without errors
- [ ] Can access paragroupcli.netlify.app
- [ ] "Sign in with Google" works
- [ ] Can log in and verify API key
- [ ] Can analyze a test folder
- [ ] Results display correctly
- [ ] Can download output files

================================================================================
📞 NEXT STEPS
================================================================================

1. **Read This Guide** (you just did! ✅)

2. **Run Setup Wizard**:
   ```bash
   cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation
   ./scripts/setup-wizard.sh
   ```

3. **Test Locally**:
   ```bash
   ./scripts/run-local.sh
   ```

4. **Deploy to Production**:
   ```bash
   ./scripts/deploy-to-netlify.sh
   ```

5. **Use Your App**!
   - Visit paragroupcli.netlify.app
   - Sign in with Google
   - Enter Claude API key
   - Start analyzing code!

================================================================================
🎉 YOU'RE READY!
================================================================================

The setup wizard will guide you through everything.

**Estimated Time**:
- Setup wizard: 5 minutes
- Local testing: 2 minutes
- Production deployment: 3 minutes
- **Total: 10 minutes to live production app!**

Just run:
```bash
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation
./scripts/setup-wizard.sh
```

**The wizard does everything else for you!** 🚀
