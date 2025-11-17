'use client'

import { useEffect, useState } from 'react'

export default function KeyboardShortcuts() {
  const [showHelp, setShowHelp] = useState(false)

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Ctrl/Cmd + K to toggle help
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault()
        setShowHelp(!showHelp)
      }
      // Escape to close
      if (e.key === 'Escape' && showHelp) {
        setShowHelp(false)
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [showHelp])

  if (!showHelp) return null

  return (
    <div className="fixed inset-0 bg-black/50 dark:bg-black/70 z-50 flex items-center justify-center p-4" onClick={() => setShowHelp(false)}>
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full p-6" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Keyboard Shortcuts</h2>
          <button
            onClick={() => setShowHelp(false)}
            className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
          >
            ✕
          </button>
        </div>
        <div className="space-y-4">
          {[
            { key: 'Ctrl/Cmd + K', desc: 'Show keyboard shortcuts' },
            { key: 'Esc', desc: 'Close dialogs/modals' },
            { key: '/', desc: 'Focus search (on history page)' },
            { key: 'Ctrl/Cmd + /', desc: 'Toggle dark mode' },
          ].map((shortcut, idx) => (
            <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <span className="text-gray-700 dark:text-gray-300">{shortcut.desc}</span>
              <kbd className="px-3 py-1 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded font-mono text-sm">
                {shortcut.key}
              </kbd>
            </div>
          ))}
        </div>
        <div className="mt-6 text-sm text-gray-500 dark:text-gray-400 text-center">
          Press <kbd className="px-2 py-1 bg-gray-200 dark:bg-gray-600 rounded">Esc</kbd> to close
        </div>
      </div>
    </div>
  )
}

