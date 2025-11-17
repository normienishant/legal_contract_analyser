'use client'

import { useState } from 'react'

interface DocumentPreviewProps {
  text: string
  filename: string
}

export default function DocumentPreview({ text, filename }: DocumentPreviewProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const previewLength = 500

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-gray-900">Document Preview</h3>
        <span className="text-sm text-gray-500">{filename}</span>
      </div>
      <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
        <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">
          {isExpanded ? text : `${text.substring(0, previewLength)}${text.length > previewLength ? '...' : ''}`}
        </pre>
      </div>
      {text.length > previewLength && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-4 text-blue-600 hover:text-blue-700 font-semibold text-sm"
        >
          {isExpanded ? 'Show Less' : 'Show More'}
        </button>
      )}
    </div>
  )
}

