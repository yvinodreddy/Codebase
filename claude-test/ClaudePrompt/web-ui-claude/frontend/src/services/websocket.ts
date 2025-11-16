import { io, Socket } from 'socket.io-client'
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
