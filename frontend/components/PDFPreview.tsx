'use client'

import { useState } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import 'react-pdf/dist/esm/Page/TextLayer.css'

// Set up PDF.js worker
if (typeof window !== 'undefined') {
  pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`
}

interface PDFPreviewProps {
  fileUrl: string
  filename: string
  clauses?: Array<{
    clause_index: number
    clause_text: string
    risk_label: string
    risk_score: number
  }>
  onClauseClick?: (clauseIndex: number) => void
}

export default function PDFPreview({ fileUrl, filename, clauses = [], onClauseClick }: PDFPreviewProps) {
  const [numPages, setNumPages] = useState<number | null>(null)
  const [pageNumber, setPageNumber] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages)
    setLoading(false)
    setError(null)
  }

  function onDocumentLoadError(error: Error) {
    setError('Failed to load PDF. Please try downloading the file instead.')
    setLoading(false)
    console.error('PDF load error:', error)
  }

  const downloadPDF = () => {
    const link = document.createElement('a')
    link.href = fileUrl
    link.download = filename
    link.click()
  }

  return (
    <div className="bg-white dark:bg-[#141414] rounded-2xl shadow-xl border border-gray-100 dark:border-[#262626] p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900 dark:text-[#e5e5e5]">PDF Preview</h2>
        <div className="flex items-center gap-3">
          {numPages && (
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}
                disabled={pageNumber <= 1}
                className="px-3 py-1 bg-gray-100 dark:bg-[#262626] text-gray-700 dark:text-[#e5e5e5] rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-200 dark:hover:bg-[#404040] transition-colors"
              >
                ←
              </button>
              <span className="text-sm text-gray-600 dark:text-[#a3a3a3]">
                Page {pageNumber} of {numPages}
              </span>
              <button
                onClick={() => setPageNumber(Math.min(numPages, pageNumber + 1))}
                disabled={pageNumber >= numPages}
                className="px-3 py-1 bg-gray-100 dark:bg-[#262626] text-gray-700 dark:text-[#e5e5e5] rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-200 dark:hover:bg-[#404040] transition-colors"
              >
                →
              </button>
            </div>
          )}
          <button
            onClick={downloadPDF}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-semibold"
          >
            📥 Download
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4">
          <p className="text-red-800 dark:text-red-200 text-sm">{error}</p>
        </div>
      )}

      <div className="border border-gray-200 dark:border-[#262626] rounded-lg overflow-hidden bg-gray-50 dark:bg-[#0a0a0a]">
        {loading && (
          <div className="flex items-center justify-center h-96">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mb-4"></div>
              <p className="text-gray-600 dark:text-[#a3a3a3]">Loading PDF...</p>
            </div>
          </div>
        )}

        <div className="flex justify-center overflow-auto max-h-[800px]">
          <Document
            file={fileUrl}
            onLoadSuccess={onDocumentLoadSuccess}
            onLoadError={onDocumentLoadError}
            loading={
              <div className="flex items-center justify-center h-96">
                <div className="text-center">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mb-4"></div>
                  <p className="text-gray-600 dark:text-[#a3a3a3]">Loading PDF...</p>
                </div>
              </div>
            }
            error={
              <div className="p-8 text-center">
                <p className="text-red-600 dark:text-red-400 mb-4">Failed to load PDF</p>
                <button
                  onClick={downloadPDF}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Download PDF Instead
                </button>
              </div>
            }
          >
            <Page
              pageNumber={pageNumber}
              renderTextLayer={true}
              renderAnnotationLayer={true}
              className="shadow-lg"
            />
          </Document>
        </div>
      </div>

      {clauses.length > 0 && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-[#e5e5e5] mb-3">Clauses in Document</h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {clauses.map((clause, idx) => (
              <button
                key={idx}
                onClick={() => onClauseClick?.(clause.clause_index)}
                className="w-full text-left p-3 bg-gray-50 dark:bg-[#1a1a1a] hover:bg-gray-100 dark:hover:bg-[#262626] rounded-lg transition-colors border border-gray-200 dark:border-[#262626]"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-900 dark:text-[#e5e5e5]">
                    Clause {clause.clause_index + 1}
                  </span>
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      clause.risk_label === 'HIGH'
                        ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                        : clause.risk_label === 'MEDIUM'
                        ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400'
                        : 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                    }`}
                  >
                    {clause.risk_label}
                  </span>
                </div>
                <p className="text-xs text-gray-600 dark:text-[#a3a3a3] mt-1 line-clamp-2">
                  {clause.clause_text.substring(0, 100)}...
                </p>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

