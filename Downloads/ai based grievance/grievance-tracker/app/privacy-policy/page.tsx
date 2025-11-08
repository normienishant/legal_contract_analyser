'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'

export default function PrivacyPolicy() {
  return (
    <div className="bg-gradient-to-b from-blue-100 to-white dark:from-blue-900 dark:to-gray-900 min-h-screen py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-8 text-center">Privacy Policy</h1>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
            <Image
              src="/privacy-policy-image.jpg"
              alt="Privacy Policy"
              width={800}
              height={400}
              className="rounded-lg mb-8 w-full"
            />
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">1. Information We Collect</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              We collect personal information that you provide to us, such as your name, email address, and any other information you choose to provide when using our services.
            </p>
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">2. How We Use Your Information</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              We use the information we collect to provide, maintain, and improve our services, to communicate with you, and to comply with legal obligations.
            </p>
            <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">3. Data Security</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              We implement appropriate technical and organizational measures to protect your personal information against unauthorized or unlawful processing, accidental loss, destruction, or damage.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}