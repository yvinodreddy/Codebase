import { NextApiRequest, NextApiResponse } from 'next';
import { deleteCookie } from 'cookies-next';

// ✅ OWASP Security Integration (Added 2025-11-15)
import { securityLogger, SecurityEvent } from '@/lib/security/logging';


export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    // Delete the session cookie
    deleteCookie('session', { req, res });

    res.status(200).json({ success: true, message: 'Logged out successfully' });
  } catch (error) {
    console.error('Logout error:', error);
    res.status(500).json({ error: 'Logout failed' });
  }
}
