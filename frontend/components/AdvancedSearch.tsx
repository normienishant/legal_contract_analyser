'use client'

import { useState, useEffect } from 'react'

interface AdvancedSearchProps {
  onSearch: (query: string, searchIn: 'filename' | 'clause' | 'all') => void
  placeholder?: string
}

export default function AdvancedSearch({ onSearch, placeholder = "Search..." }: AdvancedSearchProps) {
  const [query, setQuery] = useState('')
  const [searchIn, setSearchIn] = useState<'filename' | 'clause' | 'all'>('all')
  const [isExpanded, setIsExpanded] = useState(false)

  useEffect(() => {
    // Debounce search
    const timer = setTimeout(() => {
      onSearch(query, searchIn)
    }, 300)

    return () => clearTimeout(timer)
  }, [query, searchIn, onSearch])

  return (
    <div className="space-y-2">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder={placeholder}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsExpanded(true)}
            className="w-full px-4 py-3 pl-10 border-2 border-gray-300 dark:border-[#262626] dark:bg-[#141414] dark:text-[#e5e5e5] rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
          />
          <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
            🔍
          </span>
          {query && (
            <button
              onClick={() => {
                setQuery('')
                onSearch('', searchIn)
              }}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              ✕
            </button>
          )}
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="px-4 py-3 bg-white dark:bg-[#141414] border-2 border-gray-300 dark:border-[#262626] text-gray-700 dark:text-[#e5e5e5] rounded-xl hover:border-blue-400 transition-colors font-semibold"
        >
          {isExpanded ? '▲' : '▼'} Advanced
        </button>
      </div>
      
      {isExpanded && (
        <div className="bg-white dark:bg-[#141414] border-2 border-gray-300 dark:border-[#262626] rounded-xl p-4 space-y-3 animate-fadeIn">
          <div>
            <label className="text-sm font-semibold text-gray-700 dark:text-[#e5e5e5] mb-2 block">
              Search In:
            </label>
            <div className="flex gap-2 flex-wrap">
              <button
                onClick={() => setSearchIn('all')}
                className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
                  searchIn === 'all'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-gray-100 dark:bg-[#262626] text-gray-700 dark:text-[#e5e5e5] hover:bg-gray-200 dark:hover:bg-[#404040]'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setSearchIn('filename')}
                className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
                  searchIn === 'filename'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-gray-100 dark:bg-[#262626] text-gray-700 dark:text-[#e5e5e5] hover:bg-gray-200 dark:hover:bg-[#404040]'
                }`}
              >
                Filename Only
              </button>
              <button
                onClick={() => setSearchIn('clause')}
                className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
                  searchIn === 'clause'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-gray-100 dark:bg-[#262626] text-gray-700 dark:text-[#e5e5e5] hover:bg-gray-200 dark:hover:bg-[#404040]'
                }`}
              >
                Clause Text
              </button>
            </div>
          </div>
          {query && (
            <div className="text-sm text-gray-600 dark:text-[#a3a3a3]">
              Searching for: <span className="font-semibold text-blue-600 dark:text-blue-400">&quot;{query}&quot;</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// Helper function to highlight search results
export function highlightText(text: string, query: string): string {
  if (!query) return text
  
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
  return text.replace(regex, '<mark class="bg-yellow-300 dark:bg-yellow-600 font-semibold">$1</mark>')
}

