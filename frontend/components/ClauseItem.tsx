'use client'

import RiskBadge from './RiskBadge'
import ClauseRewriter from './ClauseRewriter'

interface Clause {
  clause_text: string
  clause_index: number
  risk_label: string
  risk_score: number
  explanation: string
  suggested_mitigation: string
}

interface ClauseItemProps {
  clause: Clause
  isSelected: boolean
  onSelect: () => void
}

export default function ClauseItem({ clause, isSelected, onSelect }: ClauseItemProps) {
  const getRiskColor = (label: string) => {
    switch (label) {
      case 'HIGH':
        return 'border-red-500 dark:border-red-500 bg-red-50 dark:bg-red-900/20'
      case 'MEDIUM':
        return 'border-yellow-500 dark:border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20'
      case 'LOW':
        return 'border-green-500 dark:border-green-500 bg-green-50 dark:bg-green-900/20'
      default:
        return 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700'
    }
  }

  return (
    <div
      className={`border-2 rounded-xl p-5 cursor-pointer transition-all shadow-md hover:shadow-lg ${
        isSelected 
          ? `${getRiskColor(clause.risk_label)} shadow-xl` 
          : 'border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-500 bg-white dark:bg-gray-800'
      }`}
      onClick={onSelect}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-sm ${
            clause.risk_label === 'HIGH' ? 'bg-red-500' :
            clause.risk_label === 'MEDIUM' ? 'bg-yellow-500' : 'bg-green-500'
          }`}>
            {clause.clause_index + 1}
          </div>
          <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Clause {clause.clause_index + 1}</span>
        </div>
        <RiskBadge score={clause.risk_score} label={clause.risk_label} />
      </div>
      <p className="text-gray-900 dark:text-gray-100 mb-3 leading-relaxed text-base font-normal">{clause.clause_text}</p>
      {isSelected && (
        <div className="mt-4 pt-4 border-t-2 border-gray-300 dark:border-gray-600 space-y-4 animate-fadeIn">
          <div className="bg-white dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
            <h4 className="font-bold text-sm text-gray-900 dark:text-white mb-2 flex items-center gap-2">
              <span>💡</span> Explanation
            </h4>
            <p className="text-sm text-gray-900 dark:text-gray-100 leading-relaxed">{clause.explanation}</p>
          </div>
          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
            <h4 className="font-bold text-sm text-blue-900 dark:text-blue-100 mb-2 flex items-center gap-2">
              <span>🛡️</span> Suggested Mitigation
            </h4>
            <p className="text-sm text-blue-900 dark:text-blue-100 leading-relaxed font-medium">{clause.suggested_mitigation}</p>
          </div>
          {clause.risk_label === 'HIGH' && (
            <ClauseRewriter 
              originalClause={clause.clause_text} 
              riskLabel={clause.risk_label}
            />
          )}
        </div>
      )}
    </div>
  )
}

