'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { AlertCircle, LogIn, Loader2 } from 'lucide-react';

function HomePageContent() {
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

export default function HomePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-dark-bg via-slate-900 to-dark-card">
        <div className="text-center">
          <Loader2 className="animate-spin text-primary mx-auto mb-4" size={48} />
          <p className="text-dark-textMuted">Loading...</p>
        </div>
      </div>
    }>
      <HomePageContent />
    </Suspense>
  );
}
