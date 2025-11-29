#!/bin/bash

################################################################################
# APPLY DARK THEME TO ALL PAGES
################################################################################
# This script creates/updates all page components with dark theme
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${BLUE}🌙 Applying Dark Theme to All Pages${NC}"
echo "======================================"
echo ""

# Navigate to project directory
BASE_DIR="/home/user01/claude-test/ClaudePrompt/web-ui-implementation"
cd "$BASE_DIR"

################################################################################
# CREATE DARK-THEMED PAGE COMPONENTS
################################################################################

echo -e "${YELLOW}Creating dark-themed page components...${NC}"

# Create app directory structure
mkdir -p src/app/dashboard
mkdir -p src/app/results/\[id\]

# src/app/layout.tsx (Root Layout with Dark Theme)
cat > src/app/layout.tsx << 'EOF'
import type { Metadata } from 'next'
import '../styles/globals.css'

export const metadata: Metadata = {
  title: 'Para Group Web UI',
  description: 'Analyze codebases with AI-powered insights',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-dark-bg text-dark-text antialiased">
        {children}
      </body>
    </html>
  )
}
EOF
echo -e "${GREEN}✓ layout.tsx created (dark theme)${NC}"

# src/app/page.tsx (Login Page - Dark Theme)
cat > src/app/page.tsx << 'EOF'
'use client';

import { useSearchParams } from 'next/navigation';
import { AlertCircle, LogIn } from 'lucide-react';

export default function HomePage() {
  const searchParams = useSearchParams();
  const error = searchParams?.get('error');

  const handleLogin = () => {
    window.location.href = '/api/auth/oauth';
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-dark-bg via-slate-900 to-dark-card">
      <div className="bg-dark-card rounded-xl shadow-2xl p-8 max-w-md w-full border border-dark-border">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <div className="inline-block p-3 bg-primary/10 rounded-full mb-4">
            <svg className="w-12 h-12 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-dark-text mb-2">
            Para Group Web UI
          </h1>
          <p className="text-dark-textMuted">
            Analyze codebases with AI-powered insights
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-error/10 border border-error/30 rounded-lg p-4 mb-6 flex items-start">
            <AlertCircle className="text-error mr-3 mt-0.5 flex-shrink-0" size={20} />
            <div>
              <p className="text-error font-medium">Authentication Error</p>
              <p className="text-error/80 text-sm mt-1">
                {error === 'oauth_failed' && 'OAuth authentication failed'}
                {error === 'no_code' && 'No authorization code received'}
                {error === 'authentication_failed' && 'Authentication process failed'}
              </p>
            </div>
          </div>
        )}

        {/* Login Button */}
        <button
          onClick={handleLogin}
          className="w-full bg-primary hover:bg-primary-dark text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center gap-3 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="currentColor"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="currentColor"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="currentColor"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Sign in with Google
        </button>

        {/* Info Text */}
        <div className="mt-6 text-center text-sm text-dark-textMuted space-y-2">
          <p>
            You'll be asked to verify your Claude API key after login.
          </p>
          <p className="flex items-center justify-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Your API key is encrypted and never shared.
          </p>
        </div>
      </div>
    </div>
  );
}
EOF
echo -e "${GREEN}✓ page.tsx (login) created (dark theme)${NC}"

# src/app/dashboard/page.tsx (Dashboard Page - Dark Theme)
cat > src/app/dashboard/page.tsx << 'EOF'
'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Loader2, FolderOpen, MessageSquare, LogOut, User, Sparkles } from 'lucide-react';

interface User {
  email: string;
  name: string;
  verified: boolean;
}

interface AnalysisResult {
  summary: string;
  files: Array<{ name: string; path: string; size: number }>;
  timestamp: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const step = searchParams?.get('step');

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [folderPath, setFolderPath] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [showApiKeyForm, setShowApiKeyForm] = useState(false);

  useEffect(() => {
    fetchUser();
  }, []);

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

