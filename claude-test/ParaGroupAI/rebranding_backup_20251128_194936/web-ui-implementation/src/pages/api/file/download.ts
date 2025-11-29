import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';
import * as fs from 'fs/promises';
import * as path from 'path';

/**
 * SECURITY: Secure file download endpoint
 * - Uses file IDs instead of exposing paths
 * - Validates user session
 * - Prevents directory traversal attacks
 * - Only serves files from allowed directories
 * - Content-Disposition header prevents XSS
 */
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  try {
    // Verify authentication
    const token = getCookie('session', { req, res });
    if (!token || typeof token !== 'string') return res.status(401).json({ error: 'Not authenticated' });

    const session = await verifySession(token);
    if (!session) return res.status(401).json({ error: 'Unauthorized' });

    const { id } = req.query;
    if (!id || typeof id !== 'string') {
      return res.status(400).json({ error: 'File ID is required' });
    }

    // SECURITY: Validate file ID format (prevents injection attacks)
    if (!/^[a-f0-9]{32}$/.test(id)) {
      return res.status(400).json({ error: 'Invalid file ID format' });
    }

    // Get file path from secure mapping
    const claudePromptDir = '/home/user01/claude-test/ClaudePrompt';
    const userOutputDir = path.join(claudePromptDir, 'tmp', 'web-outputs', session.user.id);
    const mappingFile = path.join(userOutputDir, '.file-mappings.json');

    let mappings: Record<string, string> = {};
    try {
      const mappingContent = await fs.readFile(mappingFile, 'utf-8');
      mappings = JSON.parse(mappingContent);
    } catch (error) {
      return res.status(404).json({ error: 'File not found' });
    }

    const filePath = mappings[id];
    if (!filePath) {
      return res.status(404).json({ error: 'File not found' });
    }

    // SECURITY: Verify file is within allowed directory (prevents directory traversal)
    const resolvedPath = path.resolve(filePath);
    const resolvedUserDir = path.resolve(userOutputDir);
    if (!resolvedPath.startsWith(resolvedUserDir)) {
      return res.status(403).json({ error: 'Access denied - path outside allowed directory' });
    }

    // Get file name for download
    const fileName = path.basename(filePath);

    // Read file content
    const content = await fs.readFile(filePath);

    // SECURITY: Set headers to force download and prevent XSS
    res.setHeader('Content-Type', 'application/octet-stream');
    res.setHeader('Content-Disposition', `attachment; filename="${fileName}"`);
    res.setHeader('X-Content-Type-Options', 'nosniff');  // Prevent MIME sniffing
    res.setHeader('Content-Security-Policy', "default-src 'none'");  // Prevent script execution

    res.status(200).send(content);
  } catch (error: any) {
    console.error('Download error:', error);
    res.status(500).json({ error: 'Failed to download file' });
  }
}
