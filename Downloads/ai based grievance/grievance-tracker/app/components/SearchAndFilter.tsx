'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'

interface SearchAndFilterProps {
  onSearch: (searchTerm: string) => void
  onFilter: (status: string, priority: string) => void
}

const SearchAndFilter: React.FC<SearchAndFilterProps> = ({ onSearch, onFilter }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [status, setStatus] = useState('all')
  const [priority, setPriority] = useState('all')

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value)
    onSearch(e.target.value)
  }

  const handleFilter = () => {
    onFilter(status, priority)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mb-8 flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4"
    >
      <input
        type="text"
        placeholder="Search grievances..."
        value={searchTerm}
        onChange={handleSearch}
        className="w-full md:w-1/3 px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <select
        value={status}
        onChange={(e) => setStatus(e.target.value)}
        className="w-full md:w-auto px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">All Statuses</option>
        <option value="open">Open</option>
        <option value="in progress">In Progress</option>
        <option value="resolved">Resolved</option>
      </select>
      <select
        value={priority}
        onChange={(e) => setPriority(e.target.value)}
        className="w-full md:w-auto px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">All Priorities</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={handleFilter}
        className="w-full md:w-auto px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition duration-300"
      >
        Apply Filters
      </motion.button>
    </motion.div>
  )
}

export default SearchAndFilter