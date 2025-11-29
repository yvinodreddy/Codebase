'use client';

import { useState } from 'react';
import { ApiKeySetup } from './ApiKeySetup';

export function LoginPrompt() {
  const [showApiKeyMode, setShowApiKeyMode] = useState(false);

  const handleGoogleLogin = () => {
    window.location.href = '/api/auth/oauth';
  };

  const handleApiKeySuccess = () => {
    window.location.reload();
  };

  if (showApiKeyMode) {
    return (
      <div>
        <button
          onClick={() => setShowApiKeyMode(false)}
          className="mb-4 text-blue-600 hover:text-blue-700 flex items-center gap-2"
        >
          ← Back to login options
        </button>
        <ApiKeySetup onSuccess={handleApiKeySuccess} />
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">🔐</div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Choose How to Sign In
        </h2>
        <p className="text-gray-600">
          Select your preferred authentication method
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Google OAuth Option */}
        <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-blue-200 hover:border-blue-400 transition-all">
          <div className="text-center mb-4">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg className="w-8 h-8" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Google Account
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Quick & easy - use your Google login
            </p>
          </div>

          <ul className="text-sm text-gray-700 space-y-2 mb-6">
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>One-click authentication</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>Uses your Claude subscription</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>No API keys to manage</span>
            </li>
          </ul>

          <button
            onClick={handleGoogleLogin}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Continue with Google
          </button>
        </div>

        {/* API Key Option */}
        <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-gray-200 hover:border-gray-400 transition-all">
          <div className="text-center mb-4">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-3xl">🔑</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              API Key
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Use your own Claude API key directly
            </p>
          </div>

          <ul className="text-sm text-gray-700 space-y-2 mb-6">
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>Full control over API usage</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>Works without Google account</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>Stored securely in session</span>
            </li>
          </ul>

          <button
            onClick={() => setShowApiKeyMode(true)}
            className="w-full bg-gray-600 text-white py-3 px-6 rounded-lg hover:bg-gray-700 transition-colors font-medium"
          >
            Enter API Key
          </button>
        </div>
      </div>

      <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
        <div className="flex items-start gap-4">
          <div className="text-3xl">💡</div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 mb-2">Which should I choose?</h3>
            <div className="space-y-2 text-sm text-gray-700">
              <p><strong>Google OAuth:</strong> Best for most users. Quick setup, automatic Claude Max subscription integration.</p>
              <p><strong>API Key:</strong> For advanced users who want direct control or have custom API configurations.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
