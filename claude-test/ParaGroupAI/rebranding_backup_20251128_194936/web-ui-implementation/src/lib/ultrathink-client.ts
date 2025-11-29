import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
import * as path from 'path';

const execAsync = promisify(exec);

export interface AnalysisRequest {
  folderPath: string | null;
  query: string;
}

export interface AnalysisResult {
  summary: string;
  fullResponse: string;
  files: Array<{ name: string; fileId: string; size: number }>;
  timestamp: string;
}

export class UltrathinkClient {
  private ultrathinkPath: string;
  private outputDir: string;

  constructor(outputDir: string = '/home/user01/claude-test/ClaudePrompt/tmp/web-outputs') {
    this.ultrathinkPath = '/home/user01/claude-test/ClaudePrompt';
    this.outputDir = outputDir;
    // SECURITY: Never use system /tmp/ - always use ClaudePrompt/tmp/
  }

  async analyzeFolder(request: AnalysisRequest): Promise<AnalysisResult> {
    // Convert Windows path to WSL path if needed (only if folder path provided)
    let analyzePath: string | null = null;
    if (request.folderPath) {
      const convertedPath = this.convertWindowsPathToWSL(request.folderPath);
      analyzePath = convertedPath;
    }

    // Build comprehensive analysis prompt (works with or without folder)
    const prompt = await this.buildAnalysisPrompt({ ...request, folderPath: analyzePath });

    // Execute ULTRATHINK framework via cpps command (not cpp)
    const ultrathinkOutput = await this.executeUltrathink(prompt);

    // Parse ULTRATHINK output file
    const parsedResults = await this.parseUltrathinkOutput(ultrathinkOutput.outputFile);

    // Save analysis to user-friendly file
    const outputFiles = await this.saveAnalysis(parsedResults, request.query);

    return {
      summary: this.extractSummary(parsedResults.fullAnalysis),
      fullResponse: parsedResults.fullAnalysis,
      files: outputFiles,
      timestamp: new Date().toISOString(),
    };
  }

  private convertWindowsPathToWSL(windowsPath: string): string {
    // Check if this is a Windows path (C:\, D:\, etc.)
    const windowsPathRegex = /^([A-Za-z]):(\\|\/)/;
    const match = windowsPath.match(windowsPathRegex);

    if (match) {
      const driveLetter = match[1].toLowerCase();
      // Convert C:\Users\... to /mnt/c/Users/...
      let wslPath = windowsPath
        .replace(/^[A-Za-z]:/, `/mnt/${driveLetter}`)
        .replace(/\\/g, '/');

      return wslPath;
    }

    // Already a Unix path, return as-is
    return windowsPath;
  }

  private async buildAnalysisPrompt(request: AnalysisRequest): Promise<string> {
    // Check if this is a general query (no folder) or code analysis (with folder)
    const hasFolder = request.folderPath !== null && request.folderPath !== '';

    if (!hasFolder) {
      // General query without folder - just pass the question to ULTRATHINK
      return `USER QUERY:
${request.query}

Please provide a comprehensive, detailed answer to the user's query with 99-100% confidence.
Use markdown formatting for better readability.`;
    }

    // Code analysis with folder - scan and include all files
    const folderContents = await this.scanFolder(request.folderPath!);

    let prompt = `COMPREHENSIVE CODEBASE ANALYSIS REQUEST

FOLDER PATH: ${request.folderPath}
TOTAL FILES: ${folderContents.size}

USER QUERY:
${request.query}

CODEBASE CONTENTS:
${'='.repeat(80)}

`;

    // Add all files to prompt
    for (const [filePath, content] of folderContents.entries()) {
      prompt += `
FILE: ${filePath}
${'='.repeat(80)}

${content}

${'='.repeat(80)}

`;
    }

    prompt += `
${'='.repeat(80)}
ANALYSIS REQUIREMENTS:
${'='.repeat(80)}

1. Provide a comprehensive, detailed analysis addressing the user's query
2. Analyze all code files in context
3. Identify patterns, issues, and improvements
4. Provide specific file locations and line numbers when relevant
5. Give actionable recommendations
6. Include code examples where helpful

DELIVERABLES:
1. Executive Summary (2-3 paragraphs)
2. Detailed Analysis (organized by topic)
3. Findings (list of key discoveries)
4. Recommendations (prioritized action items)
5. Code Examples (if applicable)

Please provide production-ready, comprehensive analysis with 99-100% confidence.
`;

    return prompt;
  }

