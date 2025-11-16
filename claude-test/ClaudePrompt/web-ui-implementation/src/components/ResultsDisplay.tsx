'use client';

import { useState } from 'react';

interface ResultsDisplayProps {
  results: {
    summary: string;
    fullAnalysis?: string;
    files: Array<{ name: string; fileId: string; size: number }>;
    timestamp: string;
    confidence?: number;
    guardrailsStatus?: string;
  };
}

export function ResultsDisplay({ results }: ResultsDisplayProps) {
  const [previewFileId, setPreviewFileId] = useState<string | null>(null);
  const [previewContent, setPreviewContent] = useState<string>('');
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const formatDate = (iso: string) => {
    return new Date(iso).toLocaleString();
  };

  const handlePreview = async (fileId: string) => {
    setIsLoadingPreview(true);
    try {
      const response = await fetch(`/api/file/preview?id=${fileId}`);
      if (!response.ok) throw new Error('Preview failed');
      const data = await response.json();
      setPreviewContent(data.content);
      setPreviewFileId(fileId);
    } catch (error) {
      alert('Failed to preview file');
    } finally {
      setIsLoadingPreview(false);
    }
  };

  const handleDownload = async (fileId: string, fileName: string) => {
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

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="mb-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Analysis Results</h2>
            <p className="text-sm text-gray-500 mt-1">
              Completed at {formatDate(results.timestamp)}
            </p>
          </div>
          <div className="flex gap-3">
            {results.confidence !== undefined && (
              <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                results.confidence >= 99
                  ? 'bg-green-100 text-green-800'
                  : results.confidence >= 95
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                ✓ {results.confidence}% Confidence
              </span>
            )}
            {results.guardrailsStatus && (
              <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                🛡️ {results.guardrailsStatus}
              </span>
            )}
          </div>
        </div>
        {results.confidence !== undefined && results.confidence >= 99 && (
          <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800">
              <strong>ULTRATHINK Framework:</strong> This analysis passed all 8 guardrail layers with {results.confidence}% confidence.
              Results are production-ready and validated.
            </p>
          </div>
        )}
      </div>

      <div className="space-y-6">
        {/* Summary Section */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-3">Summary</h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
              {results.summary}
            </pre>
          </div>
        </div>

        {/* Files Section */}
        {results.files && results.files.length > 0 && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">
              Output Files ({results.files.length})
            </h3>
            <div className="space-y-2">
              {results.files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {/* SECURITY: Never expose file paths - show generic description */}
                      Analysis results - Click to preview or download
                    </p>
                  </div>
                  <div className="ml-4 flex-shrink-0 flex gap-2 items-center">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {formatFileSize(file.size)}
                    </span>
                    <button
                      onClick={() => handlePreview(file.fileId)}
                      disabled={isLoadingPreview}
                      className="px-3 py-1 bg-indigo-600 text-white text-xs rounded-md hover:bg-indigo-700 disabled:bg-gray-400 transition-colors"
                    >
                      {isLoadingPreview ? 'Loading...' : 'Preview'}
                    </button>
                    <button
                      onClick={() => handleDownload(file.fileId, file.name)}
                      className="px-3 py-1 bg-green-600 text-white text-xs rounded-md hover:bg-green-700 transition-colors"
                    >
                      Download
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Preview Modal */}
        {previewFileId && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[80vh] flex flex-col">
              <div className="p-4 border-b border-gray-200 flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">File Preview</h3>
                <button
                  onClick={() => setPreviewFileId(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              <div className="flex-1 overflow-auto p-4">
                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                  {previewContent}
                </pre>
              </div>
            </div>
          </div>
        )}

        {/* Download All Button */}
        <div className="pt-4 border-t border-gray-200">
          <button
            onClick={() => {
              // Copy summary to clipboard
              navigator.clipboard.writeText(results.summary);
              alert('Summary copied to clipboard!');
            }}
            className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors font-medium"
          >
            Copy Summary to Clipboard
          </button>
        </div>
      </div>
    </div>
  );
}
