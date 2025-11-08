'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import GrievanceForm from '../components/GrievanceForm'
import { CheckCircleIcon, ClockIcon, ShieldCheckIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

export default function SubmitGrievance() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const router = useRouter()

  const handleSubmit = async (formData: { title: string; description: string; category: string }) => {
    setIsSubmitting(true)

    try {
      const response = await fetch('/api/grievances', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        setIsSubmitted(true)
        setTimeout(() => {
          router.push('/dashboard')
        }, 3000)
      } else {
        throw new Error('Failed to submit grievance')
      }
    } catch (error) {
      console.error('Error submitting grievance:', error)
      alert('Failed to submit grievance. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="bg-gradient-to-b from-blue-100 to-white dark:from-blue-900 dark:to-gray-900 min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="max-w-2xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md"
      >
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">Submit a Grievance</h1>
        {isSubmitted ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-2">Grievance Submitted Successfully!</h2>
            <p className="text-gray-600 dark:text-gray-300">Redirecting you to the dashboard...</p>
          </motion.div>
        ) : (
          <>
            <GrievanceForm onSubmit={handleSubmit} />
            {isSubmitting && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-4 text-center text-gray-600 dark:text-gray-300"
              >
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mr-2"></div>
                Submitting your grievance...
              </motion.div>
            )}
          </>
        )}
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.8 }}
        className="mt-16 max-w-4xl mx-auto"
      >
        <h2 className="text-3xl font-semibold text-center text-gray-800 dark:text-white mb-12">Our Commitment</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { title: '24/7 Support', description: 'We are always here to assist you.', icon: ClockIcon },
            { title: 'Secure Process', description: 'Your information is safe with us.', icon: ShieldCheckIcon },
            { title: 'Quick Response', description: 'Get timely updates on your grievance.', icon: ChatBubbleLeftRightIcon }
          ].map((item, index) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 + index * 0.2, duration: 0.5 }}
              className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
            >
              <item.icon className="h-12 w-12 text-blue-500 mb-4 mx-auto" />
              <h3 className="text-xl font-semibold text-blue-600 dark:text-blue-400 mb-2">{item.title}</h3>
              <p className="text-gray-600 dark:text-gray-300">{item.description}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.5, duration: 0.8 }}
        className="mt-16 text-center"
      >
        <Link href="/" className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-300">
          Back to Home
        </Link>
      </motion.div>
    </div>
  )
}