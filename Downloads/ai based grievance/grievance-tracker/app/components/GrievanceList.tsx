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

interface GrievanceListProps {
  grievances: Grievance[]
}

const GrievanceList: React.FC<GrievanceListProps> = ({ grievances }) => {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open':
        return 'bg-yellow-200 text-yellow-800'
      case 'in progress':
        return 'bg-blue-200 text-blue-800'
      case 'resolved':
        return 'bg-green-200 text-green-800'
      default:
        return 'bg-gray-200 text-gray-800'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'bg-red-200 text-red-800'
      case 'medium':
        return 'bg-orange-200 text-orange-800'
      case 'low':
        return 'bg-green-200 text-green-800'
      default:
        return 'bg-gray-200 text-gray-800'
    }
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600 uppercase tracking-wider">Title</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600 uppercase tracking-wider">Category</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600 uppercase tracking-wider">Status</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600 uppercase tracking-wider">Priority</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-gray-600 uppercase tracking-wider">Created At</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {grievances.map((grievance) => (
            <motion.tr
              key={grievance.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="hover:bg-gray-50"
            >
              <td className="px-4 py-3 text-sm text-gray-900">{grievance.title}</td>
              <td className="px-4 py-3 text-sm text-gray-900">{grievance.category}</td>
              <td className="px-4 py-3 text-sm">
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusColor(grievance.status)}`}>
                  {grievance.status}
                </span>
              </td>
              <td className="px-4 py-3 text-sm">
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getPriorityColor(grievance.priority)}`}>
                  {grievance.priority}
                </span>
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">{new Date(grievance.createdAt).toLocaleString()}</td>
            </motion.tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default GrievanceList