  private async scanFolder(folderPath: string): Promise<Map<string, string>> {
    const contents = new Map<string, string>();
    const maxFileSize = 1024 * 1024; // 1MB
    const excludeDirs = ['node_modules', '.git', 'dist', 'build', '.next', '__pycache__'];

    async function scan(dirPath: string) {
      try {
        const entries = await fs.readdir(dirPath, { withFileTypes: true });

        for (const entry of entries) {
          const fullPath = path.join(dirPath, entry.name);

          if (excludeDirs.includes(entry.name)) continue;

          if (entry.isDirectory()) {
            await scan(fullPath);
          } else if (entry.isFile()) {
            try {
              const stats = await fs.stat(fullPath);
              if (stats.size <= maxFileSize) {
                const content = await fs.readFile(fullPath, 'utf-8');
                contents.set(fullPath, content);
              }
            } catch (err) {
              // Skip files we can't read
            }
          }
        }
      } catch (err) {
        // Skip directories we can't read
      }
    }

    await scan(folderPath);
    return contents;
  }

  private async executeUltrathink(prompt: string): Promise<{ outputFile: string; stdout: string }> {
    // Get timestamped output file path
    const getOutputPathCmd = `cd ${this.ultrathinkPath} && python3 get_output_path.py`;
    const { stdout: outputFilePath } = await execAsync(getOutputPathCmd);
    const outputFile = outputFilePath.trim();

    // Write prompt to temporary file to avoid E2BIG error (command line argument too large)
    // Use ClaudePrompt/tmp directory which is whitelisted for security
    const timestamp = Date.now();
    const tempDir = path.join(this.ultrathinkPath, 'tmp');
    await fs.mkdir(tempDir, { recursive: true });
    const tempPromptFile = path.join(tempDir, `ultrathink-prompt-${timestamp}.txt`);
    await fs.writeFile(tempPromptFile, prompt, 'utf-8');

    // Execute ULTRATHINK cpps command using --file flag (USER REQUIREMENT: Use cpps -v instead of cpp --verbose)
    // Use --file instead of command line argument to avoid E2BIG error with large codebases
    const cppsCommand = `cd ${this.ultrathinkPath} && ./cpps --file "${tempPromptFile}" -v 2>&1 > "${outputFile}"`;

    // 🔧 FIX #1: Debug logging to diagnose issues
    const debugLog = path.join(this.outputDir, 'ultrathink-debug.log');
    await fs.mkdir(this.outputDir, { recursive: true });

    const logEntry = {
      timestamp: new Date().toISOString(),
      command: cppsCommand,
      tempFile: tempPromptFile,
      outputFile: outputFile,
      promptLength: prompt.length,
    };

    try {
      await fs.appendFile(debugLog, JSON.stringify(logEntry, null, 2) + '\n', 'utf-8');
    } catch {
      // Ignore logging errors - don't fail the request
    }

    let executionError: any = null;

    try {
      const { stdout, stderr } = await execAsync(cppsCommand, {
        maxBuffer: 10 * 1024 * 1024, // 10MB buffer
        timeout: 300000, // 5 minute timeout
      });

      // 🔧 FIX #1: Log success
      try {
        await fs.appendFile(debugLog, `SUCCESS\nSTDOUT: ${stdout}\nSTDERR: ${stderr}\n\n`, 'utf-8');
      } catch {
        // Ignore logging errors
      }

    } catch (error: any) {
      executionError = error;

      // 🔧 FIX #1: Log the ACTUAL error with full details
      try {
        await fs.appendFile(
          debugLog,
          `ERROR: ${error.message}\nSTDOUT: ${error.stdout || ''}\nSTDERR: ${error.stderr || ''}\nSTACK: ${error.stack || ''}\n\n`,
          'utf-8'
        );
      } catch {
        // Ignore logging errors
      }

      // cpps command might return non-zero exit code, but that's ok if output file exists
      if (!(await this.fileExists(outputFile))) {
        throw new Error(`ULTRATHINK execution failed: ${error.message}\nSTDERR: ${error.stderr || ''}`);
      }
    }

    // 🔧 FIX #2: Wait before cleanup to prevent race condition
    // Ensure cpp has completely finished reading the temp file
    await new Promise(resolve => setTimeout(resolve, 1000)); // 1 second delay

    // Clean up temporary prompt file AFTER ensuring output exists
    try {
      await fs.unlink(tempPromptFile);
    } catch {
      // Ignore cleanup errors
    }

    return { outputFile, stdout: '' };
  }

