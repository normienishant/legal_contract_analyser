'use client'

import { useState } from 'react'
import { uploadFile } from '@/lib/api'
import { getSessionHeaders } from '@/lib/session'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface UploaderProps {
  onUploadSuccess: (fileId: string) => void
  uploading: boolean
  setUploading: (value: boolean) => void
}

export default function Uploader({ onUploadSuccess, uploading, setUploading }: UploaderProps) {
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      const ext = selectedFile.name.split('.').pop()?.toLowerCase()
      if (!['pdf', 'docx', 'txt'].includes(ext || '')) {
        setError('Please upload a PDF, DOCX, or TXT file')
        return
      }
      setFile(selectedFile)
      setError(null)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    if (uploading) return

    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile) {
      const ext = droppedFile.name.split('.').pop()?.toLowerCase()
      if (!['pdf', 'docx', 'txt'].includes(ext || '')) {
        setError('Please upload a PDF, DOCX, or TXT file')
        return
      }
      if (droppedFile.size > 10 * 1024 * 1024) {
        setError('File size exceeds 10MB limit')
        return
      }
      setFile(droppedFile)
      setError(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    try {
      setUploading(true)
      setError(null)
      const formData = new FormData()
      formData.append('file', file)
      
      const result = await uploadFile(formData)
      
      // Trigger analysis pipeline
      // First extract, then analyze
      const sessionHeaders = getSessionHeaders()
      const extractResponse = await fetch(`${API_BASE_URL}/api/extract?file_id=${result.file_id}`, {
        method: 'POST',
        headers: sessionHeaders,
      })
      if (!extractResponse.ok) {
        const errorData = await extractResponse.json().catch(() => ({ detail: 'Failed to extract text' }))
        throw new Error(errorData.detail || 'Failed to extract text')
      }
      
      const analysisResponse = await fetch(`${API_BASE_URL}/api/analyze?file_id=${result.file_id}`, {
        method: 'POST',
        headers: sessionHeaders,
      })
      if (!analysisResponse.ok) {
        const errorData = await analysisResponse.json().catch(() => ({ detail: 'Failed to analyze document' }))
        throw new Error(errorData.detail || 'Failed to analyze document')
      }
      
      const analysisData = await analysisResponse.json()
      onUploadSuccess(analysisData.analysis_id.toString())
    } catch (err: any) {
      console.error('Upload error:', err)
      if (err.name === 'AbortError' || err.message?.includes('fetch')) {
        setError('Failed to connect to server. Please check if the backend is running and NEXT_PUBLIC_API_URL is set correctly.')
      } else if (err.message) {
        setError(err.message)
      } else {
        setError('Upload failed. Please try again.')
      }
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl p-8 border border-gray-100 dark:border-[#262626]">
      <div className="text-center mb-6">
        <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <span className="text-4xl">📄</span>
        </div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-[#e5e5e5] mb-2">Upload Your Contract</h2>
        <p className="text-gray-600 dark:text-[#e5e5e5]">Supported formats: PDF, DOCX, TXT (Max 10MB)</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 dark:text-[#e5e5e5] mb-3">
            Select Document
          </label>
          <div 
            className={`border-2 border-dashed rounded-xl p-8 text-center transition-all bg-gray-50 dark:bg-[#0a0a0a] ${
              isDragging 
                ? 'border-blue-500 dark:border-blue-400 bg-blue-50 dark:bg-blue-900/20 scale-105' 
                : 'border-gray-300 dark:border-[#262626] hover:border-blue-400 dark:hover:border-blue-500'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
              disabled={uploading}
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer flex flex-col items-center"
            >
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <span className="text-3xl">📎</span>
              </div>
              {file ? (
                <div>
                  <p className="text-lg font-semibold text-gray-900 dark:text-[#e5e5e5]">{file.name}</p>
                  <p className="text-sm text-gray-500 dark:text-[#a3a3a3] mt-1">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <button
                    onClick={(e) => {
                      e.preventDefault()
                      e.stopPropagation()
                      setFile(null)
                      setError(null)
                    }}
                    className="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline"
                  >
                    Remove file
                  </button>
                </div>
              ) : (
                <div>
                  <p className="text-gray-700 dark:text-[#e5e5e5] font-medium mb-1">
                    {isDragging ? 'Drop file here' : 'Click to browse or drag and drop'}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-[#a3a3a3]">PDF, DOCX, or TXT files (Max 10MB)</p>
                </div>
              )}
            </label>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg text-sm">
            ⚠️ {error}
          </div>
        )}

        {uploading && (
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-300 px-4 py-3 rounded-lg text-sm">
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-700 dark:border-blue-400"></div>
                <span>Uploading and analyzing your document...</span>
              </div>
              <div className="w-full bg-blue-200 dark:bg-blue-800 rounded-full h-2">
                <div className="bg-blue-600 dark:bg-blue-400 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
              </div>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={!file || uploading}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:transform-none"
        >
          {uploading ? (
            <span className="flex items-center justify-center gap-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Analyzing...
            </span>
          ) : (
            '🚀 Upload and Analyze'
          )}
        </button>
      </form>
    </div>
  )
}

