'use client'

import { useState, useMemo, useEffect } from 'react'
import ClauseItem from './ClauseItem'

interface Clause {
  clause_text: string
  clause_index: number
  risk_label: string
  risk_score: number
  explanation: string
  suggested_mitigation: string
}

interface ClauseListProps {
  clauses: Clause[]
  riskFilter?: 'ALL' | 'HIGH' | 'MEDIUM' | 'LOW'
}

export default function ClauseList({ clauses, riskFilter = 'ALL' }: ClauseListProps) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const clausesPerPage = 5

  // Filter clauses by risk type
  const filteredClauses = useMemo(() => {
    if (riskFilter === 'ALL') return clauses
    return clauses.filter(c => c.risk_label === riskFilter)
  }, [clauses, riskFilter])

  // Pagination
  const totalPages = Math.ceil(filteredClauses.length / clausesPerPage)
  const startIndex = (currentPage - 1) * clausesPerPage
  const endIndex = startIndex + clausesPerPage
  const currentClauses = filteredClauses.slice(startIndex, endIndex)

  // Reset to page 1 when filter changes
  useEffect(() => {
    setCurrentPage(1)
  }, [riskFilter])

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-100 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Clauses</h2>
        <span className="text-sm text-gray-600 dark:text-gray-400">
          Showing {startIndex + 1}-{Math.min(endIndex, filteredClauses.length)} of {filteredClauses.length}
        </span>
      </div>
      
      <div className="space-y-4">
        {currentClauses.length > 0 ? (
          currentClauses.map((clause, index) => {
            const originalIndex = clauses.findIndex(c => c.clause_index === clause.clause_index)
            return (
              <ClauseItem
                key={clause.clause_index}
                clause={clause}
                isSelected={selectedIndex === originalIndex}
                onSelect={() => setSelectedIndex(selectedIndex === originalIndex ? null : originalIndex)}
              />
            )
          })
        ) : (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            No clauses found for the selected filter.
          </div>
        )}
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="mt-6 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 pt-4">
          <button
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold"
          >
            ← Previous
          </button>
          
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Page {currentPage} of {totalPages}
            </span>
          </div>
          
          <button
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  )
}

