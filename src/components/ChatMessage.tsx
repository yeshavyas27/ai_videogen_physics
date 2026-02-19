import { User } from 'lucide-react'
import type { Message } from '../types'
import { VideoPlayer } from './VideoPlayer'

interface ChatMessageProps {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-10 h-10 bg-physica-100 rounded-full flex items-center justify-center">
          <User className="w-5 h-5 text-physica-500" />
        </div>
      )}
      <div className={`flex flex-col gap-2 max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-physica-500 text-white rounded-br-md'
              : 'bg-physica-100 text-black rounded-bl-md'
          }`}
        >
          <p className="text-base leading-relaxed whitespace-pre-wrap">{message.content}</p>
        </div>
        {message.videoUrl && (
          <div className="w-full max-w-md">
            <VideoPlayer src={message.videoUrl} alembicSrc={message.alembicUrl} />
          </div>
        )}
      </div>
    </div>
  )
}
