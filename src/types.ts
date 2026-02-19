export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  videoUrl?: string
  alembicUrl?: string
  timestamp: Date
}
