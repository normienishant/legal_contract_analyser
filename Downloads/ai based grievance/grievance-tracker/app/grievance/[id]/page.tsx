'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'

interface Grievance {
  id: string
  title: string
  description: string
  category: string
  status: string
  priority: string
  createdAt: string
}

export default function GrievanceDetail({ params }: { params: { id: string } }) {
  const [grievance, setGrievance] = useState<Grievance | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const fetchGrievance = async () => {
      try {
        const response = await fetch(`/api/grievances/${params.id}`)
        if (response.ok) {
          const data = await response.json()
          setGrievance(data)
        } else {
          throw new Error('Failed to fetch grievance')
        }
      } catch (error) {
        console.error('Error fetching grievance:', error)
        alert('Failed to load grievance. Please try again.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchGrievance()
  }, [params.id])

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (!grievance) {
    return <div className="text-center py-10">Grievance not found</div>
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8"
    >
      <button
        onClick={() => router.back()}
        className="mb-6 text-blue-500 hover:text-blue-600 transition duration-300"
      >
        &larr; Back to Dashboard
      </button>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">{grievance.title}</h1>
      <div className="bg-white shadow-md rounded-lg p-6">
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <p className="text-sm font-medium text-gray-500">Category</p>
            <p className="mt-1 text-sm text-gray-900">{grievance.category}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Status</p>
            <p className="mt-1 text-sm text-gray-900">{grievance.status}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Priority</p>
            <p className="mt-1 text-sm text-gray-900">{grievance.priority}</p>
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Created At</p>
            <p className="mt-1 text-sm text-gray-900">{new Date(grievance.createdAt).toLocaleString()}</p>
          </div>
        </div>
        <div>
          <p className="text-sm font-medium text-gray-500">Description</p>
          <p className="mt-1 text-sm text-gray-900">{grievance.description}</p>
        </div>
      </div>
    </motion.div>
  )
}