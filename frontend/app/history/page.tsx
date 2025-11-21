'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import RiskBadge from '@/components/RiskBadge'
import DateRangeFilter from '@/components/DateRangeFilter'
import AdvancedSearch from '@/components/AdvancedSearch'
import { getHistory } from '@/lib/api'

interface HistoryItem {
  id: number
  filename: string
  original_filename: string
  global_risk_score: number
  total_clauses: number
  high_risk_count: number
  medium_risk_count: number
  low_risk_count: number
  created_at: string
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [filteredHistory, setFilteredHistory] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchIn, setSearchIn] = useState<'filename' | 'clause' | 'all'>('all')
  const [riskFilter, setRiskFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all')
  const [sortBy, setSortBy] = useState<'date' | 'risk' | 'name'>('date')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [dateRange, setDateRange] = useState<{ start: Date | null; end: Date | null }>({ start: null, end: null })

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        // Add timeout to prevent infinite loading
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 10000) // 10 second timeout
        
        const data = await getHistory()
        clearTimeout(timeoutId)
        setHistory(data || [])
        setFilteredHistory(data || [])
      } catch (err: any) {
        console.error('Failed to load history:', err)
        // If error, set empty array so empty state shows
        setHistory([])
        setFilteredHistory([])
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [])

  useEffect(() => {
    let filtered = history

    // Date range filter
    if (dateRange.start && dateRange.end) {
      filtered = filtered.filter(item => {
        const itemDate = new Date(item.created_at)
        return itemDate >= dateRange.start! && itemDate <= dateRange.end!
      })
    }

    // Search filter
    if (searchQuery) {
      const queryLower = searchQuery.toLowerCase()
      filtered = filtered.filter(item => {
        if (searchIn === 'filename' || searchIn === 'all') {
          if (item.original_filename.toLowerCase().includes(queryLower)) {
            return true
          }
        }
        // For clause search, we'd need to fetch clause data - for now, just filename
        // In a real implementation, you'd make an API call to search clauses
        return false
      })
    }

    // Risk filter
    if (riskFilter !== 'all') {
      filtered = filtered.filter(item => {
        if (riskFilter === 'high') return item.high_risk_count > 0
        if (riskFilter === 'medium') return item.medium_risk_count > 0
        if (riskFilter === 'low') return item.low_risk_count > 0
        return true
      })
    }

    // Sort
    filtered = [...filtered].sort((a, b) => {
      let comparison = 0
      if (sortBy === 'date') {
        comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      } else if (sortBy === 'risk') {
        comparison = a.global_risk_score - b.global_risk_score
      } else if (sortBy === 'name') {
        comparison = a.original_filename.localeCompare(b.original_filename)
      }
      return sortOrder === 'asc' ? comparison : -comparison
    })

    setFilteredHistory(filtered)
  }, [searchQuery, searchIn, riskFilter, sortBy, sortOrder, history, dateRange])

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:bg-[#0a0a0a]">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Analysis History
          </h1>
          <p className="text-gray-600 mb-6">View all your previous contract analyses</p>
          
          {/* Search and Filter */}
          <div className="space-y-4 mb-6">
            <AdvancedSearch
              onSearch={(query, searchIn) => {
                setSearchQuery(query)
                setSearchIn(searchIn)
              }}
              placeholder="Search by filename or clause text..."
            />
            
            <DateRangeFilter
              onDateRangeChange={(start, end) => {
                setDateRange({ start, end })
              }}
            />
            
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex gap-2">
              <button
                onClick={() => setRiskFilter('all')}
                className={`px-4 py-3 rounded-xl font-semibold transition-all ${
                  riskFilter === 'all'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                    : 'bg-white border-2 border-gray-300 text-gray-700 hover:border-blue-400'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setRiskFilter('high')}
                className={`px-4 py-3 rounded-xl font-semibold transition-all ${
                  riskFilter === 'high'
                    ? 'bg-red-600 text-white shadow-lg'
                    : 'bg-white border-2 border-gray-300 text-red-600 hover:border-red-400'
                }`}
              >
                High Risk
              </button>
              <button
                onClick={() => setRiskFilter('medium')}
                className={`px-4 py-3 rounded-xl font-semibold transition-all ${
                  riskFilter === 'medium'
                    ? 'bg-yellow-600 text-white shadow-lg'
                    : 'bg-white border-2 border-gray-300 text-yellow-600 hover:border-yellow-400'
                }`}
              >
                Medium
              </button>
              <button
                onClick={() => setRiskFilter('low')}
                className={`px-4 py-3 rounded-xl font-semibold transition-all ${
                  riskFilter === 'low'
                    ? 'bg-green-600 text-white shadow-lg'
                    : 'bg-white border-2 border-gray-300 text-green-600 hover:border-green-400'
                }`}
              >
                Low Risk
              </button>
            </div>
            </div>
            {/* Sort Options */}
            <div className="flex items-center gap-4 flex-wrap">
              <span className="text-sm font-semibold text-gray-700 dark:text-[#e5e5e5]">Sort by:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'date' | 'risk' | 'name')}
                className="px-4 py-2 border-2 border-gray-300 dark:border-[#262626] dark:bg-[#141414] dark:text-[#e5e5e5] rounded-lg focus:border-blue-500 focus:outline-none"
              >
                <option value="date">Date</option>
                <option value="risk">Risk Score</option>
                <option value="name">Filename</option>
              </select>
              <button
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="px-4 py-2 bg-white dark:bg-[#141414] border-2 border-gray-300 dark:border-[#262626] text-gray-700 dark:text-[#e5e5e5] rounded-lg hover:border-blue-400 transition-colors"
              >
                {sortOrder === 'asc' ? '↑ Ascending' : '↓ Descending'}
              </button>
            </div>
          </div>
        </div>
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-gray-600 dark:text-[#e5e5e5]">Loading history...</p>
          </div>
        ) : filteredHistory.length === 0 ? (
          <div className="text-center py-12 bg-white dark:bg-[#141414] rounded-2xl shadow-lg">
            <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-4xl">{history.length === 0 ? '📋' : '🔍'}</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-[#e5e5e5] mb-2">
              {history.length === 0 ? 'No Analysis History Yet' : 'No Results Found'}
            </h3>
            <p className="text-gray-600 dark:text-[#e5e5e5] mb-2">
              {history.length === 0 
                ? 'You haven\'t analyzed any contracts yet. Upload your first contract to get started!'
                : 'Try adjusting your search or filter criteria'}
            </p>
            {history.length === 0 && (
              <>
                <p className="text-sm text-gray-500 dark:text-[#a3a3a3] mb-6">
                  📄 Upload a PDF, DOCX, or TXT file to analyze it for risks
                </p>
                <Link
                  href="/upload"
                  className="inline-block bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl"
                >
                  📤 Upload Your First Document
                </Link>
              </>
            )}
          </div>
        ) : (
          <>
            <div className="mb-4 text-sm text-gray-600 dark:text-[#a3a3a3]">
              Showing {filteredHistory.length} of {history.length} analyses
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {filteredHistory.map((item) => (
              <Link
                key={item.id}
                href={`/analysis/${item.id}`}
                className="block bg-white dark:bg-[#141414] rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all transform hover:-translate-y-1 border border-gray-100 dark:border-[#262626]"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-[#e5e5e5] mb-2 line-clamp-1">{item.original_filename}</h3>
                    <p className="text-gray-500 dark:text-[#a3a3a3] text-sm mb-4">
                      {new Date(item.created_at).toLocaleString()}
                    </p>
                  </div>
                  <RiskBadge score={item.global_risk_score} />
                </div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="bg-gray-50 dark:bg-[#262626] rounded-lg p-3">
                    <div className="text-sm text-gray-600 dark:text-[#a3a3a3] mb-1">Total Clauses</div>
                    <div className="text-2xl font-bold text-gray-900 dark:text-[#e5e5e5]">{item.total_clauses}</div>
                  </div>
                  <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-3">
                    <div className="text-sm text-red-600 dark:text-red-400 mb-1">High Risk</div>
                    <div className="text-2xl font-bold text-red-900 dark:text-red-300">{item.high_risk_count}</div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <div className="flex-1 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-2 text-center">
                    <div className="text-xs text-yellow-600 dark:text-yellow-400 mb-1">Medium</div>
                    <div className="text-lg font-bold text-yellow-900 dark:text-yellow-300">{item.medium_risk_count}</div>
                  </div>
                  <div className="flex-1 bg-green-50 dark:bg-green-900/20 rounded-lg p-2 text-center">
                    <div className="text-xs text-green-600 dark:text-green-400 mb-1">Low</div>
                    <div className="text-lg font-bold text-green-900 dark:text-green-300">{item.low_risk_count}</div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  )
}

