import { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
import { verifySession } from '@/lib/auth';
import * as path from 'path';
import * as fs from 'fs/promises';
import { spawn } from 'child_process';

/**
 * Server-Sent Events (SSE) endpoint for streaming ULTRATHINK query results
 *
 * This endpoint provides real-time progressive rendering for Claude Code responses,
 * achieving the critical 2-second initial response time requirement.
 *
 * Implementation strategy:
 * 1. Start cpps command immediately in background
 * 2. Stream output file chunks as they're written
 * 3. Client renders progressively (like ChatGPT/Claude Web)
 * 4. Complete within 2 seconds for first content
 */
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const token = getCookie('session', { req, res });
    if (!token || typeof token !== 'string') {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    const session = await verifySession(token);
    if (!session) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const {
      folderPath,
      query,
      mode = 'quiet',  // Default to quiet mode for faster responses
      verbose = false,
      minConfidence = 99.0
    } = req.body;

    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }

    // Validate folder path only if provided
    if (folderPath) {
      try {
        const stats = await fs.stat(folderPath);
        if (!stats.isDirectory()) {
          return res.status(400).json({ error: 'Path is not a directory' });
        }
      } catch {
        return res.status(400).json({ error: 'Folder not found' });
      }
    }

    // Set up Server-Sent Events headers
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache, no-transform');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no'); // Disable nginx buffering

    // Generate timestamped output file
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const outputFile = path.join('/tmp', `streaming_output_${session.user.id}_${timestamp}.txt`);

    // Build cpps command - create temp file for query to avoid shell escaping issues
    const cppsCwd = '/home/user01/claude-test/ClaudePrompt';
    const cppsCmd = './cpps';

    // Always use file-based input to avoid command-line escaping issues
    const promptContent = folderPath
      ? `FOLDER PATH: ${folderPath}\n\nQUERY: ${query}`
      : query;

    const promptFile = path.join('/tmp', `prompt_${session.user.id}_${timestamp}.txt`);
    await fs.writeFile(promptFile, promptContent);

    // Build args array (no shell escaping needed with file input)
    const args: string[] = ['--file', promptFile];

    // Add mode flags
    if (mode === 'quiet' || !verbose) {
      args.push('-q');
    } else if (mode === 'verbose' || verbose) {
      args.push('-v');
    }

    // Add minimum confidence if specified
    if (minConfidence && minConfidence !== 99.0) {
      args.push('--min-confidence', minConfidence.toString());
    }

    // Start cpps process in background (no shell: true to avoid escaping issues)
    const cppsProcess = spawn(cppsCmd, args, {
      cwd: cppsCwd,
      env: { ...process.env }
    });

    // Redirect output to file
    const outputStream = await fs.open(outputFile, 'w');
    cppsProcess.stdout.on('data', async (data) => {
      await outputStream.write(data);
    });
    cppsProcess.stderr.on('data', async (data) => {
      await outputStream.write(data);
    });

    // Send initial connection event
    res.write('data: {"type":"connected","message":"Processing your query..."}\n\n');

    // Track what we've already sent
    let lastSentPosition = 0;
    let chunkCount = 0;
    let firstChunkSent = false;

    // Poll output file for new content
    const pollInterval = setInterval(async () => {
      try {
        const stats = await fs.stat(outputFile);
        const currentSize = stats.size;

        if (currentSize > lastSentPosition) {
          // Read new content since last poll
          const fileHandle = await fs.open(outputFile, 'r');
          const buffer = Buffer.alloc(currentSize - lastSentPosition);
          await fileHandle.read(buffer, 0, buffer.length, lastSentPosition);
          await fileHandle.close();

          const newContent = buffer.toString('utf-8');
          lastSentPosition = currentSize;
          chunkCount++;

          // Send chunk to client
          const event = {
            type: 'chunk',
            content: newContent,
            chunkNumber: chunkCount,
            totalBytes: currentSize
          };

          res.write(`data: ${JSON.stringify(event)}\n\n`);

          // Mark first chunk sent (critical 2-second metric)
          if (!firstChunkSent) {
            firstChunkSent = true;
            console.log(`[STREAMING] First chunk sent in ${Date.now() - startTime}ms`);
          }
        }
      } catch (error) {
        // File not created yet, continue polling
      }
    }, 100); // Poll every 100ms for real-time streaming

    const startTime = Date.now();

    // Handle process completion
    cppsProcess.on('close', async (code) => {
      clearInterval(pollInterval);
      await outputStream.close();

      // Send any remaining content
      try {
        const finalContent = await fs.readFile(outputFile, 'utf-8');
        if (finalContent.length > lastSentPosition) {
          const remaining = finalContent.substring(lastSentPosition);
          res.write(`data: ${JSON.stringify({
            type: 'chunk',
            content: remaining,
            chunkNumber: chunkCount + 1,
            totalBytes: finalContent.length
          })}\n\n`);
        }
      } catch (error) {
        console.error('Error reading final content:', error);
      }

      // Send completion event
      const completionEvent = {
        type: 'complete',
        exitCode: code,
        totalChunks: chunkCount,
        processingTimeMs: Date.now() - startTime,
        message: code === 0 ? 'Query completed successfully' : 'Query completed with errors'
      };

      res.write(`data: ${JSON.stringify(completionEvent)}\n\n`);
      res.end();

      // Cleanup temporary files
      try {
        await fs.unlink(outputFile);
        if (folderPath) {
          const promptFile = path.join('/tmp', `prompt_${session.user.id}_${timestamp}.txt`);
          await fs.unlink(promptFile);
        }
      } catch (error) {
        console.error('Cleanup error:', error);
      }
    });

    // Handle process errors
    cppsProcess.on('error', (error) => {
      clearInterval(pollInterval);
      res.write(`data: ${JSON.stringify({
        type: 'error',
        message: error.message
      })}\n\n`);
      res.end();
    });

    // Handle client disconnect
    req.on('close', () => {
      clearInterval(pollInterval);
      cppsProcess.kill('SIGTERM');
      outputStream.close();
    });

  } catch (error: any) {
    console.error('Streaming error:', error);
    res.write(`data: ${JSON.stringify({
      type: 'error',
      message: 'Streaming failed: ' + error.message
    })}\n\n`);
    res.end();
  }
}
