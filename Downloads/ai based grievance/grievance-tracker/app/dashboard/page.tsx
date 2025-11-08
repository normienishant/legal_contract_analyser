'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import GrievanceList from '../components/GrievanceList'
import DashboardStats from '../components/DashboardStats'
import SearchAndFilter from '../components/SearchAndFilter'

interface Grievance {
  id: string
  title: string
  category: string
  status: string
  priority: string
  createdAt: string
}

export default function Dashboard() {
  const [grievances, setGrievances] = useState<Grievance[]>([])
  const [filteredGrievances, setFilteredGrievances] = useState<Grievance[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchGrievances = async () => {
      try {
        const response = await fetch('/api/grievances')
        if (response.ok) {
          const data = await response.json()
          setGrievances(data)
          setFilteredGrievances(data)
        } else {
          throw new Error('Failed to fetch grievances')
        }
      } catch (error) {
        console.error('Error fetching grievances:', error)
        alert('Failed to load grievances. Please try again.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchGrievances()
  }, [])

  const handleSearch = (searchTerm: string) => {
    const filtered = grievances.filter(
      (grievance) =>
        grievance.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        grievance.category.toLowerCase().includes(searchTerm.toLowerCase())
    )
    setFilteredGrievances(filtered)
  }

  const handleFilter = (status: string, priority: string) => {
    const filtered = grievances.filter(
      (grievance) =>
        (status === 'all' || grievance.status === status) &&
        (priority === 'all' || grievance.priority === priority)
    )
    setFilteredGrievances(filtered)
  }

  return (
    <div className="bg-gradient-to-b from-blue-100 to-white dark:from-blue-900 dark:to-gray-900 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="max-w-7xl mx-auto"
      >
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Grievance Dashboard</h1>
        <DashboardStats grievances={grievances} />
        <SearchAndFilter onSearch={handleSearch} onFilter={handleFilter} />
        {isLoading ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-10"
          >
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600 dark:text-gray-300">Loading grievances...</p>
          </motion.div>
        ) : filteredGrievances.length === 0 ? (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-10 text-gray-600 dark:text-gray-300"
          >
            No grievances found. Submit one to get started!
          </motion.p>
        ) : (
          <GrievanceList grievances={filteredGrievances} />
        )}
      </motion.div>
    </div>
  )
}