'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'
import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

export default function ContactUs() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically handle the form submission
    console.log('Form submitted:', { name, email, message })
    // Reset form fields
    setName('')
    setEmail('')
    setMessage('')
    alert('Thank you for your message. We will get back to you soon!')
  }

  return (
    <div className="bg-gradient-to-b from-blue-100 to-white dark:from-blue-900 dark:to-gray-900 min-h-screen py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-8 text-center">Contact Us</h1>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
            <Image
              src="/contact-us-image.jpg"
              alt="Contact Us"
              width={800}
              height={400}
              className="rounded-lg mb-8 w-full"
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">Get in Touch</h2>
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  We're here to help and answer any question you might have. We look forward to hearing from you!
                </p>
                <div className="mb-4">
                  <h3 className="font-semibold text-gray-800 dark:text-white">Address</h3>
                  <p className="text-gray-600 dark:text-gray-300">123 Grievance Street, AI City, 12345</p>
                </div>
                <div className="mb-4">
                  <h3 className="font-semibold text-gray-800 dark:text-white">Phone</h3>
                  <p className="text-gray-600 dark:text-gray-300">+1 (123) 456-7890</p>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 dark:text-white">Email</h3>
                  <p className="text-gray-600 dark:text-gray-300">support@grievease.com</p>
                </div>
              </div>
              <div>
                <h2 className="text-2xl font-semibold mb-4 text-gray-800 dark:text-white">Send us a Message</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Name</label>
                    <Input
                      type="text"
                      id="name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                      className="mt-1"
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
                    <Input
                      type="email"
                      id="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="mt-1"
                    />
                  </div>
                  <div>
                    <label htmlFor="message" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Message</label>
                    <Textarea
                      id="message"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      required
                      className="mt-1"
                      rows={4}
                    />
                  </div>
                  <Button type="submit" className="w-full">Send Message</Button>
                </form>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}