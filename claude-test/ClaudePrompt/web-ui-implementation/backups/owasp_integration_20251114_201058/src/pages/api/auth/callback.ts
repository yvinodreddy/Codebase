import { NextApiRequest, NextApiResponse } from 'next';
import { OAUTH_CONFIG, createSession, User } from '@/lib/auth';
import { setCookie } from 'cookies-next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { code, error } = req.query;
  if (error) return res.redirect('/?error=oauth_failed');
  if (!code || typeof code !== 'string') return res.redirect('/?error=no_code');

  try {
    const tokenResponse = await fetch(OAUTH_CONFIG.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        code,
        client_id: OAUTH_CONFIG.clientId,
        client_secret: OAUTH_CONFIG.clientSecret,
        redirect_uri: OAUTH_CONFIG.redirectUri,
        grant_type: 'authorization_code',
      }),
    });

    if (!tokenResponse.ok) throw new Error('Token exchange failed');
    const tokens = await tokenResponse.json();

    const userResponse = await fetch(OAUTH_CONFIG.userInfoUrl, {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    });

    if (!userResponse.ok) throw new Error('Failed to fetch user info');
    const userInfo = await userResponse.json();

    const user: User = {
      id: userInfo.id,
      email: userInfo.email,
      name: userInfo.name,
      picture: userInfo.picture,
      claudeApiKey: '', // Not needed - using ULTRATHINK framework with Claude Max subscription
      verified: true, // No API key validation needed - Claude Max includes Claude Code access
    };

    const sessionToken = await createSession(user);
    setCookie('session', sessionToken, {
      req,
      res,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 7 * 24 * 60 * 60,
    });

    res.redirect('/dashboard'); // Go directly to dashboard - no API key setup needed
  } catch (error) {
    console.error('OAuth callback error:', error);
    res.redirect('/?error=authentication_failed');
  }
}
