import { useState, useRef, useEffect } from 'react'
import { Header, ChatMessage, ChatInput } from './components'
import type { Message } from './types'

// Path to your local flood simulation video
// Place your video in the public folder and update this path
const FLOOD_SIMULATION_VIDEO = '/videos/flood-simulation.mp4'

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m Physica, your AI physics simulation engine. I can generate videos that accurately follow the laws of physics. What simulation would you like to see today?',
      timestamp: new Date(),
    },
  ])
  const [isProcessing, setIsProcessing] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsProcessing(true)

    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Check if the user is asking for a flood simulation
    const isFloodRequest = content.toLowerCase().includes('flood')

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: isFloodRequest
        ? 'I\'ve generated a flood simulation for you. This video demonstrates realistic water dynamics, including fluid flow, wave propagation, and interaction with terrain surfaces - all following accurate physics principles.'
        : 'I can help you generate physics-accurate simulations. Try asking me to create a flood simulation, and I\'ll show you realistic water dynamics in action!',
      videoUrl: isFloodRequest ? FLOOD_SIMULATION_VIDEO : undefined,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, assistantMessage])
    setIsProcessing(false)
  }

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Header />

      {/* Curvy lines background - lower half only */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <svg
          className="absolute bottom-0 left-0 right-0 w-full h-1/2"
          viewBox="0 0 1000 500"
          preserveAspectRatio="xMidYMax slice"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Densely packed flowing curved lines */}
          <g fill="none" strokeLinecap="round">
            {/* Row 1 - Bottom */}
            <path d="M-100,490 Q150,470 300,485 T600,465 T900,490 T1200,470" stroke="#93bdd0" strokeWidth="2" opacity="0.5" />
            <path d="M-100,480 Q200,455 350,475 T650,450 T950,480 T1200,455" stroke="#a5c9db" strokeWidth="1.5" opacity="0.45" />
            <path d="M-100,470 Q180,445 320,465 T620,440 T920,470 T1200,445" stroke="#7fb1c5" strokeWidth="2" opacity="0.4" />
            <path d="M-100,458 Q220,430 380,455 T680,425 T980,458 T1200,430" stroke="#6ba5ba" strokeWidth="1.5" opacity="0.35" />

            {/* Row 2 */}
            <path d="M-100,440 Q100,415 250,435 T550,405 T850,440 T1200,410" stroke="#b8d4e3" strokeWidth="2" opacity="0.5" />
            <path d="M-100,428 Q150,400 300,425 T600,395 T900,428 T1200,400" stroke="#a5c9db" strokeWidth="1.5" opacity="0.45" />
            <path d="M-100,415 Q200,385 350,410 T650,380 T950,415 T1200,385" stroke="#93bdd0" strokeWidth="2" opacity="0.4" />
            <path d="M-100,400 Q180,370 330,395 T630,365 T930,400 T1200,370" stroke="#7fb1c5" strokeWidth="1.5" opacity="0.35" />

            {/* Row 3 */}
            <path d="M-100,380 Q120,350 280,375 T580,345 T880,380 T1200,350" stroke="#c5dce8" strokeWidth="2" opacity="0.45" />
            <path d="M-100,365 Q180,335 340,360 T640,330 T940,365 T1200,335" stroke="#b8d4e3" strokeWidth="1.5" opacity="0.4" />
            <path d="M-100,350 Q150,320 310,345 T610,315 T910,350 T1200,320" stroke="#a5c9db" strokeWidth="2" opacity="0.35" />
            <path d="M-100,335 Q200,305 360,330 T660,300 T960,335 T1200,305" stroke="#93bdd0" strokeWidth="1.5" opacity="0.3" />

            {/* Row 4 */}
            <path d="M-100,315 Q100,285 260,310 T560,280 T860,315 T1200,285" stroke="#d2e4ed" strokeWidth="2" opacity="0.4" />
            <path d="M-100,300 Q160,270 320,295 T620,265 T920,300 T1200,270" stroke="#c5dce8" strokeWidth="1.5" opacity="0.35" />
            <path d="M-100,285 Q140,255 300,280 T600,250 T900,285 T1200,255" stroke="#b8d4e3" strokeWidth="2" opacity="0.3" />
            <path d="M-100,270 Q180,240 340,265 T640,235 T940,270 T1200,240" stroke="#a5c9db" strokeWidth="1.5" opacity="0.25" />

            {/* Row 5 */}
            <path d="M-100,250 Q80,220 240,245 T540,215 T840,250 T1200,220" stroke="#dceaf1" strokeWidth="2" opacity="0.35" />
            <path d="M-100,235 Q130,205 290,230 T590,200 T890,235 T1200,205" stroke="#d2e4ed" strokeWidth="1.5" opacity="0.3" />
            <path d="M-100,220 Q110,190 270,215 T570,185 T870,220 T1200,190" stroke="#c5dce8" strokeWidth="2" opacity="0.25" />
            <path d="M-100,205 Q150,175 310,200 T610,170 T910,205 T1200,175" stroke="#b8d4e3" strokeWidth="1.5" opacity="0.2" />

            {/* Row 6 - Top */}
            <path d="M-100,185 Q100,155 260,180 T560,150 T860,185 T1200,155" stroke="#dceaf1" strokeWidth="2" opacity="0.3" />
            <path d="M-100,170 Q140,140 300,165 T600,135 T900,170 T1200,140" stroke="#d2e4ed" strokeWidth="1.5" opacity="0.25" />
            <path d="M-100,155 Q120,125 280,150 T580,120 T880,155 T1200,125" stroke="#c5dce8" strokeWidth="2" opacity="0.2" />
            <path d="M-100,140 Q160,110 320,135 T620,105 T920,140 T1200,110" stroke="#b8d4e3" strokeWidth="1.5" opacity="0.15" />

            {/* Row 7 - Very top, fading out */}
            <path d="M-100,120 Q100,90 260,115 T560,85 T860,120 T1200,90" stroke="#dceaf1" strokeWidth="1.5" opacity="0.2" />
            <path d="M-100,105 Q130,75 290,100 T590,70 T890,105 T1200,75" stroke="#e5eff4" strokeWidth="1.5" opacity="0.15" />
            <path d="M-100,90 Q110,60 270,85 T570,55 T870,90 T1200,60" stroke="#e5eff4" strokeWidth="1.5" opacity="0.1" />
          </g>
        </svg>
      </div>

      {/* Chat container */}
      <main className="flex-1 flex flex-col max-w-3xl mx-auto w-full px-4 py-6 relative z-10">
        {/* Messages area */}
        <div className="flex-1 overflow-y-auto chat-scrollbar space-y-6 pb-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {isProcessing && (
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-10 h-10 bg-physica-100 rounded-full flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-physica-500 border-t-transparent rounded-full animate-spin" />
              </div>
              <div className="bg-physica-100 text-black rounded-2xl rounded-bl-md px-4 py-3">
                <p className="text-base text-physica-600">Generating physics simulation...</p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div className="pt-4 border-t border-physica-100">
          <ChatInput onSend={handleSendMessage} disabled={isProcessing} />
        </div>
      </main>
    </div>
  )
}

export default App
