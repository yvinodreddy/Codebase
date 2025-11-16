import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';
import * as fs from 'fs/promises';
import * as path from 'path';

/**
 * SECURITY: Secure file preview endpoint
 * - Uses file IDs instead of exposing paths
 * - Validates user session
 * - Prevents directory traversal attacks
 * - Only serves files from allowed directories
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

    // Read file content
    const content = await fs.readFile(filePath, 'utf-8');

    // Return content (limit to 1MB for preview)
    const maxPreviewSize = 1024 * 1024; // 1MB
    const previewContent = content.length > maxPreviewSize
      ? content.substring(0, maxPreviewSize) + '\n\n[... Content truncated for preview. Download full file to see more ...]'
      : content;

    res.status(200).json({ content: previewContent });
  } catch (error: any) {
    console.error('Preview error:', error);
    res.status(500).json({ error: 'Failed to preview file' });
  }
}
