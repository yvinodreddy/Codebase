module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Dark theme color palette (easy on the eyes)
        dark: {
          bg: '#0f172a',        // Very dark blue-gray (main background)
          card: '#1e293b',      // Dark card background
          hover: '#334155',     // Hover state
          border: '#475569',    // Borders
          text: '#e2e8f0',      // Main text (light gray)
          textMuted: '#94a3b8', // Muted text
          textDim: '#64748b',   // Dimmed text
        },
        primary: {
          DEFAULT: '#3b82f6',   // Blue (easier on eyes than bright blue)
          dark: '#2563eb',      // Darker blue
          light: '#60a5fa',     // Lighter blue
        },
        secondary: {
          DEFAULT: '#8b5cf6',   // Purple (softer than before)
          dark: '#7c3aed',      // Darker purple
          light: '#a78bfa',     // Lighter purple
        },
        success: '#10b981',     // Green
        warning: '#f59e0b',     // Orange
        error: '#ef4444',       // Red
        info: '#06b6d4',        // Cyan
      },
    },
  },
  plugins: [],
};
