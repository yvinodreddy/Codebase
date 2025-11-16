# 🚀 QUICK START GUIDE

Get Para Group Web UI running in **5 minutes**.

## Prerequisites

- Node.js 20+
- npm 10+
- Google Cloud account (for OAuth)
- Claude API key (from Anthropic)

## Step 1: Install Dependencies (1 minute)

```bash
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation
npm install
```

## Step 2: Generate All Missing Files (1 minute)

We've created a **code generator** that creates all remaining files automatically:

```bash
chmod +x scripts/generate-all-files.sh
./scripts/generate-all-files.sh
```

This will create:
- All TypeScript source files (auth.ts, claude-client.ts, etc.)
- All React components
- All API routes
- All tests
- All configuration files

**Total**: 60+ files generated automatically

## Step 3: Configure Environment (1 minute)

### Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project: "Para Group Web UI"
3. Go to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth 2.0 Client ID"
5. Application type: **Web application**
6. Authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback`
   - `https://paragroupcli.netlify.app/api/auth/callback`
7. Copy Client ID and Client Secret

### Create .env.local

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```bash
NEXT_PUBLIC_APP_URL=http://localhost:3000
JWT_SECRET=$(openssl rand -base64 32)
GOOGLE_CLIENT_ID=paste-your-client-id-here
GOOGLE_CLIENT_SECRET=paste-your-secret-here
```

## Step 4: Test Locally (1 minute)

```bash
npm run dev
```

Visit: http://localhost:3000

Test:
1. Click "Sign in with Google"
2. Authorize
3. Enter your Claude API key
4. Try analyzing a folder

## Step 5: Deploy to Netlify (1 minute)

### Option A: GitHub Integration (Recommended)

1. Push code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

2. Go to [Netlify](https://app.netlify.com)
3. Click "Add new site" > "Import an existing project"
4. Connect GitHub
5. Select your repository
6. Build settings (auto-detected):
   - Build command: `npm run build`
   - Publish directory: `.next`
7. Add environment variables (same as .env.local)
8. Click "Deploy site"

### Option B: Direct Deploy

```bash
npm install -g netlify-cli
netlify login
netlify init --manual
netlify deploy --prod
```

## Done! 🎉

Your app is now live at: https://YOUR_SITE.netlify.app

## What to Do Next

1. **Update OAuth Redirect**:
   - Go back to Google Console
   - Update redirect URI to your Netlify URL
   - `https://YOUR_SITE.netlify.app/api/auth/callback`

2. **Test Production**:
   - Visit your Netlify URL
   - Test login
   - Test folder analysis
   - Test file downloads

3. **Monitor**:
   - Check Netlify dashboard for errors
   - View analytics
   - Monitor usage

## Troubleshooting

**"OAuth redirect error"**:
- Verify redirect URI matches exactly in Google Console
- Include protocol (http:// or https://)

**"Module not found"**:
- Run `./scripts/generate-all-files.sh` again
- Clear `.next` folder: `rm -rf .next`
- Rebuild: `npm run build`

**"Invalid API key"**:
- Get key from [Anthropic Console](https://console.anthropic.com)
- Should start with `sk-ant-`
- Verify key has credits

## Need Help?

Read the comprehensive docs:
- `MASTER_IMPLEMENTATION_PLAN.md` - Complete details
- `IMPLEMENTATION_SUMMARY.md` - Overview
- `SETUP.md` - Detailed setup
- `USER_GUIDE.md` - User documentation

## Code Generator Details

The `generate-all-files.sh` script creates:

**Source Files** (30+ files):
- Authentication library
- Claude API client
- All API routes
- All React components
- Type definitions

**Tests** (15+ files):
- Unit tests
- Integration tests
- E2E tests

**Configuration** (10+ files):
- Tailwind config
- PostCSS config
- Jest config
- Playwright config

**Scripts** (5 files):
- Build script
- Test script
- Deploy script
- Development script

This ensures **zero manual file creation** - everything is automated.

## Time Breakdown

- Install dependencies: 1 minute
- Generate files: 1 minute
- Configure environment: 1 minute
- Test locally: 1 minute
- Deploy: 1 minute

**Total: 5 minutes to production** 🚀
