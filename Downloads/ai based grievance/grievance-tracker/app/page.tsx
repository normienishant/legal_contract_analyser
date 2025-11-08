'use client'

import { motion, useMotionValue, useTransform, animate } from 'framer-motion'
import Link from 'next/link'
import { ArrowRightIcon, ClipboardDocumentCheckIcon, ChartBarIcon, ChatBubbleBottomCenterTextIcon } from '@heroicons/react/24/outline'
import { useEffect } from 'react'

const AnimatedNumber = ({ value }: { value: number }) => {
  const count = useMotionValue(0)
  const rounded = useTransform(count, latest => Math.round(latest))

  useEffect(() => {
    const controls = animate(count, value, { duration: 2 })
    return controls.stop
  }, [count, value])

  return <motion.span>{rounded}</motion.span>
}

export default function Home() {
  return (
    <div className="bg-gradient-to-b from-blue-100 to-white dark:from-blue-900 dark:to-gray-900 min-h-screen">
      <div className="container mx-auto px-4 py-16 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-blue-600 dark:text-blue-400 mb-6">
            AI-Powered Grievance Management
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            Submit and track your grievances with ease, powered by advanced AI technology for faster resolution and improved satisfaction.
          </p>
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Link
              href="/submit"
              className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-full shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-300"
            >
              Lodge a Grievance
              <ArrowRightIcon className="ml-2 -mr-1 h-5 w-5" aria-hidden="true" />
            </Link>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="mt-16"
        >
          <h2 className="text-3xl font-semibold text-center text-gray-800 dark:text-white mb-12">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: 'Submit', description: 'Submit your grievance through our easy-to-use form.', icon: ClipboardDocumentCheckIcon },
              { title: 'AI Analysis', description: 'Our AI analyzes and categorizes your grievance for efficient processing.', icon: ChartBarIcon },
              { title: 'Track Progress', description: 'Track the progress of your grievance in real-time through our dashboard.', icon: ChatBubbleBottomCenterTextIcon }
            ].map((step, index) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.2, duration: 0.5 }}
                className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
              >
                <step.icon className="h-12 w-12 text-blue-500 mb-4 mx-auto" />
                <h3 className="text-xl font-semibold text-blue-600 dark:text-blue-400 mb-2">{step.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.3, duration: 0.8 }}
          className="mt-16 text-center"
        >
          <h2 className="text-3xl font-semibold text-gray-800 dark:text-white mb-8">People We Have Helped</h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
              <h3 className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-4">
                <AnimatedNumber value={10000} />+
              </h3>
              <p className="text-gray-600 dark:text-gray-300">Grievances Resolved</p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
              <h3 className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-4">
                <AnimatedNumber value={5000} />+
              </h3>
              <p className="text-gray-600 dark:text-gray-300">Satisfied Users</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}