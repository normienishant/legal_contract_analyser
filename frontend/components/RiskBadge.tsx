interface RiskBadgeProps {
  score: number
  label?: string
}

export default function RiskBadge({ score, label }: RiskBadgeProps) {
  const getRiskLevel = (score: number) => {
    if (score >= 70) return { text: 'HIGH', color: 'bg-red-500 text-white' }
    if (score >= 40) return { text: 'MEDIUM', color: 'bg-yellow-500 text-white' }
    return { text: 'LOW', color: 'bg-green-500 text-white' }
  }

  const risk = label ? { text: label, color: getRiskLevel(score).color } : getRiskLevel(score)

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${risk.color}`}>
      {risk.text} ({score.toFixed(1)})
    </span>
  )
}

