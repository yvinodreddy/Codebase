import { NextApiRequest, NextApiResponse } from 'next';
import { getOAuthUrl } from '@/lib/auth';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });
  const authUrl = getOAuthUrl();
  res.redirect(authUrl);
}
