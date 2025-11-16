# Para Group Web UI - Netlify Deployment Guide

## ⚠️ CRITICAL: About API Keys and Claude Max

**IMPORTANT CLARIFICATION:**

Your $200/month Claude Max subscription gives you:
- ✅ Access to Claude.ai web interface
- ✅ Access to Claude Code
- ✅ Extended conversation lengths
- ✅ Priority access during high traffic

Your Claude Max subscription does **NOT** give you:
- ❌ Claude API access
- ❌ API keys for third-party applications
- ❌ Programmatic API calls

**THIS WEB APP REQUIRES A CLAUDE API KEY FROM console.anthropic.com**

You will need to create a separate API key from https://console.anthropic.com/settings/keys
This is separate from your Claude Max subscription and has separate costs.

## Prerequisites

1. GitHub account
2. Netlify account (free tier is fine)
3. Google Cloud Console access (for OAuth)
4. Claude API account (for users to get API keys)

## Step 1: Push Code to GitHub

1. Create a new GitHub repository at https://github.com/new

2. Push your code:
```bash
cd /home/user01/claude-test/ClaudePrompt/web-ui-implementation

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Para Group Web UI"

# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

## Step 2: Update Google OAuth Redirect URI

1. Go to: https://console.cloud.google.com/apis/credentials

2. Find your OAuth client: "Para Group Web UI"
   Client ID: 372171601678-0dq7vdvu2j5do6n7f7tmvjohije90b66.apps.googleusercontent.com

3. Click the Edit icon (pencil)

4. Under "Authorized redirect URIs", ADD:
   ```
   https://your-app-name.netlify.app/api/auth/callback
   ```
   (You'll get the actual URL after deploying to Netlify in Step 3)

5. Click SAVE

## Step 3: Deploy to Netlify

1. Go to: https://app.netlify.com

2. Click "Add new site" → "Import an existing project"

3. Choose "GitHub"

4. Authorize Netlify to access your GitHub account

5. Select your repository: "para-group-web-ui" (or whatever you named it)

6. Configure build settings:
   - **Build command:** `npm run build`
   - **Publish directory:** `.next`
   - **Base directory:** (leave empty)

7. Click "Deploy site"

8. Wait for deployment to complete (2-3 minutes)

9. Note your Netlify URL (e.g., `random-name-12345.netlify.app`)

## Step 4: Update Google OAuth with Actual Netlify URL

Now that you have your Netlify URL:

1. Go back to Google Cloud Console: https://console.cloud.google.com/apis/credentials

2. Edit your OAuth client again

3. Update the redirect URI with your ACTUAL Netlify URL:
   ```
   https://random-name-12345.netlify.app/api/auth/callback
   ```
   (Replace with your actual Netlify subdomain)

4. Click SAVE

## Step 5: Configure Environment Variables in Netlify

1. In Netlify Dashboard, go to: **Site settings** → **Environment variables**

2. Click "Add a variable" and add these ONE BY ONE:

   **Variable 1:**
   - Key: `NEXT_PUBLIC_APP_URL`
   - Value: `https://your-actual-netlify-url.netlify.app`
   - Click "Create variable"

   **Variable 2:**
   - Key: `JWT_SECRET`
   - Value: Generate with this command in terminal:
     ```bash
     openssl rand -base64 32
     ```
     Copy the output and paste as value
   - Click "Create variable"

   **Variable 3:**
   - Key: `GOOGLE_CLIENT_ID`
   - Value: `372171601678-0dq7vdvu2j5do6n7f7tmvjohije90b66.apps.googleusercontent.com`
   - Click "Create variable"

   **Variable 4:**
   - Key: `GOOGLE_CLIENT_SECRET`
   - Value: `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`
   - Click "Create variable"

3. **DO NOT** add CLAUDE_API_KEY - users will provide their own!

## Step 6: Redeploy Site

1. In Netlify Dashboard, go to: **Deploys** tab

