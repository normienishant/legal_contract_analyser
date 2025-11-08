import './globals.css'
import { Inter } from 'next/font/google'
import Header from './components/Header'
import { Providers } from './providers'
import ClientFooter from './components/ClientFooter'
import ClientChatbot from './components/ClientChatbot'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'AI Grievance Tracker',
  description: 'Lodge and track your grievances with AI assistance',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} flex flex-col min-h-screen`}>
        <Providers>
          <Header />
          <main className="flex-grow">
            {children}
          </main>
          <ClientFooter />
          <ClientChatbot />
        </Providers>
      </body>
    </html>
  )
}