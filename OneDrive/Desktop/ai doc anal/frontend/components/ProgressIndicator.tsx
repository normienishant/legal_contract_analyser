'use client'

interface ProgressIndicatorProps {
  current: number
  total: number
  label: string
}

export default function ProgressIndicator({ current, total, label }: ProgressIndicatorProps) {
  const percentage = total > 0 ? (current / total) * 100 : 0

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">{label}</span>
        <span className="text-sm text-gray-600 dark:text-gray-400">{current} / {total}</span>
      </div>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
        >
          <div className="h-full bg-gradient-to-r from-blue-400 to-purple-400 animate-pulse"></div>
        </div>
      </div>
      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 text-right">{percentage.toFixed(0)}%</p>
    </div>
  )
}

