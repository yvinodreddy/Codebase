# Google OAuth Setup Guide

## Two Authentication Methods Available

Your Para Group Web UI now supports **TWO** ways to authenticate:

### Option 1: Google OAuth (Recommended)
- ✅ Quick one-click login
- ✅ Uses your Claude Max subscription
- ✅ No API keys to manage
- ✅ Best for most users

### Option 2: Manual API Key
- ✅ Full control over API usage
- ✅ Works without Google account
- ✅ For advanced users

---

## Setting Up Google OAuth

### Step 1: Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com)

2. Create a new project:
   - Click "Select a project" (top left)
   - Click "NEW PROJECT"
   - Project name: `Para Group Web UI`
   - Click "CREATE"

3. Enable OAuth Consent Screen:
   - Left sidebar: `APIs & Services` → `Credentials`
   - Click "CONFIGURE CONSENT SCREEN"
   - Choose "External" → Click "CREATE"
   - Fill in:
     - App name: `Para Group Web UI`
     - User support email: Your email
     - Developer contact: Your email
   - Click "SAVE AND CONTINUE" (3 times)

4. Create OAuth 2.0 Credentials:
   - Click "CREATE CREDENTIALS" → "OAuth 2.0 Client ID"
   - Application type: `Web application`
   - Name: `Para Group Web UI`
   - Authorized redirect URIs:
     - **Local**: `http://localhost:3001/api/auth/callback`
     - **Production**: `https://your-domain.com/api/auth/callback`
   - Click "CREATE"

5. Copy your credentials:
   - Client ID: `xxx.apps.googleusercontent.com`
   - Client Secret: `GOCSPX-xxx`

### Step 2: Configure Environment Variables

Edit `.env.local`:

```bash
# Google OAuth Credentials
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_secret_here

# Claude API Key (for OAuth users)
CLAUDE_API_KEY=sk-ant-your-api-key-here
```

### Step 3: Get Claude API Key

1. Go to [Claude Console](https://console.anthropic.com)
2. Sign in
3. Go to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)
6. Add it to `.env.local` as `CLAUDE_API_KEY`

### Step 4: Restart Server

```bash
# Stop current server (Ctrl+C)
# Start again
npm run dev
```

---

## How It Works

### Google OAuth Flow:
1. User clicks "Continue with Google"
2. Redirected to Google login
3. User authorizes the app
4. Google redirects back with auth code
5. Server exchanges code for user info
6. Server creates session with server API key
7. User is logged in and ready to analyze code!

### API Key Flow:
1. User clicks "Enter API Key"
2. User enters their Claude API key
3. Server validates the key
4. Server creates session with user's key
5. User is logged in and ready to analyze code!

---

## Testing

### Test Google OAuth:
1. Open: `http://localhost:3001/dashboard`
2. Click "Continue with Google"
3. Should redirect to Google login
4. After login, should return to dashboard

### Test API Key:
1. Open: `http://localhost:3001/dashboard`
2. Click "Enter API Key"
3. Enter a valid Claude API key
4. Should redirect to analysis form

---

## Production Deployment

### Environment Variables for Netlify:

```bash
NEXT_PUBLIC_APP_URL=https://your-domain.com
JWT_SECRET=<generate-random-string>
GOOGLE_CLIENT_ID=<your-client-id>
GOOGLE_CLIENT_SECRET=<your-secret>
CLAUDE_API_KEY=<your-api-key>
```

### Update Google OAuth Redirect URI:
- Add production URL: `https://your-domain.com/api/auth/callback`

---

## Troubleshooting

### "OAuth callback error"
- Check that redirect URI matches exactly
- Verify Google OAuth credentials are correct
- Check that consent screen is published

### "Invalid API key"
- Verify Claude API key is correct
- Check that key starts with `sk-ant-`
- Test key at console.anthropic.com

### "Not authenticated"
- Clear browser cookies
- Try logging in again
- Check server logs for errors

---

## Security Notes

- ✅ All API keys stored server-side
- ✅ Sessions use JWT with HTTP-only cookies
- ✅ 7-day session expiry
- ✅ Secure flag in production
- ✅ No API keys exposed to frontend

---

## User Experience

Users will see a beautiful two-column layout:

**Left Column (Blue)**: Google OAuth
- Shows Google logo
- "Continue with Google" button
- Benefits listed

**Right Column (Gray)**: API Key
- Shows key icon
- "Enter API Key" button
- Benefits listed

**Help Section Below**: Explains which to choose

This gives users the flexibility to choose their preferred method!
