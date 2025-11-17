'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
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
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const history = await getHistory()
        
        const totalAnalyses = history.length
        const totalClauses = history.reduce((sum, item) => sum + item.total_clauses, 0)
        const avgRiskScore = history.length > 0
          ? history.reduce((sum, item) => sum + item.global_risk_score, 0) / history.length
          : 0
        const highRiskCount = history.reduce((sum, item) => sum + item.high_risk_count, 0)
        
        // Recent analyses (last 7 days)
        const sevenDaysAgo = new Date()
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
        const recentAnalyses = history.filter(
          item => new Date(item.created_at) >= sevenDaysAgo
        ).length

        // Risk trend (last 10 analyses)
        const riskTrend = history
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
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">Loading dashboard...</p>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="text-center text-gray-600 dark:text-gray-300">Failed to load dashboard</div>
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
          <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
            Dashboard
          </h1>
          <p className="text-gray-700 dark:text-gray-300">Overview of your contract analyses</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Total Analyses</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.totalAnalyses}</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📄</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Total Clauses</h3>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.totalClauses.toLocaleString()}</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">⚠️</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Avg Risk Score</h3>
            <p className={`text-3xl font-bold ${
              stats.avgRiskScore >= 70 ? 'text-red-600 dark:text-red-400' :
              stats.avgRiskScore >= 40 ? 'text-yellow-600 dark:text-yellow-400' :
              'text-green-600 dark:text-green-400'
            }`}>
              {stats.avgRiskScore.toFixed(1)}
            </p>
            <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
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

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🔴</span>
              </div>
            </div>
            <h3 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">High Risk Clauses</h3>
            <p className="text-3xl font-bold text-red-600 dark:text-red-400">{stats.highRiskCount}</p>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Risk Trend Chart */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Risk Trend (Last 10 Analyses)</h2>
            <div className="h-64 flex items-end justify-between gap-2">
              {stats.riskTrend.map((point, idx) => (
                <div key={idx} className="flex-1 flex flex-col items-center">
                  <div
                    className="w-full bg-gradient-to-t from-blue-500 to-purple-500 rounded-t-lg transition-all hover:opacity-80"
                    style={{
                      height: `${(point.score / 100) * 200}px`,
                      minHeight: '4px',
                    }}
                    title={`${point.date}: ${point.score.toFixed(1)}`}
                  ></div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 mt-2 transform -rotate-45 origin-top-left whitespace-nowrap">
                    {point.date.split('/')[0]}/{point.date.split('/')[1]}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Recent Activity</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">Analyses This Week</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Last 7 days</p>
                </div>
                <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">{stats.recentAnalyses}</div>
              </div>
              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">Total High Risk</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Across all analyses</p>
                </div>
                <div className="text-3xl font-bold text-red-600 dark:text-red-400">{stats.highRiskCount}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              href="/upload"
              className="p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl text-center"
            >
              📤 Upload New Document
            </Link>
            <Link
              href="/history"
              className="p-4 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-xl font-semibold hover:border-blue-400 dark:hover:border-blue-500 transition-all shadow-lg hover:shadow-xl text-center"
            >
              📋 View History
            </Link>
            <Link
              href="/settings"
              className="p-4 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-xl font-semibold hover:border-blue-400 dark:hover:border-blue-500 transition-all shadow-lg hover:shadow-xl text-center"
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

