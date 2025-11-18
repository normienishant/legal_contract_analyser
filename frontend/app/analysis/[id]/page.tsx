'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import ClauseList from '@/components/ClauseList'
import RiskBadge from '@/components/RiskBadge'
import ExportReport from '@/components/ExportReport'
import { getAnalysis } from '@/lib/api'

interface AnalysisData {
  analysis_id: number
  filename: string
  analysis: {
    global_risk_score: number
    total_clauses: number
    high_risk_count: number
    medium_risk_count: number
    low_risk_count: number
    clauses: Array<{
      clause_id?: number
      clause_text: string
      clause_index: number
      risk_label: string
      risk_score: number
      explanation: string
      suggested_mitigation: string
    }>
  }
  created_at: string
}

export default function AnalysisPage() {
  const params = useParams()
  const fileId = params.id as string
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [riskFilter, setRiskFilter] = useState<'ALL' | 'HIGH' | 'MEDIUM' | 'LOW'>('ALL')

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true)
        // First upload, then extract, then analyze
        // For now, we'll trigger the full pipeline
        const result = await getAnalysis(fileId)
        setAnalysis(result)
      } catch (err: any) {
        setError(err.message || 'Failed to load analysis')
      } finally {
        setLoading(false)
      }
    }

    if (fileId) {
      fetchAnalysis()
    }
  }, [fileId])

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-black dark:via-gray-950 dark:to-black">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300 text-lg">Loading analysis...</p>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  if (error || !analysis) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="text-center text-red-600 dark:text-red-400">{error || 'Analysis not found'}</div>
        </main>
        <Footer />
      </div>
    )
  }


  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
                {analysis.filename}
              </h1>
              <p className="text-gray-700 dark:text-gray-300">Analyzed on {new Date(analysis.created_at).toLocaleString()}</p>
            </div>
            <ExportReport 
              analysis={{
                ...analysis.analysis,
                filename: analysis.filename,
                created_at: analysis.created_at
              }} 
              analysisId={analysis.analysis_id} 
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-1 space-y-6">
            {/* Risk Filter Sidebar */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
              <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Filter by Risk</h2>
              <div className="space-y-2">
                <button
                  onClick={() => setRiskFilter('ALL')}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all font-semibold ${
                    riskFilter === 'ALL'
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  All Clauses ({analysis.analysis.total_clauses})
                </button>
                <button
                  onClick={() => setRiskFilter('HIGH')}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all font-semibold ${
                    riskFilter === 'HIGH'
                      ? 'bg-red-600 text-white shadow-lg'
                      : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-900/30'
                  }`}
                >
                  🔴 High Risk ({analysis.analysis.high_risk_count})
                </button>
                <button
                  onClick={() => setRiskFilter('MEDIUM')}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all font-semibold ${
                    riskFilter === 'MEDIUM'
                      ? 'bg-yellow-600 text-white shadow-lg'
                      : 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300 hover:bg-yellow-100 dark:hover:bg-yellow-900/30'
                  }`}
                >
                  🟡 Medium Risk ({analysis.analysis.medium_risk_count})
                </button>
                <button
                  onClick={() => setRiskFilter('LOW')}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-all font-semibold ${
                    riskFilter === 'LOW'
                      ? 'bg-green-600 text-white shadow-lg'
                      : 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 hover:bg-green-100 dark:hover:bg-green-900/30'
                  }`}
                >
                  🟢 Low Risk ({analysis.analysis.low_risk_count})
                </button>
              </div>
            </div>

            {/* Risk Summary Card */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
              <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Risk Summary</h2>
              <div className="mb-6">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-gray-700 dark:text-gray-300 font-medium">Global Risk Score</span>
                  <RiskBadge score={analysis.analysis.global_risk_score} />
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 mb-2">
                  <div
                    className={`h-4 rounded-full transition-all ${
                      analysis.analysis.global_risk_score >= 70
                        ? 'bg-gradient-to-r from-red-500 to-red-600'
                        : analysis.analysis.global_risk_score >= 40
                        ? 'bg-gradient-to-r from-yellow-500 to-yellow-600'
                        : 'bg-gradient-to-r from-green-500 to-green-600'
                    }`}
                    style={{ width: `${analysis.analysis.global_risk_score}%` }}
                  />
                </div>
                <p className="text-xs text-gray-600 dark:text-gray-400 text-right">{analysis.analysis.global_risk_score.toFixed(1)}/100</p>
              </div>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
                    <span className="text-gray-700 dark:text-gray-300 font-medium">Total Clauses</span>
                  </div>
                  <span className="font-bold text-gray-900 dark:text-white">{analysis.analysis.total_clauses}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span className="text-red-700 dark:text-red-300 font-medium">High Risk</span>
                  </div>
                  <span className="font-bold text-red-900 dark:text-red-300">{analysis.analysis.high_risk_count}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <span className="text-yellow-700 dark:text-yellow-300 font-medium">Medium Risk</span>
                  </div>
                  <span className="font-bold text-yellow-900 dark:text-yellow-300">{analysis.analysis.medium_risk_count}</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-700 dark:text-green-300 font-medium">Low Risk</span>
                  </div>
                  <span className="font-bold text-green-900 dark:text-green-300">{analysis.analysis.low_risk_count}</span>
                </div>
              </div>
            </div>

            {/* Risk Distribution Chart */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
              <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Risk Distribution</h3>
              <div className="space-y-3">
                {[
                  { label: 'High', count: analysis.analysis.high_risk_count, color: 'bg-red-500', total: analysis.analysis.total_clauses },
                  { label: 'Medium', count: analysis.analysis.medium_risk_count, color: 'bg-yellow-500', total: analysis.analysis.total_clauses },
                  { label: 'Low', count: analysis.analysis.low_risk_count, color: 'bg-green-500', total: analysis.analysis.total_clauses },
                ].map((item) => (
                  <div key={item.label}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-700 dark:text-gray-300">{item.label}</span>
                      <span className="text-gray-600 dark:text-gray-400">{item.count} ({item.total > 0 ? ((item.count / item.total) * 100).toFixed(0) : 0}%)</span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className={`${item.color} h-2 rounded-full transition-all`}
                        style={{ width: `${item.total > 0 ? (item.count / item.total) * 100 : 0}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="lg:col-span-2">
            <ClauseList clauses={analysis.analysis.clauses} riskFilter={riskFilter} analysisId={analysis.analysis_id} />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}

