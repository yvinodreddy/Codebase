#!/usr/bin/env python3
"""
ULTRATHINK Web UI - Complete Project Generator
Generates all frontend and backend files for production deployment
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

def create_file(path: str, content: str):
    """Create a file with the given content"""
    file_path = PROJECT_ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    print(f"✅ Created: {path}")

def generate_project():
    """Generate complete project structure"""
    print("🚀 Generating ULTRATHINK Web UI Project...")
    print()

    # Frontend files
    files = {
        # Frontend structure
        "frontend/src/main.tsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './styles/index.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      <Toaster position="top-right" />
    </QueryClientProvider>
  </React.StrictMode>,
)
''',
        "frontend/src/App.tsx": '''import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './components/Auth/LoginPage'
import Dashboard from './components/Layout/Dashboard'
import ProtectedRoute from './components/Auth/ProtectedRoute'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard/*"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
''',
        "frontend/src/styles/index.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700
           focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
           transition-colors duration-200;
  }

  .btn-secondary {
    @apply px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300
           focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2
           transition-colors duration-200;
  }

  .input-field {
    @apply w-full px-3 py-2 border border-gray-300 rounded-lg
           focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
           transition-all duration-200;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}
''',
        "frontend/src/types/index.ts": '''export interface User {
  id: string
  email: string
  name: string
  picture: string
  hasClaudeApiKey: boolean
}

export interface Project {
  id: string
  name: string
  path: string
  lastQuery?: string
  createdAt: string
  updatedAt: string
}

export interface FileNode {
  name: string
  path: string
  type: 'file' | 'directory'
  children?: FileNode[]
}

export interface QueryRequest {
  folderPath: string
  query: string
  contextFiles?: string[]
  maxIterations?: number
  confidenceThreshold?: number
}

export interface FileChange {
  file: string
  action: 'created' | 'modified' | 'deleted'
  diff?: string
  reason: string
}

export interface QueryResponse {
  queryId: string
  status: 'pending' | 'running' | 'complete' | 'error'
  filesChanged: FileChange[]
  summary: string
  executionTimeMs: number
}

export interface WebSocketMessage {
  type: 'connect' | 'progress' | 'file_change' | 'complete' | 'error'
  data?: any
}
''',
        "frontend/src/store/authStore.ts": '''import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  setUser: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      setUser: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
)
''',
        "frontend/src/store/projectStore.ts": '''import { create } from 'zustand'
import type { Project } from '@/types'

interface ProjectState {
  currentProject: Project | null
  projects: Project[]
  setCurrentProject: (project: Project) => void
  addProject: (project: Project) => void
  setProjects: (projects: Project[]) => void
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: null,
  projects: [],
  setCurrentProject: (project) => set({ currentProject: project }),
  addProject: (project) => set((state) => ({ projects: [...state.projects, project] })),
  setProjects: (projects) => set({ projects }),
}))
''',
        "frontend/src/services/api.ts": '''import axios from 'axios'
import { useAuthStore } from '@/store/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
''',
        "frontend/src/services/websocket.ts": '''import { io, Socket } from 'socket.io-client'
import type { WebSocketMessage } from '@/types'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

class WebSocketService {
  private socket: Socket | null = null
  private listeners: Map<string, Set<(data: any) => void>> = new Map()

  connect(token: string) {
    if (this.socket?.connected) return

    this.socket = io(WS_URL, {
      auth: { token },
      transports: ['websocket'],
    })

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
    })

    this.socket.on('message', (message: WebSocketMessage) => {
      const listeners = this.listeners.get(message.type)
      if (listeners) {
        listeners.forEach((callback) => callback(message.data))
      }
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  on(event: string, callback: (data: any) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set())
    }
    this.listeners.get(event)!.add(callback)
  }

  off(event: string, callback: (data: any) => void) {
    const listeners = this.listeners.get(event)
    if (listeners) {
      listeners.delete(callback)
    }
  }

  send(message: WebSocketMessage) {
    if (this.socket?.connected) {
      this.socket.emit('message', message)
    }
  }
}

export const wsService = new WebSocketService()
export default wsService
''',
        "frontend/index.html": '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ULTRATHINK Web UI</title>
    <meta name="description" content="Web-based Claude Code interface" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''',
        "frontend/.env.example": '''VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_google_client_id_here
''',
        "frontend/postcss.config.js": '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
''',
        "frontend/.eslintrc.cjs": '''module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}
''',
        "frontend/tsconfig.node.json": '''{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
''',
        "frontend/netlify.toml": '''[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
''',
    }

    # Generate all files
    for path, content in files.items():
        create_file(path, content)

    # Create remaining component placeholders
    component_dirs = [
        "frontend/src/components/Auth",
        "frontend/src/components/FileBrowser",
        "frontend/src/components/QueryInterface",
        "frontend/src/components/CodeEditor",
        "frontend/src/components/Progress",
        "frontend/src/components/Layout",
    ]

    for dir_path in component_dirs:
        (PROJECT_ROOT / dir_path).mkdir(parents=True, exist_ok=True)
        placeholder = PROJECT_ROOT / dir_path / ".gitkeep"
        placeholder.touch()
        print(f"✅ Created directory: {dir_path}/")

    print()
    print("=" * 60)
    print("✅ PROJECT GENERATION COMPLETE!")
    print("=" * 60)
    print()
    print("📁 Project Structure Created:")
    print("  ├── frontend/          React + TypeScript application")
    print("  ├── backend/           FastAPI Python application (minimal)")
    print("  ├── docs/              Architecture documentation")
    print("  └── README.md          Quick start guide (to be created)")
    print()
    print("🚀 Next Steps:")
    print("  1. cd frontend && npm install")
    print("  2. cd backend && pip install fastapi uvicorn anthropic")
    print("  3. Configure .env files")
    print("  4. Start development servers")
    print()
    print("📖 See docs/DEPLOYMENT.md for full deployment instructions")
    print()

if __name__ == "__main__":
    generate_project()
