'use client'

import { motion } from 'framer-motion'
import { SunIcon, MoonIcon } from '@heroicons/react/24/solid'

interface DarkModeToggleProps {
  darkMode: boolean
  setDarkMode: (darkMode: boolean) => void
}

const DarkModeToggle: React.FC<DarkModeToggleProps> = ({ darkMode, setDarkMode }) => {
  return (
    <motion.button
      className="fixed top-4 right-4 p-2 rounded-full bg-gray-200 dark:bg-gray-800 text-gray-800 dark:text-gray-200"
      onClick={() => setDarkMode(!darkMode)}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
    >
      {darkMode ? (
        <SunIcon className="h-6 w-6" />
      ) : (
        <MoonIcon className="h-6 w-6" />
      )}
    </motion.button>
  )
}

export default DarkModeToggle