'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Uploader from '@/components/Uploader'

export default function UploadPage() {
  const router = useRouter()
  const [uploading, setUploading] = useState(false)

  const handleUploadSuccess = (fileId: string) => {
    router.push(`/analysis/${fileId}`)
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:bg-[#0a0a0a]">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Upload Document
            </h1>
            <p className="text-gray-600 dark:text-[#e5e5e5]">Get instant AI-powered risk analysis</p>
          </div>
          <Uploader onUploadSuccess={handleUploadSuccess} uploading={uploading} setUploading={setUploading} />
        </div>
      </main>
      <Footer />
    </div>
  )
}

