'use client'

import { useState } from 'react'

interface DateRangeFilterProps {
  onDateRangeChange: (startDate: Date | null, endDate: Date | null) => void
}

export default function DateRangeFilter({ onDateRangeChange }: DateRangeFilterProps) {
  const [selectedRange, setSelectedRange] = useState<'all' | 'today' | 'week' | 'month' | 'year' | 'custom'>('all')
  const [customStart, setCustomStart] = useState('')
  const [customEnd, setCustomEnd] = useState('')

  const handleQuickFilter = (range: 'all' | 'today' | 'week' | 'month' | 'year') => {
    setSelectedRange(range)
    setCustomStart('')
    setCustomEnd('')

    const now = new Date()
    let start: Date | null = null
    let end: Date | null = null

    switch (range) {
      case 'today':
        start = new Date(now.getFullYear(), now.getMonth(), now.getDate())
        end = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59)
        break
      case 'week':
        start = new Date(now)
        start.setDate(now.getDate() - 7)
        end = now
        break
      case 'month':
        start = new Date(now.getFullYear(), now.getMonth(), 1)
        end = now
        break
      case 'year':
        start = new Date(now.getFullYear(), 0, 1)
        end = now
        break
      case 'all':
      default:
        start = null
        end = null
    }

    onDateRangeChange(start, end)
  }

  const handleCustomDateChange = () => {
    if (customStart && customEnd) {
      setSelectedRange('custom')
      const start = new Date(customStart)
      start.setHours(0, 0, 0, 0)
      const end = new Date(customEnd)
      end.setHours(23, 59, 59, 999)
      onDateRangeChange(start, end)
    }
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => handleQuickFilter('all')}
          className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
            selectedRange === 'all'
              ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
              : 'bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-blue-400'
          }`}
        >
          All Time
        </button>
        <button
          onClick={() => handleQuickFilter('today')}
          className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
            selectedRange === 'today'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-blue-400'
          }`}
        >
          Today
        </button>
        <button
          onClick={() => handleQuickFilter('week')}
          className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
            selectedRange === 'week'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-blue-400'
          }`}
        >
          Last 7 Days
        </button>
        <button
          onClick={() => handleQuickFilter('month')}
          className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
            selectedRange === 'month'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-blue-400'
          }`}
        >
          This Month
        </button>
        <button
          onClick={() => handleQuickFilter('year')}
          className={`px-4 py-2 rounded-lg font-semibold text-sm transition-all ${
            selectedRange === 'year'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-blue-400'
          }`}
        >
          This Year
        </button>
      </div>
      
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Custom Range:</span>
        <input
          type="date"
          value={customStart}
          onChange={(e) => {
            setCustomStart(e.target.value)
            if (e.target.value && customEnd) {
              setSelectedRange('custom')
              handleCustomDateChange()
            }
          }}
          className="px-3 py-2 border-2 border-gray-300 dark:border-gray-700 dark:bg-gray-800 dark:text-white rounded-lg focus:border-blue-500 focus:outline-none text-sm"
        />
        <span className="text-gray-500 dark:text-gray-400">to</span>
        <input
          type="date"
          value={customEnd}
          onChange={(e) => {
            setCustomEnd(e.target.value)
            if (customStart && e.target.value) {
              setSelectedRange('custom')
              handleCustomDateChange()
            }
          }}
          className="px-3 py-2 border-2 border-gray-300 dark:border-gray-700 dark:bg-gray-800 dark:text-white rounded-lg focus:border-blue-500 focus:outline-none text-sm"
        />
        {(customStart || customEnd) && (
          <button
            onClick={() => {
              setCustomStart('')
              setCustomEnd('')
              setSelectedRange('all')
              onDateRangeChange(null, null)
            }}
            className="px-3 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors text-sm"
          >
            Clear
          </button>
        )}
      </div>
    </div>
  )
}

