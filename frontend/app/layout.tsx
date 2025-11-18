import type { Metadata } from 'next'
import './globals.css'
import KeyboardShortcuts from '@/components/KeyboardShortcuts'

export const metadata: Metadata = {
  title: 'AI Contract Analyzer & Risk Detector',
  description: 'Analyze contract documents and detect risks',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="dark:bg-gray-900 dark:text-white transition-colors">
        {children}
        <KeyboardShortcuts />
      </body>
    </html>
  )
}

