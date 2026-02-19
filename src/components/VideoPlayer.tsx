import { useState, useRef, useEffect } from 'react'
import { Download, ChevronDown } from 'lucide-react'

interface VideoPlayerProps {
  src: string
  alembicSrc?: string
}

export function VideoPlayer({ src, alembicSrc }: VideoPlayerProps) {
  const [showExportMenu, setShowExportMenu] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowExportMenu(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleExportMp4 = () => {
    const link = document.createElement('a')
    link.href = src
    link.download = 'simulation.mp4'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    setShowExportMenu(false)
  }

  const handleExportAlembic = () => {
    if (alembicSrc) {
      const link = document.createElement('a')
      link.href = alembicSrc
      link.download = 'simulation.abc'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
    setShowExportMenu(false)
  }

  return (
    <div className="space-y-3">
      <div className="rounded-xl overflow-hidden shadow-lg border border-physica-200 bg-black">
        <video
          src={src}
          controls
          className="w-full aspect-video"
          playsInline
        >
          Your browser does not support the video tag.
        </video>
      </div>

      {/* Export Button */}
      <div className="relative" ref={menuRef}>
        <button
          onClick={() => setShowExportMenu(!showExportMenu)}
          className="flex items-center gap-2 px-4 py-2 bg-physica-500 hover:bg-physica-600 text-white rounded-lg transition-colors text-base font-medium"
        >
          <Download className="w-5 h-5" />
          Export
          <ChevronDown className={`w-4 h-4 transition-transform ${showExportMenu ? 'rotate-180' : ''}`} />
        </button>

        {/* Dropdown Menu */}
        {showExportMenu && (
          <div className="absolute top-full left-0 mt-2 bg-white rounded-lg shadow-lg border border-physica-200 overflow-hidden z-20 min-w-[180px]">
            <button
              onClick={handleExportMp4}
              className="w-full px-4 py-3 text-left text-base hover:bg-physica-50 transition-colors flex items-center gap-3"
            >
              <span className="w-8 h-8 bg-physica-100 rounded flex items-center justify-center text-xs font-bold text-physica-600">
                MP4
              </span>
              <span>Original Video</span>
            </button>
            <button
              onClick={handleExportAlembic}
              disabled={!alembicSrc}
              className="w-full px-4 py-3 text-left text-base hover:bg-physica-50 transition-colors flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span className="w-8 h-8 bg-physica-100 rounded flex items-center justify-center text-xs font-bold text-physica-600">
                ABC
              </span>
              <span>Alembic File</span>
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
