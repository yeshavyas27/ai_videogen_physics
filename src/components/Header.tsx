import { MessageCircle } from 'lucide-react'

export function Header() {
  return (
    <header className="bg-white border-b border-physica-100 px-6 py-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-physica-500 rounded-full flex items-center justify-center">
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-semibold text-black">Physica</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <a href="#" className="text-gray-600 hover:text-black transition-colors">
              Home
            </a>
            <a href="#" className="text-gray-600 hover:text-black transition-colors">
              Features
            </a>
            <a href="#" className="text-gray-600 hover:text-black transition-colors">
              About
            </a>
          </nav>
        </div>
        <button className="bg-physica-500 hover:bg-physica-600 text-white px-5 py-2 rounded-full transition-colors font-medium">
          Sign Up
        </button>
      </div>
    </header>
  )
}