  private async parseUltrathinkOutput(outputFilePath: string): Promise<{
    fullAnalysis: string;
  }> {
    const content = await fs.readFile(outputFilePath, 'utf-8');

    return {
      fullAnalysis: content,
    };
  }

  private extractSummary(fullAnalysis: string): string {
    // Look for the actual answer after the ULTRATHINK framework output
    const answerMarker = '⬇️  SCROLL DOWN FOR THE ACTUAL ANSWER  ⬇️';
    const answerStartIndex = fullAnalysis.indexOf(answerMarker);

    let analysisText = fullAnalysis;
    if (answerStartIndex !== -1) {
      analysisText = fullAnalysis.substring(answerStartIndex + answerMarker.length);
    }

    // Extract first meaningful section (up to 500 words)
    const words = analysisText.split(/\s+/).filter(word =>
      word.length > 0 && !word.match(/^[═│┌┐└┘├┤┬┴┼─┃━]+$/)
    );

    const summaryWords = words.slice(0, 500);
    let summary = summaryWords.join(' ');

    if (words.length > 500) {
      summary += '\n\n[Full analysis available in output file]';
    }

    return summary;
  }

  private async saveAnalysis(
    parsedResults: { fullAnalysis: string },
    query: string
  ): Promise<Array<{ name: string; fileId: string; size: number }>> {
    await fs.mkdir(this.outputDir, { recursive: true });

    const timestamp = Date.now();
    const sanitizedQuery = query.replace(/[^a-z0-9]+/gi, '-').toLowerCase().substring(0, 50);
    const fileName = `ultrathink-analysis-${sanitizedQuery}-${timestamp}.txt`;
    const filePath = path.join(this.outputDir, fileName);

    // SECURITY: Generate secure file ID instead of exposing real path
    const fileId = this.generateSecureFileId(fileName, timestamp);

    // Create formatted output file
    const formattedOutput = `
${'='.repeat(80)}
PARA GROUP WEB UI - ANALYSIS RESULTS
${'='.repeat(80)}

Generated: ${new Date().toISOString()}
Powered by: ULTRATHINK Framework

${'='.repeat(80)}
QUERY
${'='.repeat(80)}

${query}

${'='.repeat(80)}
FULL ANALYSIS
${'='.repeat(80)}

${parsedResults.fullAnalysis}

${'='.repeat(80)}
END OF ANALYSIS
${'='.repeat(80)}
`;

    await fs.writeFile(filePath, formattedOutput, 'utf-8');
    const stats = await fs.stat(filePath);

    // SECURITY: Save file mapping to enable secure downloads (file ID -> actual path)
    await this.saveFileMapping(fileId, filePath);

    return [{
      name: fileName,
      fileId: fileId,  // SECURITY: Return file ID, never expose actual path
      size: stats.size,
    }];
  }

  private generateSecureFileId(fileName: string, timestamp: number): string {
    // Create a secure, non-guessable file ID
    const crypto = require('crypto');
    const hash = crypto.createHash('sha256')
      .update(`${fileName}-${timestamp}-${Math.random()}`)
      .digest('hex');
    return hash.substring(0, 32);  // Use first 32 chars
  }

  private async saveFileMapping(fileId: string, filePath: string): Promise<void> {
    // Store file ID -> path mapping in secure location
    const mappingFile = path.join(this.outputDir, '.file-mappings.json');
    let mappings: Record<string, string> = {};

    try {
      const existing = await fs.readFile(mappingFile, 'utf-8');
      mappings = JSON.parse(existing);
    } catch {
      // File doesn't exist yet, start fresh
    }

    mappings[fileId] = filePath;
    await fs.writeFile(mappingFile, JSON.stringify(mappings, null, 2), 'utf-8');
  }

  private async fileExists(filePath: string): Promise<boolean> {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }
}