2. Click "Trigger deploy" → "Deploy site"

3. Wait for deployment to complete (2-3 minutes)

## Step 7: Test the Deployment

1. Open your Netlify URL: `https://your-app-name.netlify.app/dashboard`

2. You should see two login options:
   - Blue button: "Continue with Google"
   - Gray button: "Enter API Key"

3. Click "Continue with Google"

4. Login with your Google account (YVinodReddy@gmail.com)

5. After Google authentication, you'll be prompted to enter YOUR Claude API key

6. Get your Claude API key from: https://console.anthropic.com/settings/keys

7. Enter the API key and submit

8. Start analyzing code! 🎉

## Netlify Free Tier Limits

Good news - Netlify free tier is generous:

- ✅ 100 GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ Automatic HTTPS/SSL
- ✅ Custom domains (if you want)
- ✅ Continuous deployment from GitHub

Your app should stay well within these limits for testing!

## Troubleshooting

### Issue: OAuth redirect error

**Error:** "redirect_uri_mismatch"

**Solution:**
- Check Google OAuth redirect URI matches EXACTLY
- Format: `https://your-actual-url.netlify.app/api/auth/callback`
- NO trailing slash
- Must be HTTPS (not HTTP)

### Issue: Environment variables not working

**Symptoms:** App doesn't load, OAuth fails, errors about missing env vars

**Solution:**
- Verify all 4 variables are set in Netlify Dashboard
- Check for typos in variable names (they're case-sensitive)
- Redeploy after changing environment variables (Netlify → Deploys → Trigger deploy)

### Issue: Build fails

**Symptoms:** Netlify shows "Build failed" with errors

**Solution:**
- Check Netlify build logs (Deploys → click on failed deploy → View build logs)
- Verify package.json has all dependencies
- Make sure Node version is 18 or higher (set in netlify.toml)
- Try building locally first: `npm run build`

### Issue: "Invalid API key" after login

**Symptoms:** Can login with Google but API key doesn't work

**Solution:**
- Verify you're using a valid Claude API key from console.anthropic.com
- Key should start with `sk-ant-`
- Test the key at https://console.anthropic.com to make sure it's active

## Cost Breakdown

### Netlify Costs
- ✅ FREE for testing (100 GB bandwidth, 300 build minutes)
- If you exceed free tier: ~$19/month for Pro plan

### Claude API Costs
- ❌ NOT included in Claude Max subscription
- Separate billing from console.anthropic.com
- Pricing: ~$3 per 1M input tokens, ~$15 per 1M output tokens
- Example: 1000 code analyses ~= ~$5-10 depending on code size

### Google OAuth Costs
- ✅ FREE (no charges from Google)

### Total Monthly Cost Estimate
- Netlify: $0 (free tier) or $19 (if needed)
- Claude API: Variable based on usage
- Google OAuth: $0

## Custom Domain (Optional)

If you want a custom domain instead of `random-name.netlify.app`:

1. In Netlify Dashboard, go to: **Domain management**
2. Click "Add custom domain"
3. Follow the instructions to configure DNS
4. Update Google OAuth redirect URI to use custom domain

## Security Notes

✅ All API keys stored server-side
✅ Sessions use JWT with HTTP-only cookies
✅ 7-day session expiry
✅ Automatic HTTPS/SSL from Netlify
✅ No API keys exposed to frontend
✅ Each user uses their own Claude API key

## Need Help?

If you encounter issues:
1. Check Netlify build logs
2. Verify all environment variables are set
3. Check Google OAuth redirect URI matches exactly
4. Test locally first with `npm run dev`

## Summary - What You Need to Do

1. **Push code to GitHub** ✓
2. **Deploy to Netlify** ✓
3. **Configure environment variables** ✓
4. **Update Google OAuth redirect URI** ✓
5. **Get YOUR Claude API key** (from console.anthropic.com)
6. **Test the deployment** ✓

That's it! The app will be live and ready to use! 🚀
