export interface User {
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
