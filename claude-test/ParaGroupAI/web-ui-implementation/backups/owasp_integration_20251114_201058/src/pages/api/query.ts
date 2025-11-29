import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';
import { UltrathinkClient } from '@/lib/ultrathink-client';
import * as path from 'path';
import * as fs from 'fs/promises';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const token = getCookie('session', { req, res });
    if (!token || typeof token !== 'string') return res.status(401).json({ error: 'Not authenticated' });

    const session = await verifySession(token);
    if (!session) return res.status(401).json({ error: 'Unauthorized' });

    const { folderPath, query } = req.body;
    if (!query) return res.status(400).json({ error: 'Query is required' });

    // Validate folder path only if provided
    if (folderPath) {
      try {
        const stats = await fs.stat(folderPath);
        if (!stats.isDirectory()) return res.status(400).json({ error: 'Path is not a directory' });
      } catch {
        return res.status(400).json({ error: 'Folder not found' });
      }
    }

    // Use ULTRATHINK framework instead of direct Anthropic API
    // This uses Claude Code (included in $200/month Claude Max subscription)
    // ALL queries go through ULTRATHINK for 99-100% success rate with guardrails
    // SECURITY: Use ClaudePrompt/tmp directory, NOT system /tmp/ (prevents path exposure)
    const claudePromptDir = '/home/user01/claude-test/ClaudePrompt';
    const outputDir = path.join(claudePromptDir, 'tmp', 'web-outputs', session.user.id);
    const client = new UltrathinkClient(outputDir);
    const results = await client.analyzeFolder({
      folderPath: folderPath || null,
      query
    });

    res.status(200).json(results);
  } catch (error: any) {
    console.error('Analysis error:', error);
    if (error.message?.includes('rate_limit')) return res.status(429).json({ error: 'Rate limit exceeded' });
    res.status(500).json({ error: 'ULTRATHINK analysis failed: ' + error.message });
  }
}
