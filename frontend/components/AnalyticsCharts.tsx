'use client'

import { LineChart, Line, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface AnalyticsChartsProps {
  history: Array<{
    global_risk_score: number
    high_risk_count: number
    medium_risk_count: number
    low_risk_count: number
    created_at: string
  }>
}

const COLORS = {
  high: '#ef4444',
  medium: '#f59e0b',
  low: '#10b981',
}

export default function AnalyticsCharts({ history }: AnalyticsChartsProps) {
  // Risk trend data (last 10 analyses)
  const riskTrend = history
    .slice(0, 10)
    .reverse()
    .map(item => ({
      date: new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      score: item.global_risk_score,
    }))

  // Risk distribution data
  const totalHigh = history.reduce((sum, item) => sum + item.high_risk_count, 0)
  const totalMedium = history.reduce((sum, item) => sum + item.medium_risk_count, 0)
  const totalLow = history.reduce((sum, item) => sum + item.low_risk_count, 0)

  const riskDistribution = [
    { name: 'High Risk', value: totalHigh, color: COLORS.high },
    { name: 'Medium Risk', value: totalMedium, color: COLORS.medium },
    { name: 'Low Risk', value: totalLow, color: COLORS.low },
  ].filter(item => item.value > 0)

  // Risk score distribution (histogram)
  const scoreRanges = [
    { range: '0-20', min: 0, max: 20 },
    { range: '21-40', min: 21, max: 40 },
    { range: '41-60', min: 41, max: 60 },
    { range: '61-80', min: 61, max: 80 },
    { range: '81-100', min: 81, max: 100 },
  ]

  const scoreDistribution = scoreRanges.map(range => ({
    range: range.range,
    count: history.filter(item => 
      item.global_risk_score >= range.min && item.global_risk_score <= range.max
    ).length,
  }))

  // Monthly trend
  const monthlyData = history.reduce((acc, item) => {
    const date = new Date(item.created_at)
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    if (!acc[monthKey]) {
      acc[monthKey] = { month: monthKey, count: 0, avgScore: 0, totalScore: 0 }
    }
    acc[monthKey].count++
    acc[monthKey].totalScore += item.global_risk_score
    acc[monthKey].avgScore = acc[monthKey].totalScore / acc[monthKey].count
    return acc
  }, {} as Record<string, { month: string; count: number; avgScore: number; totalScore: number }>)

  const monthlyTrend = Object.values(monthlyData)
    .slice(-6) // Last 6 months
    .map(item => ({
      month: new Date(item.month + '-01').toLocaleDateString('en-US', { month: 'short' }),
      analyses: item.count,
      avgScore: Number(item.avgScore.toFixed(1)),
    }))

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-[#1a1a1a] border border-gray-200 dark:border-[#404040] rounded-lg p-3 shadow-lg">
          <p className="text-sm font-semibold text-gray-900 dark:text-[#e5e5e5]">
            {payload[0].payload.date || payload[0].payload.month || payload[0].payload.range}
          </p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="space-y-6">
      {/* Risk Trend Line Chart */}
      {riskTrend.length > 0 && (
        <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Risk Trend Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={riskTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" className="dark:stroke-[#404040]" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                className="dark:stroke-[#a3a3a3]"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#6b7280"
                className="dark:stroke-[#a3a3a3]"
                style={{ fontSize: '12px' }}
                domain={[0, 100]}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line 
                type="monotone" 
                dataKey="score" 
                stroke="#2563eb" 
                strokeWidth={2}
                dot={{ fill: '#2563eb', r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Pie Chart */}
        {riskDistribution.length > 0 && (
          <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Risk Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={riskDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {riskDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Risk Score Distribution Bar Chart */}
        {scoreDistribution.some(item => item.count > 0) && (
          <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
            <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Risk Score Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={scoreDistribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" className="dark:stroke-[#404040]" />
                <XAxis 
                  dataKey="range" 
                  stroke="#6b7280"
                  className="dark:stroke-[#a3a3a3]"
                  style={{ fontSize: '12px' }}
                />
                <YAxis 
                  stroke="#6b7280"
                  className="dark:stroke-[#a3a3a3]"
                  style={{ fontSize: '12px' }}
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="count" fill="#7c3aed" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Monthly Trend */}
      {monthlyTrend.length > 0 && (
        <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-[#262626]">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Monthly Analysis Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" className="dark:stroke-[#404040]" />
              <XAxis 
                dataKey="month" 
                stroke="#6b7280"
                className="dark:stroke-[#a3a3a3]"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#6b7280"
                className="dark:stroke-[#a3a3a3]"
                style={{ fontSize: '12px' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Bar dataKey="analyses" fill="#2563eb" name="Analyses" radius={[8, 8, 0, 0]} />
              <Bar dataKey="avgScore" fill="#7c3aed" name="Avg Risk Score" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

