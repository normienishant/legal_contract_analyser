'use client'

import { motion } from 'framer-motion'

interface Grievance {
  id: string
  title: string
  category: string
  status: string
  priority: string
  createdAt: string
}

interface DashboardStatsProps {
  grievances: Grievance[]
}

const DashboardStats: React.FC<DashboardStatsProps> = ({ grievances }) => {
  const totalGrievances = grievances.length
  const openGrievances = grievances.filter((g) => g.status === 'open').length
  const resolvedGrievances = grievances.filter((g) => g.status === 'resolved').length
  const highPriorityGrievances = grievances.filter((g) => g.priority === 'high').length

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
    >
      <StatCard title="Total Grievances" value={totalGrievances} color="bg-blue-500" />
      <StatCard title="Open Grievances" value={openGrievances} color="bg-yellow-500" />
      <StatCard title="Resolved Grievances" value={resolvedGrievances} color="bg-green-500" />
      <StatCard title="High Priority" value={highPriorityGrievances} color="bg-red-500" />
    </motion.div>
  )
}

const StatCard: React.FC<{ title: string; value: number; color: string }> = ({ title, value, color }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className={`${color} rounded-lg shadow-lg p-6 text-white`}
  >
    <h3 className="text-lg font-semibold mb-2">{title}</h3>
    <p className="text-3xl font-bold">{value}</p>
  </motion.div>
)

export default DashboardStats