  const handleAnalyze = async () => {
    if (!folderPath || !query) return;
    setAnalyzing(true);
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folderPath, query }),
      });
      if (!response.ok) throw new Error('Analysis failed');
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setAnalyzing(false);
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
      {/* Header */}
      <header className="bg-dark-card border-b border-dark-border shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <Sparkles className="text-primary" size={28} />
              <h1 className="text-2xl font-bold text-dark-text">
                Para Group Dashboard
              </h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-dark-textMuted">
                <User size={18} />
                <span className="text-sm">{user?.name}</span>
              </div>
              <button
                onClick={() => router.push('/api/auth/logout')}
                className="flex items-center gap-2 text-error hover:text-error/80 transition-colors"
              >
                <LogOut size={18} />
                <span className="text-sm">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel: Input */}
          <div className="space-y-6">
            {/* Folder Path Input */}
            <div className="bg-dark-card rounded-xl shadow-lg p-6 border border-dark-border">
              <label className="flex items-center gap-2 text-sm font-medium text-dark-text mb-3">
                <FolderOpen size={18} className="text-primary" />
                Folder Path
              </label>
              <input
                type="text"
                value={folderPath}
                onChange={(e) => setFolderPath(e.target.value)}
                placeholder="/path/to/your/project"
                className="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-dark-text placeholder-dark-textDim"
              />
              <p className="mt-2 text-sm text-dark-textMuted">
                Enter the absolute path to the folder you want to analyze
              </p>
            </div>

            {/* Query Input */}
            <div className="bg-dark-card rounded-xl shadow-lg p-6 border border-dark-border">
              <label className="flex items-center gap-2 text-sm font-medium text-dark-text mb-3">
                <MessageSquare size={18} className="text-primary" />
                Query
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="What would you like to know about this codebase?"
                rows={6}
                disabled={analyzing}
                className="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-dark-text placeholder-dark-textDim resize-none"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && e.metaKey) {
                    handleAnalyze();
                  }
                }}
              />
              <p className="mt-2 text-sm text-dark-textMuted">
                Press ⌘+Enter to submit
              </p>
            </div>

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={analyzing || !folderPath || !query}
              className="w-full bg-primary hover:bg-primary-dark disabled:bg-dark-hover disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl"
            >
              {analyzing ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles size={20} />
                  Analyze Code
                </>
              )}
            </button>
          </div>

          {/* Right Panel: Results */}
          <div>
            {results ? (
              <div className="bg-dark-card rounded-xl shadow-lg p-6 border border-dark-border">
                <div className="flex items-center gap-2 mb-4">
                  <svg className="w-6 h-6 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <h2 className="text-xl font-bold text-dark-text">Analysis Complete</h2>
                </div>

                {/* Summary */}
                <div className="mb-6">
                  <h3 className="text-sm font-medium text-dark-text mb-2">Summary</h3>
                  <div className="bg-dark-bg rounded-lg p-4 max-h-96 overflow-y-auto border border-dark-border">
                    <p className="text-dark-textMuted whitespace-pre-wrap">{results.summary}</p>
                  </div>
                  <p className="mt-2 text-xs text-dark-textDim">
                    Generated at: {new Date(results.timestamp).toLocaleString()}
                  </p>
                </div>

                {/* Files */}
                <div>
                  <h3 className="text-sm font-medium text-dark-text mb-2">
                    Output Files ({results.files.length})
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
                          onClick={() => window.location.href = `/api/results/${encodeURIComponent(file.path)}`}
                          className="text-primary hover:text-primary-light p-2 rounded-lg hover:bg-dark-hover transition-all"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                          </svg>
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-dark-card rounded-xl shadow-lg p-8 text-center border border-dark-border">
                <div className="inline-block p-4 bg-dark-bg rounded-full mb-4">
                  <Sparkles className="text-primary" size={32} />
                </div>
                <p className="text-dark-textMuted">
                  Enter a folder path and query to get started
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
EOF
echo -e "${GREEN}✓ dashboard/page.tsx created (dark theme)${NC}"

################################################################################
# SUMMARY
################################################################################

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ DARK THEME APPLIED SUCCESSFULLY${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Applied dark theme to:"
echo "  ✓ Root layout (layout.tsx)"
echo "  ✓ Login page (page.tsx)"
echo "  ✓ Dashboard page (dashboard/page.tsx)"
echo ""
echo -e "${YELLOW}Color scheme:${NC}"
echo "  Background: Very dark blue-gray (#0f172a)"
echo "  Cards: Dark slate (#1e293b)"
echo "  Text: Light gray (#e2e8f0)"
echo "  Primary: Soft blue (#3b82f6)"
echo "  Accents: Soft purple (#8b5cf6)"
echo ""
echo -e "${BLUE}Benefits:${NC}"
echo "  ✓ Easy on the eyes"
echo "  ✓ Reduced eye strain"
echo "  ✓ Better for long coding sessions"
echo "  ✓ Modern dark mode aesthetics"
echo ""
