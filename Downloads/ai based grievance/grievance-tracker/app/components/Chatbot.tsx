'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChatBubbleLeftRightIcon, XMarkIcon } from '@heroicons/react/24/outline'

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>([])
  const [inputText, setInputText] = useState('')

  const toggleChat = () => setIsOpen(!isOpen)

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputText.trim()) {
      setMessages([...messages, { text: inputText, isUser: true }])
      setInputText('')
      // Simulate bot response
      setTimeout(() => {
        setMessages(prev => [...prev, { text: getBotResponse(inputText), isUser: false }])
      }, 500)
    }
  }

  const getBotResponse = (message: string) => {
    const lowerMessage = message.toLowerCase()
    if (lowerMessage.includes('appointment') || lowerMessage.includes('timing')) {
      return "Our office hours are Monday to Friday, 9 AM to 5 PM. You can book an appointment through our online portal or by calling our helpline."
    } else if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
      return "Hello! How can I assist you today?"
    } else {
      return "I'm sorry, I didn't understand that. Can you please rephrase your question?"
    }
  }

  return (
    <>
      <motion.button
        className="fixed bottom-4 right-4 bg-blue-500 text-white p-3 rounded-full shadow-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        onClick={toggleChat}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <ChatBubbleLeftRightIcon className="h-6 w-6" />
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-20 right-4 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl overflow-hidden"
          >
            <div className="bg-blue-500 text-white p-4 flex justify-between items-center">
              <h3 className="font-semibold">Chat with us</h3>
              <button onClick={toggleChat} className="text-white hover:text-gray-200">
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>
            <div className="h-80 overflow-y-auto p-4">
              {messages.map((msg, index) => (
                <div key={index} className={`mb-2 ${msg.isUser ? 'text-right' : 'text-left'}`}>
                  <span className={`inline-block p-2 rounded-lg ${msg.isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white'}`}>
                    {msg.text}
                  </span>
                </div>
              ))}
            </div>
            <form onSubmit={handleSendMessage} className="p-4 border-t dark:border-gray-700">
              <div className="flex">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Type your message..."
                  className="flex-grow px-3 py-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                >
                  Send
                </button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

export default Chatbot