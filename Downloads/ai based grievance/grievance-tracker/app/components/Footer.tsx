'use client'

import { motion } from 'framer-motion'

const Footer = () => {
  return (
    <footer className="bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-300 py-8">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-4 md:mb-0"
          >
            <p>&copy; 2023 GrievEase. All rights reserved.</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="flex space-x-4"
          >
            <a href="#" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200">
              Terms of Service
            </a>
            <a href="#" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200">
              Contact Us
            </a>
          </motion.div>
        </div>
      </div>
    </footer>
  )
}

export default Footer