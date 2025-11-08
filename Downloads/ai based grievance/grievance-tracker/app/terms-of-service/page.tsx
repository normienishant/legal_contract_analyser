'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'

export default function TermsOfService() {
  return (
    <div className="bg-gradient-to-b from-blue-100 to-white dark:from-blue-900 dark:to-gray-900 min-h-screen py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-8 text-center">Terms of Service</h1>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
            <Image
              src="/terms-of-service-image.jpg"
              alt="Terms of Service"
              width={800}
              height={400}
              className="rounded-lg mb-8 w-full"
            />
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">1. Acceptance of Terms</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              By accessing or using our services, you agree to be bound by these Terms of Service and all applicable laws and regulations.
            </p>
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">2. Use of Services</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              You agree to use our services only for lawful purposes and in accordance with these Terms of Service. You are responsible for maintaining the confidentiality of your account information.
            </p>
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">3. Limitation of Liability</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              We shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of or inability to use our services.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}