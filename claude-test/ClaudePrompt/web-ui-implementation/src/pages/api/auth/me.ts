import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';

// ✅ OWASP Security Integration (Added 2025-11-15)
import { securityLogger, SecurityEvent } from '@/lib/security/logging';


export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const token = getCookie('session', { req, res });

    if (!token || typeof token !== 'string') {
      return res.status(200).json({ authenticated: false });
    }

    const session = await verifySession(token);

    if (!session || !session.user) {
      return res.status(200).json({ authenticated: false });
    }

    // Return user info without sensitive data
    return res.status(200).json({
      authenticated: true,
      user: {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name,
        picture: session.user.picture,
        verified: session.user.verified,
      },
    });
  } catch (error) {
    return res.status(200).json({ authenticated: false });
  }
}
