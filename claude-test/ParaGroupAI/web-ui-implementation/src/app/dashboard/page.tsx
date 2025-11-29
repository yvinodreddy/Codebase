'use client';

import { useState, useEffect, useRef, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize from 'rehype-sanitize';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import {
  Loader2,
  FolderOpen,
  MessageSquare,
  LogOut,
  User,
  Sparkles,
  Download,
  FileText,
  Printer,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Search,
  Folder,
  Sun,
  Moon
} from 'lucide-react';
// Theme toggle - no Context needed, works directly with DOM

interface User {
  email: string;
  name: string;
  verified: boolean;
}

interface AnalysisResult {
  summary: string;
  fullResponse?: string;
  files: Array<{ name: string; fileId: string; size: number }>;
  timestamp: string;
}

function DashboardPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const step = searchParams?.get('step');
  const resultRef = useRef<HTMLDivElement>(null);
  const [currentTheme, setCurrentTheme] = useState<'light' | 'dark'>('dark');

  // Initialize theme from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (savedTheme) {
      setCurrentTheme(savedTheme);
      document.documentElement.className = savedTheme;
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setCurrentTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.className = newTheme;
  };

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [folderPath, setFolderPath] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [showApiKeyForm, setShowApiKeyForm] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [folderPathExpanded, setFolderPathExpanded] = useState(false);
  const [advancedExpanded, setAdvancedExpanded] = useState(false);
  const [streamingMode, setStreamingMode] = useState(true); // Enable streaming by default
  const [queryMode, setQueryMode] = useState<'quiet' | 'detailed' | 'verbose' | 'web'>('quiet');
  const [minConfidence, setMinConfidence] = useState(99.0);
  const [streamingContent, setStreamingContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [abortController, setAbortController] = useState<AbortController | null>(null);
  const [streamingProgress, setStreamingProgress] = useState({ chunks: 0, bytes: 0 });
  const [debouncedContent, setDebouncedContent] = useState('');
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const [queryHistory, setQueryHistory] = useState<Array<{query: string, timestamp: string}>>([]);
  const [historyExpanded, setHistoryExpanded] = useState(false);

  useEffect(() => {
    fetchUser();
    // Load saved draft from localStorage
    const savedDraft = localStorage.getItem('para-group-draft');
    if (savedDraft) {
      try {
        const draft = JSON.parse(savedDraft);
        setQuery(draft.query || '');
        setFolderPath(draft.folderPath || '');
      } catch (e) {
        console.error('Failed to load draft:', e);
      }
    }
    // Load query history
    const savedHistory = localStorage.getItem('para-group-history');
    if (savedHistory) {
      try {
        setQueryHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Failed to load history:', e);
      }
    }
  }, []);

  // Debounce streaming content updates to reduce re-renders
  useEffect(() => {
    if (streamingContent && isStreaming) {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }

      debounceTimerRef.current = setTimeout(() => {
        setDebouncedContent(streamingContent);
      }, 50); // 50ms debounce
    } else {
      setDebouncedContent(streamingContent);
    }

    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [streamingContent, isStreaming]);

  // Auto-save draft to localStorage
  useEffect(() => {
    const draft = { query, folderPath };
    localStorage.setItem('para-group-draft', JSON.stringify(draft));
  }, [query, folderPath]);

  const fetchUser = async () => {
    try {
      const response = await fetch('/api/auth/me');
      if (!response.ok) {
        router.push('/');
        return;
      }
      const userData = await response.json();
      setUser(userData);
      setShowApiKeyForm(step === 'verify-api-key' && !userData.verified);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      router.push('/');
    } finally {
      setLoading(false);
    }
  };

  const handleApiKeySubmit = async () => {
    if (!apiKey) return;
    try {
      const response = await fetch('/api/auth/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ apiKey }),
      });
      if (response.ok) {
        setShowApiKeyForm(false);
        fetchUser();
      } else {
        alert('Invalid API key');
      }
    } catch (error) {
      alert('Failed to validate API key');
    }
  };

  const addToHistory = (newQuery: string) => {
    const newHistory = [
      { query: newQuery, timestamp: new Date().toISOString() },
      ...queryHistory.filter(h => h.query !== newQuery)
    ].slice(0, 5); // Keep only last 5
    setQueryHistory(newHistory);
    localStorage.setItem('para-group-history', JSON.stringify(newHistory));
  };

  const loadFromHistory = (historyQuery: string) => {
    setQuery(historyQuery);
    setHistoryExpanded(false);
  };

  const handleSubmit = async () => {
    if (!query) return; // Only query is required, folder path is optional
    setAnalyzing(true);
    setStreamingContent('');
    setIsStreaming(false);

    // Add to history before submitting
    addToHistory(query);

    try {
      // Use streaming mode for immediate response (2-second target)
      if (streamingMode) {
        handleStreamingSubmit();
      } else {
        // Legacy non-streaming mode
        const response = await fetch('/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            folderPath: folderPath || null,
            query,
            mode: queryMode,
            verbose: queryMode === 'verbose',
            minConfidence
          }),
        });
        if (!response.ok) throw new Error('Analysis failed');
        const data = await response.json();
        setResults(data);
        // Auto-expand if content is short, otherwise show preview
        const contentLength = data.summary?.length || 0;
        setExpanded(contentLength < 1000);
        setShowPreview(contentLength >= 1000);
        setAnalyzing(false);
      }
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Analysis failed. Please try again.');
      setAnalyzing(false);
    }
  };

  const handleCancelStreaming = () => {
    if (abortController) {
      abortController.abort();
      setAbortController(null);
      setIsStreaming(false);
      setAnalyzing(false);
      setStreamingProgress({ chunks: 0, bytes: 0 });
    }
  };

  const handleStreamingSubmit = () => {
    setIsStreaming(true);
    setStreamingContent('');
    setStreamingProgress({ chunks: 0, bytes: 0 });

    // Create AbortController for canceling mid-flight
    const controller = new AbortController();
    setAbortController(controller);

    // Use fetch with ReadableStream for SSE (EventSource only supports GET)
    fetch('/api/query-stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        folderPath: folderPath || null,
        query,
        mode: queryMode,
        verbose: queryMode === 'verbose',
        minConfidence
      }),
      signal: controller.signal
    }).then(async response => {
      if (!response.ok) throw new Error('Streaming failed');

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) throw new Error('No response body');

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          setIsStreaming(false);
          setAnalyzing(false);
          // Convert streaming content to results format
          setResults({
            summary: streamingContent || buffer,
            fullResponse: streamingContent || buffer,
            files: [],
            timestamp: new Date().toISOString()
          });
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        // Process complete SSE messages
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6));

              if (data.type === 'chunk') {
                setStreamingContent(prev => prev + data.content);
                setStreamingProgress({ chunks: data.chunkNumber, bytes: data.totalBytes });
              } else if (data.type === 'complete') {
                setIsStreaming(false);
                setAnalyzing(false);
              } else if (data.type === 'error') {
                throw new Error(data.message);
              }
            } catch (e) {
              console.error('Error parsing SSE message:', e);
            }
          }
        }
      }
    }).catch(error => {
      // Don't show error if user aborted
      if (error.name !== 'AbortError') {
        console.error('Streaming error:', error);
        alert('Streaming failed. Please try again.');
      }
      setIsStreaming(false);
      setAnalyzing(false);
      setAbortController(null);
      setStreamingProgress({ chunks: 0, bytes: 0 });
    });
  };

  const downloadMarkdown = () => {
    if (!results) return;
    const content = results.fullResponse || results.summary;
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analysis-${Date.now()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadText = () => {
    if (!results) return;
    const content = results.fullResponse || results.summary;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analysis-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadPDF = async () => {
    if (!resultRef.current) return;
    try {
      const canvas = await html2canvas(resultRef.current, {
        scale: 2,
        backgroundColor: '#0f172a',
        logging: false,
      });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'px',
        format: [canvas.width, canvas.height],
      });
      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
      pdf.save(`analysis-${Date.now()}.pdf`);
    } catch (error) {
      console.error('PDF generation failed:', error);
      alert('Failed to generate PDF. Please try again.');
    }
  };

  const handlePrint = () => {
    if (!resultRef.current) return;
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    printWindow.document.write(`
      <html>
        <head>
          <title>Analysis Results</title>
          <style>
            body {
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              padding: 2rem;
              max-width: 800px;
              margin: 0 auto;
              line-height: 1.8;
            }
            h1, h2, h3 { margin-top: 1.5rem; margin-bottom: 0.75rem; }
            p { margin-bottom: 1rem; }
            code {
              background: #f5f5f5;
              padding: 0.2rem 0.4rem;
              border-radius: 3px;
              font-family: 'Courier New', monospace;
            }
            pre {
              background: #1e293b;
              color: #e2e8f0;
              padding: 1rem;
              border-radius: 8px;
              overflow-x: auto;
            }
          </style>
        </head>
        <body>
          ${resultRef.current.innerHTML}
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  const handleFileDownload = async (fileId: string, fileName: string) => {
    try {
      const response = await fetch(`/api/file/download?id=${fileId}`);
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      alert('Failed to download file');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-dark-bg">
        <Loader2 className="animate-spin text-primary" size={48} />
      </div>
    );
  }

  if (showApiKeyForm) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-dark-bg p-4">
        <div className="bg-dark-card rounded-xl shadow-2xl p-8 max-w-md w-full border border-dark-border">
          <div className="text-center mb-6">
            <div className="inline-block p-3 bg-warning/10 rounded-full mb-4">
              <svg className="w-12 h-12 text-warning" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-dark-text mb-2">Verify Claude API Key</h2>
            <p className="text-dark-textMuted">
              Enter your Claude API key from Anthropic Console
            </p>
          </div>
          <div className="space-y-4">
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-ant-..."
              className="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-dark-text placeholder-dark-textDim"
            />
            <button
              onClick={handleApiKeySubmit}
              disabled={!apiKey}
              className="w-full bg-primary hover:bg-primary-dark text-white font-semibold py-3 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
            >
              Verify API Key
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-bg">
      {/* Header - Optimized for Less Space */}
      <header className="bg-dark-card border-b border-dark-border shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Sparkles className="text-primary" size={24} />
              <h1 className="text-xl font-bold text-dark-text">
                Para Group Dashboard
              </h1>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 text-dark-textMuted">
                <User size={16} />
                <span className="text-xs">{user?.name}</span>
              </div>
              {/* Day/Night Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="flex items-center gap-2 text-primary hover:text-primary-light transition-colors p-2 rounded-lg hover:bg-dark-hover"
                title={currentTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              >
                {currentTheme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
              </button>
              <button
                onClick={() => router.push('/api/auth/logout')}
                className="flex items-center gap-2 text-error hover:text-error/80 transition-colors"
              >
                <LogOut size={16} />
                <span className="text-xs">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        {/* Compact Folder Path - Collapsible */}
        <div className="mb-3">
          <button
            onClick={() => setFolderPathExpanded(!folderPathExpanded)}
            className="flex items-center gap-2 text-sm text-dark-textMuted hover:text-dark-text transition-colors"
          >
            <Folder size={16} className="text-primary" />
            <span>Folder Path (Optional)</span>
            <ChevronDown
              size={14}
              className={`transition-transform ${folderPathExpanded ? 'rotate-180' : ''}`}
            />
          </button>

          {folderPathExpanded && (
            <div className="mt-2 animate-in slide-in-from-top-2">
              <input
                type="text"
                value={folderPath}
                onChange={(e) => setFolderPath(e.target.value)}
                placeholder="/path/to/your/project"
                className="w-full px-3 py-2 bg-dark-card border border-dark-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-dark-text placeholder-dark-textDim text-sm"
              />
              <p className="mt-1 text-xs text-dark-textMuted">
                Leave empty for general queries, or specify a path to analyze a specific folder
              </p>
            </div>
          )}
        </div>

        {/* History/Recents - Collapsible */}
        {queryHistory.length > 0 && (
          <div className="mb-3">
            <button
              onClick={() => setHistoryExpanded(!historyExpanded)}
              className="flex items-center gap-2 text-sm text-dark-textMuted hover:text-dark-text transition-colors"
            >
              <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Recent Queries ({queryHistory.length})</span>
              <ChevronDown
                size={14}
                className={`transition-transform ${historyExpanded ? 'rotate-180' : ''}`}
              />
            </button>

            {historyExpanded && (
              <div className="mt-2 space-y-1 animate-in slide-in-from-top-2">
                {queryHistory.map((item, index) => (
                  <button
                    key={index}
                    onClick={() => loadFromHistory(item.query)}
                    className="w-full text-left px-3 py-2 bg-dark-card border border-dark-border rounded-lg hover:bg-dark-hover transition-colors group"
                  >
                    <div className="flex items-center justify-between">
                      <p className="text-sm text-dark-text truncate flex-1 group-hover:text-primary transition-colors">
                        {item.query}
                      </p>
                      <span className="text-xs text-dark-textDim ml-2 flex-shrink-0">
                        {new Date(item.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Advanced Options - Collapsible */}
        <div className="mb-3">
          <button
            onClick={() => setAdvancedExpanded(!advancedExpanded)}
            className="flex items-center gap-2 text-sm text-dark-textMuted hover:text-dark-text transition-colors"
          >
            <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
            <span>Advanced Options</span>
            <ChevronDown
              size={14}
              className={`transition-transform ${advancedExpanded ? 'rotate-180' : ''}`}
            />
          </button>

          {advancedExpanded && (
            <div className="mt-2 p-4 bg-dark-card rounded-lg border border-dark-border animate-in slide-in-from-top-2">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Query Mode */}
                <div>
                  <label className="block text-xs font-medium text-dark-text mb-2">
                    Query Mode
                  </label>
                  <select
                    value={queryMode}
                    onChange={(e) => setQueryMode(e.target.value as any)}
                    className="w-full px-3 py-2 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary text-dark-text text-sm"
                  >
                    <option value="quiet">Quiet (Default) - Brief answers, fast results</option>
                    <option value="detailed">Detailed - Comprehensive with examples</option>
                    <option value="verbose">Verbose - Full processing details</option>
                    <option value="web">Web - Copy-paste ready prompt</option>
                  </select>
                </div>

                {/* Minimum Confidence */}
                <div>
                  <label className="block text-xs font-medium text-dark-text mb-2">
                    Minimum Confidence: {minConfidence.toFixed(1)}%
                  </label>
                  <input
                    type="range"
                    min="90"
                    max="100"
                    step="0.5"
                    value={minConfidence}
                    onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
                    className="w-full accent-primary"
                  />
                  <div className="flex justify-between text-xs text-dark-textMuted mt-1">
                    <span>90%</span>
                    <span>95%</span>
                    <span>99%</span>
                    <span>100%</span>
                  </div>
                </div>

                {/* Streaming Mode Toggle */}
                <div className="md:col-span-2">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={streamingMode}
                      onChange={(e) => setStreamingMode(e.target.checked)}
                      className="w-4 h-4 accent-primary"
                    />
                    <div>
                      <span className="text-sm font-medium text-dark-text">
                        Enable Streaming (Recommended)
                      </span>
                      <p className="text-xs text-dark-textMuted">
                        Start seeing results within 2 seconds instead of waiting for complete response
                      </p>
                    </div>
                  </label>
                </div>
              </div>

              <div className="mt-3 p-2 bg-dark-bg rounded border-l-4 border-primary">
                <p className="text-xs text-dark-textMuted">
                  <strong className="text-primary">💡 Tip:</strong> Use Quiet mode with Streaming enabled for fastest results (2-second initial response)
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Prominent Query Input with Inline Search Button */}
        <div className="bg-dark-card rounded-xl shadow-lg p-6 border border-dark-border mb-6">
          <label className="flex items-center gap-2 text-base font-medium text-dark-text mb-3">
            <MessageSquare size={20} className="text-primary" />
            What would you like to know?
            <span className="text-xs text-error">*Required</span>
          </label>

          <div className="flex gap-3">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask any question... Type your query here and press Cmd/Ctrl+Enter or click Search"
              rows={4}
              disabled={analyzing}
              className="flex-1 px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-dark-text placeholder-dark-textDim resize-none transition-all leading-relaxed text-base"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                  handleSubmit();
                }
              }}
            />

            {/* Professional Search Button - Right Side */}
            <button
              onClick={handleSubmit}
              disabled={analyzing || !query}
              title="Search (Cmd/Ctrl+Enter)"
              className="group relative px-8 py-3 bg-gradient-to-r from-primary to-primary-dark hover:from-primary-dark hover:to-primary disabled:from-dark-hover disabled:to-dark-hover disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all duration-300 flex items-center justify-center gap-3 shadow-2xl hover:shadow-primary/50 hover:scale-105 disabled:hover:scale-100 h-fit self-center"
            >
              {analyzing ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  <span className="hidden sm:inline">{isStreaming ? 'Streaming...' : 'Processing...'}</span>
                </>
              ) : (
                <>
                  <Search size={20} />
                  <span className="hidden sm:inline">Search</span>
                </>
              )}
              <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 rounded-xl transition-opacity duration-300" />
            </button>
          </div>

          <div className="mt-3 flex items-center justify-between text-xs text-dark-textMuted">
            <span>Press ⌘+Enter (Mac) or Ctrl+Enter (Windows) to search</span>
            {streamingMode && <span className="text-success">⚡ Streaming enabled - 2s response time</span>}
          </div>
        </div>

        {/* Results Area - Maximum Space */}
        <div>
            {(results || isStreaming) ? (
              <div className="bg-dark-card rounded-xl shadow-lg border border-dark-border overflow-hidden">
                {/* Results Header */}
                <div className="bg-gradient-to-r from-primary/10 to-secondary/10 p-6 border-b border-dark-border">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {isStreaming ? (
                        <Loader2 className="w-6 h-6 text-primary animate-spin" />
                      ) : (
                        <svg className="w-6 h-6 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      )}
                      <h2 className="text-xl font-bold text-dark-text">
                        {isStreaming ? 'Streaming Response...' : 'Response'}
                      </h2>
                    </div>

                    {/* Action Buttons - Only show when not streaming */}
                    {!isStreaming && (
                      <div className="flex items-center gap-2">
                      <button
                        onClick={downloadMarkdown}
                        title="Download as Markdown"
                        className="p-2 text-primary hover:text-primary-light hover:bg-dark-bg/50 rounded-lg transition-all"
                      >
                        <FileText size={18} />
                      </button>
                      <button
                        onClick={downloadText}
                        title="Download as Text"
                        className="p-2 text-primary hover:text-primary-light hover:bg-dark-bg/50 rounded-lg transition-all"
                      >
                        <Download size={18} />
                      </button>
                      <button
                        onClick={downloadPDF}
                        title="Download as PDF"
                        className="p-2 text-primary hover:text-primary-light hover:bg-dark-bg/50 rounded-lg transition-all"
                      >
                        <svg className="w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                        </svg>
                      </button>
                      <button
                        onClick={handlePrint}
                        title="Print"
                        className="p-2 text-primary hover:text-primary-light hover:bg-dark-bg/50 rounded-lg transition-all"
                      >
                        <Printer size={18} />
                      </button>
                      </div>
                    )}
                  </div>
                  {!isStreaming && results && (
                    <p className="mt-2 text-xs text-dark-textDim">
                      Generated at: {new Date(results.timestamp).toLocaleString()}
                    </p>
                  )}
                  {isStreaming && (
                    <div className="mt-3 space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className="flex gap-1">
                            <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                            <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                            <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                          </div>
                          <p className="text-xs text-primary">Processing your query...</p>
                        </div>
                        <button
                          onClick={handleCancelStreaming}
                          className="px-3 py-1 text-xs bg-error hover:bg-error/80 text-white rounded-lg transition-colors flex items-center gap-1"
                        >
                          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                          Cancel
                        </button>
                      </div>
                      {/* Progress Bar */}
                      {streamingProgress.chunks > 0 && (
                        <div className="space-y-1">
                          <div className="flex justify-between text-xs text-dark-textDim">
                            <span>{streamingProgress.chunks} chunks</span>
                            <span>{(streamingProgress.bytes / 1024).toFixed(1)} KB</span>
                          </div>
                          <div className="w-full bg-dark-bg rounded-full h-1.5 overflow-hidden">
                            <div className="h-full bg-gradient-to-r from-primary to-secondary animate-pulse"></div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Response Content */}
                <div
                  ref={resultRef}
                  className={`p-6 ${expanded ? 'max-h-none' : 'max-h-[600px]'} overflow-y-auto`}
                >
                  <div className="prose prose-invert prose-lg max-w-none">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeRaw, rehypeSanitize]}
                      components={{
                        // Headings with proper spacing
                        h1: ({ node, ...props }) => (
                          <h1 className="text-3xl font-bold text-dark-text mb-4 mt-8 pb-2 border-b border-dark-border" {...props} />
                        ),
                        h2: ({ node, ...props }) => (
                          <h2 className="text-2xl font-bold text-dark-text mb-3 mt-6" {...props} />
                        ),
                        h3: ({ node, ...props }) => (
                          <h3 className="text-xl font-semibold text-dark-text mb-2 mt-5" {...props} />
                        ),
                        h4: ({ node, ...props }) => (
                          <h4 className="text-lg font-semibold text-dark-text mb-2 mt-4" {...props} />
                        ),

                        // Paragraphs with proper spacing
                        p: ({ node, ...props }) => (
                          <p className="text-dark-textMuted mb-4 leading-relaxed tracking-wide" {...props} />
                        ),

                        // Lists with proper spacing
                        ul: ({ node, ...props }) => (
                          <ul className="list-disc list-inside space-y-2 mb-4 text-dark-textMuted" {...props} />
                        ),
                        ol: ({ node, ...props }) => (
                          <ol className="list-decimal list-inside space-y-2 mb-4 text-dark-textMuted" {...props} />
                        ),
                        li: ({ node, ...props }) => (
                          <li className="leading-relaxed ml-4" {...props} />
                        ),

                        // Code blocks with syntax highlighting
                        code: ({ node, inline, className, children, ...props }: any) => {
                          const match = /language-(\w+)/.exec(className || '');
                          return !inline && match ? (
                            <SyntaxHighlighter
                              style={vscDarkPlus}
                              language={match[1]}
                              PreTag="div"
                              className="rounded-lg my-4 shadow-lg"
                              customStyle={{
                                padding: '1.5rem',
                                fontSize: '0.95rem',
                                lineHeight: '1.6',
                              }}
                              {...props}
                            >
                              {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                          ) : (
                            <code className="bg-dark-bg text-primary px-2 py-1 rounded text-sm font-mono" {...props}>
                              {children}
                            </code>
                          );
                        },

                        // Blockquotes
                        blockquote: ({ node, ...props }) => (
                          <blockquote className="border-l-4 border-primary pl-4 py-2 my-4 italic text-dark-textMuted bg-dark-bg/50 rounded-r" {...props} />
                        ),

                        // Tables
                        table: ({ node, ...props }) => (
                          <div className="overflow-x-auto my-6">
                            <table className="min-w-full border-collapse border border-dark-border" {...props} />
                          </div>
                        ),
                        th: ({ node, ...props }) => (
                          <th className="border border-dark-border bg-dark-bg px-4 py-2 text-left font-semibold text-dark-text" {...props} />
                        ),
                        td: ({ node, ...props }) => (
                          <td className="border border-dark-border px-4 py-2 text-dark-textMuted" {...props} />
                        ),

                        // Links open in new tab
                        a: ({ node, ...props }) => (
                          <a
                            className="text-primary hover:text-primary-light underline inline-flex items-center gap-1 transition-colors"
                            target="_blank"
                            rel="noopener noreferrer"
                            {...props}
                          >
                            {props.children}
                            <ExternalLink size={14} className="inline" />
                          </a>
                        ),

                        // Horizontal rules
                        hr: ({ node, ...props }) => (
                          <hr className="border-dark-border my-6" {...props} />
                        ),

                        // Strong/bold text
                        strong: ({ node, ...props }) => (
                          <strong className="font-bold text-dark-text" {...props} />
                        ),

                        // Emphasis/italic text
                        em: ({ node, ...props }) => (
                          <em className="italic text-dark-text" {...props} />
                        ),
                      }}
                    >
                      {isStreaming ? debouncedContent : (results?.fullResponse || results?.summary || '')}
                    </ReactMarkdown>
                  </div>
                </div>

                {/* Expand/Collapse Button */}
                {showPreview && (
                  <div className="border-t border-dark-border p-4 text-center">
                    <button
                      onClick={() => setExpanded(!expanded)}
                      className="flex items-center justify-center gap-2 mx-auto text-primary hover:text-primary-light transition-colors"
                    >
                      {expanded ? (
                        <>
                          <ChevronUp size={18} />
                          <span>Show Less</span>
                        </>
                      ) : (
                        <>
                          <ChevronDown size={18} />
                          <span>Show More</span>
                        </>
                      )}
                    </button>
                  </div>
                )}

                {/* Output Files */}
                {results && results.files && results.files.length > 0 && (
                  <div className="border-t border-dark-border p-6">
                    <h3 className="text-sm font-medium text-dark-text mb-3">
                      Additional Files ({results.files.length})
                    </h3>
                    <div className="space-y-2">
                      {results.files.map((file, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between bg-dark-bg rounded-lg p-3 hover:bg-dark-hover transition-colors border border-dark-border"
                        >
                          <div className="flex items-center gap-3">
                            <svg className="w-5 h-5 text-primary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <div>
                              <p className="text-sm font-medium text-dark-text">
                                {file.name}
                              </p>
                              <p className="text-xs text-dark-textDim">
                                {(file.size / 1024).toFixed(2)} KB
                              </p>
                            </div>
                          </div>
                          <button
                            onClick={() => handleFileDownload(file.fileId, file.name)}
                            className="text-primary hover:text-primary-light p-2 rounded-lg hover:bg-dark-hover transition-all"
                            title="Download file"
                          >
                            <Download size={18} />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-dark-card rounded-xl shadow-lg p-8 text-center border border-dark-border">
                <div className="inline-block p-4 bg-dark-bg rounded-full mb-4">
                  <Sparkles className="text-primary" size={32} />
                </div>
                <h3 className="text-xl font-semibold text-dark-text mb-2">
                  Ready to Help
                </h3>
                <p className="text-dark-textMuted leading-relaxed">
                  Enter your query to get started. You can ask any question with or without a folder path.
                </p>
              </div>
            )}
          </div>
      </main>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-dark-bg">
        <div className="text-center">
          <Loader2 className="animate-spin text-primary mx-auto mb-4" size={48} />
          <p className="text-dark-textMuted">Loading dashboard...</p>
        </div>
      </div>
    }>
      <DashboardPageContent />
    </Suspense>
  );
}
