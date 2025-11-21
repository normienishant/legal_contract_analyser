'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import AnalyticsCharts from '@/components/AnalyticsCharts'
import { getHistory } from '@/lib/api'

interface DashboardStats {
  totalAnalyses: number
  totalClauses: number
  avgRiskScore: number
  highRiskCount: number
  recentAnalyses: number
  riskTrend: Array<{ date: string; score: number }>
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [history, setHistory] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const historyData = await getHistory()
        setHistory(historyData)
        
        const totalAnalyses = historyData.length
        const totalClauses = historyData.reduce((sum, item) => sum + item.total_clauses, 0)
        const avgRiskScore = historyData.length > 0
          ? historyData.reduce((sum, item) => sum + item.global_risk_score, 0) / historyData.length
          : 0
        const highRiskCount = historyData.reduce((sum, item) => sum + item.high_risk_count, 0)
        
        // Recent analyses (last 7 days)
        const sevenDaysAgo = new Date()
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
        const recentAnalyses = historyData.filter(
          item => new Date(item.created_at) >= sevenDaysAgo
        ).length

        // Risk trend (last 10 analyses)
        const riskTrend = historyData
          .slice(0, 10)
          .reverse()
          .map(item => ({
            date: new Date(item.created_at).toLocaleDateString(),
            score: item.global_risk_score,
          }))

        setStats({
          totalAnalyses,
          totalClauses,
          avgRiskScore,
          highRiskCount,
          recentAnalyses,
          riskTrend,
        })
      } catch (err) {
        console.error('Failed to load stats:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:bg-[#0a0a0a]">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mb-4"></div>
            <p className="text-gray-600 dark:text-[#e5e5e5]">Loading dashboard...</p>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:bg-[#0a0a0a]">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="text-center text-gray-600 dark:text-[#e5e5e5]">Failed to load dashboard</div>
        </main>
        <Footer />
      </div>
    )
  }

  // Show empty state if no analyses
  if (stats.totalAnalyses === 0) {
    return (
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:bg-[#0a0a0a]">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
              Dashboard
            </h1>
            <p className="text-gray-700 dark:text-[#a3a3a3]">Overview of your contract analyses</p>
          </div>

          <div className="max-w-2xl mx-auto text-center py-16">
            <div className="mb-6">
              <div className="w-24 h-24 bg-gray-200 dark:bg-[#262626] rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">📊</span>
              </div>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-[#e5e5e5] mb-3">
              No Analyses Yet
            </h2>
            <p className="text-gray-600 dark:text-[#a3a3a3] mb-8">
              Upload your first contract to see analytics and insights here.
            </p>
            <Link
              href="/upload"
              className="inline-block bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 hover:scale-105"
            >
              📤 Upload Your First Document
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:bg-[#0a0a0a] dark:text-[#e5e5e5]">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
            Dashboard
          </h1>
          <p className="text-gray-700 dark:text-[#a3a3a3]">Overview of your contract analyses</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-[#a3a3a3] mb-1">Total Analyses</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-[#e5e5e5]">{stats.totalAnalyses}</p>
          </div>

          <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📄</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-[#a3a3a3] mb-1">Total Clauses</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-[#e5e5e5]">{stats.totalClauses.toLocaleString()}</p>
          </div>

          <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">⚠️</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-[#a3a3a3] mb-1">Avg Risk Score</h3>
            <p className={`text-3xl font-bold ${
              stats.avgRiskScore >= 70 ? 'text-red-600 dark:text-red-400' :
              stats.avgRiskScore >= 40 ? 'text-yellow-600 dark:text-yellow-400' :
              'text-green-600 dark:text-green-400'
            }`}>
              {stats.avgRiskScore.toFixed(1)}
            </p>
            <div className="mt-2 w-full bg-gray-200 dark:bg-[#262626] rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${
                  stats.avgRiskScore >= 70 ? 'bg-red-500' :
                  stats.avgRiskScore >= 40 ? 'bg-yellow-500' :
                  'bg-green-500'
                }`}
                style={{ width: `${Math.min(100, stats.avgRiskScore)}%` }}
              ></div>
            </div>
          </div>

          <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🔴</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-[#a3a3a3] mb-1">High Risk Clauses</h3>
            <p className="text-3xl font-bold text-red-600 dark:text-red-400">{stats.highRiskCount}</p>
          </div>
        </div>

        {/* Analytics Charts */}
        {history.length > 0 && (
          <div className="mb-8">
            <AnalyticsCharts history={history} />
          </div>
        )}

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Recent Activity</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-[#262626] rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-[#e5e5e5]">Analyses This Week</p>
                  <p className="text-sm text-gray-600 dark:text-[#a3a3a3]">Last 7 days</p>
                </div>
                <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">{stats.recentAnalyses}</div>
              </div>
              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-[#262626] rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-[#e5e5e5]">Total High Risk</p>
                  <p className="text-sm text-gray-600 dark:text-[#a3a3a3]">Across all analyses</p>
                </div>
                <div className="text-3xl font-bold text-red-600 dark:text-red-400">{stats.highRiskCount}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              href="/upload"
              className="p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl text-center"
            >
              📤 Upload New Document
            </Link>
            <Link
              href="/history"
              className="p-4 bg-white dark:bg-[#141414] border-2 border-gray-300 dark:border-[#262626] text-gray-700 dark:text-[#e5e5e5] rounded-xl font-semibold hover:border-blue-400 dark:hover:border-blue-500 transition-all shadow-lg hover:shadow-xl text-center"
            >
              📋 View History
            </Link>
            <Link
              href="/settings"
              className="p-4 bg-white dark:bg-[#141414] border-2 border-gray-300 dark:border-[#262626] text-gray-700 dark:text-[#e5e5e5] rounded-xl font-semibold hover:border-blue-400 dark:hover:border-blue-500 transition-all shadow-lg hover:shadow-xl text-center"
            >
              ⚙️ Settings
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}

