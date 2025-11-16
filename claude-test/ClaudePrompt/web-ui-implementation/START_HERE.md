# ⚡ START HERE - CLAUDE CODE WEB UI

**Get your app running in 3 commands!**

================================================================================
🎯 WHAT IS THIS?
================================================================================

This is a **web version of Para Group** that works exactly like the Para Group on your computer, but:
- ✅ Runs in a web browser
- ✅ Can be accessed from anywhere (after you deploy it)
- ✅ Users log in with Gmail (just like you logged into Para Group)
- ✅ Uses your $200/month Claude plan (no extra charges)

================================================================================
🚀 GETTING STARTED (3 COMMANDS)
================================================================================

```bash
# 1. Run the setup wizard (asks you questions, configures everything)
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation
./scripts/setup-wizard.sh

# 2. Test on your computer (opens http://localhost:3000)
./scripts/run-local.sh

# 3. Deploy to the internet (makes it live at paragroupcli.netlify.app)
./scripts/deploy-to-netlify.sh
```

**That's it!** The scripts do everything for you.

================================================================================
❓ CONFUSED ABOUT AUTHENTICATION?
================================================================================

## How Para Group Works (What You're Used To)

**On Your Computer**:
```
You → Para Group on your PC → Already logged in → Just works
```

You logged in ONCE and never think about it again.

## How the Web App Works (Same Idea!)

**On the Server (paragroupcli.netlify.app)**:
```
User → Clicks "Sign in with Google" → Logs in once → Just works
```

**It's the SAME experience!** Users log in once and then it just works.

================================================================================
📍 TWO PLACES: LOCAL vs SERVER
================================================================================

## LOCAL (Your Computer Only)

**What**: Runs on YOUR computer
**URL**: http://localhost:3000
**Who can access**: Only YOU
**Purpose**: Testing before going live

**Run it**:
```bash
./scripts/run-local.sh
```

**Use it when**:
- You want to test if it works
- You're making changes
- You're debugging

---

## SERVER (Internet - Netlify)

**What**: Runs on Netlify's servers (internet)
**URL**: https://paragroupcli.netlify.app
**Who can access**: ANYONE (after they log in with Google)
**Purpose**: Real use

**Deploy it**:
```bash
./scripts/deploy-to-netlify.sh
```

**Use it when**:
- You want to access from any computer
- You want others to use it
- You want to use it on your phone

================================================================================
🔐 ABOUT GOOGLE OAUTH (Why We Need It)
================================================================================

**Question**: "Why do I need to set up Google OAuth?"

**Answer**: So users can log in with Gmail (just like you logged into Para Group).

**How It Works**:

1. **You (One Time Only)**:
   - Set up Google OAuth (5 minutes, the wizard helps you)
   - This tells Google: "My app is allowed to verify Gmail accounts"

2. **Users (Every Time They Use It)**:
   - Click "Sign in with Google"
   - Google asks: "Allow access?"
   - User clicks "Yes"
   - ✅ They're logged in!

**Just Like**:
- Logging into websites with "Sign in with Google"
- How you logged into Para Group the first time

================================================================================
📋 WHAT THE SETUP WIZARD DOES
================================================================================

When you run `./scripts/setup-wizard.sh`, it:

1. ✅ Checks if Node.js is installed
2. ✅ Installs all dependencies (npm packages)
3. ✅ Asks you for Google OAuth credentials
4. ✅ Creates configuration files (.env.local)
5. ✅ Validates everything works
6. ✅ Tells you exactly what to do next

**It's Interactive!** It asks questions and guides you through everything.

================================================================================
🎯 STEP-BY-STEP VISUAL GUIDE
================================================================================

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: RUN SETUP WIZARD                                    │
│ Command: ./scripts/setup-wizard.sh                          │
│                                                              │
│ What it asks you:                                           │
│ 1. "Do you have Google OAuth credentials?"                  │
│    → If NO: Shows you EXACTLY how to get them              │
│    → If YES: Asks you to paste them                        │
│                                                              │
│ 2. Creates .env.local file automatically                    │
│ 3. ✓ Setup complete!                                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: TEST LOCALLY                                        │
│ Command: ./scripts/run-local.sh                             │
│                                                              │
│ What happens:                                               │
│ 1. Starts server on http://localhost:3000                  │
│ 2. You open it in browser                                  │
│ 3. Click "Sign in with Google"                             │
│ 4. Enter your Claude API key                               │
│ 5. ✓ You can now analyze folders!                          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: DEPLOY TO PRODUCTION                                │
│ Command: ./scripts/deploy-to-netlify.sh                     │
│                                                              │
│ What happens:                                               │
│ 1. Script asks: "Deploy via GitHub or direct?"             │
│ 2. You choose (GitHub is recommended)                      │
│ 3. Script builds and deploys                               │
│ 4. ✓ Live at paragroupcli.netlify.app!                     │
└─────────────────────────────────────────────────────────────┘
```

================================================================================
🆘 IF SOMETHING DOESN'T WORK
================================================================================

**Run the diagnostic tool**:
```bash
./scripts/diagnose.sh
```

It checks EVERYTHING and tells you exactly what's wrong.

**Common Issues**:

1. **"OAuth redirect error"**
   - Solution: Make sure you added BOTH URLs in Google Console:
     - `http://localhost:3000/api/auth/callback`
     - `https://paragroupcli.netlify.app/api/auth/callback`

2. **"Port 3000 already in use"**
   - Solution: The script will ask if you want to kill it, say "yes"

3. **"Module not found"**
   - Solution: Run `npm install`

4. **"Can't connect to localhost"**
   - Solution: Run `./scripts/run-local.sh` again

================================================================================
📚 MORE HELP
================================================================================

**Detailed Guides**:
- `SIMPLE_SETUP.md` - Comprehensive setup guide
- `QUICK_START.md` - 5-minute quick start
- `MASTER_IMPLEMENTATION_PLAN.md` - Complete technical details

**Scripts**:
- `setup-wizard.sh` - Interactive setup
- `run-local.sh` - Start local server
- `deploy-to-netlify.sh` - Deploy to production
- `diagnose.sh` - Fix problems

**Just Read SIMPLE_SETUP.md** if you want to understand everything in detail.

================================================================================
✅ QUICK CHECKLIST
================================================================================

Before deploying to production, make sure:

**Google OAuth Setup**:
- [ ] Created project in Google Cloud Console
- [ ] Created OAuth credentials
- [ ] Added BOTH redirect URIs (local + production)
- [ ] Copied Client ID and Secret

**Local Testing**:
- [ ] Ran setup wizard
- [ ] Local server starts without errors
- [ ] Can log in with Google
- [ ] Can enter Claude API key
- [ ] Can analyze a test folder

**Production Deployment**:
- [ ] Deployed to Netlify
- [ ] Added environment variables in Netlify dashboard
- [ ] Updated Google OAuth redirect URI for production
- [ ] Tested login on paragroupcli.netlify.app

================================================================================
🎉 READY TO START!
================================================================================

**Just run these 3 commands**:

```bash
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation

./scripts/setup-wizard.sh    # Configure everything
./scripts/run-local.sh        # Test locally
./scripts/deploy-to-netlify.sh  # Deploy to internet
```

**That's it!** The scripts guide you through everything.

**Time Required**:
- Setup wizard: 5 minutes
- Local testing: 2 minutes
- Deployment: 3 minutes
- **Total: 10 minutes**

**GO! 🚀**
