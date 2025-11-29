import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie, setCookie } from 'cookies-next';
import { verifySession, verifyClaudeApiKey, createSession } from '@/lib/auth';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const token = getCookie('session', { req, res });
    if (!token || typeof token !== 'string') return res.status(401).json({ error: 'Not authenticated' });

    const session = await verifySession(token);
    if (!session) return res.status(401).json({ error: 'Invalid session' });

    const { apiKey } = req.body;
    if (!apiKey) return res.status(400).json({ error: 'API key required' });

    const isValid = await verifyClaudeApiKey(apiKey);
    if (!isValid) return res.status(400).json({ error: 'Invalid Claude API key' });

    const updatedUser = { ...session.user, claudeApiKey: apiKey, verified: true };
    const newToken = await createSession(updatedUser);

    setCookie('session', newToken, {
      req,
      res,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 7 * 24 * 60 * 60,
    });

    res.status(200).json({ success: true, user: updatedUser });
  } catch (error) {
    console.error('Validation error:', error);
    res.status(500).json({ error: 'Validation failed' });
  }
}
