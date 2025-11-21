import type { Metadata } from 'next'
import './globals.css'
import KeyboardShortcuts from '@/components/KeyboardShortcuts'
import Toaster from '@/components/Toaster'

export const metadata: Metadata = {
  title: 'AI Contract Analyzer & Risk Detector',
  description: 'Analyze contract documents and detect risks',
  icons: {
    icon: '/icon.svg',
    shortcut: '/icon.svg',
    apple: '/icon.svg',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="transition-colors">
        {children}
        <KeyboardShortcuts />
        <Toaster />
      </body>
    </html>
  )
}

