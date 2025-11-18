'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import RiskBadge from '@/components/RiskBadge'
import { getBookmarks, deleteBookmark, type Bookmark } from '@/lib/api'

export default function BookmarksPage() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchBookmarks()
  }, [])

  const fetchBookmarks = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getBookmarks()
      setBookmarks(data)
    } catch (err: any) {
      setError(err.message || 'Failed to load bookmarks')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (bookmarkId: number) => {
    if (!confirm('Are you sure you want to remove this bookmark?')) return

    try {
      await deleteBookmark(bookmarkId)
      setBookmarks(bookmarks.filter(b => b.id !== bookmarkId))
    } catch (err: any) {
      alert(err.message || 'Failed to delete bookmark')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <Header />
        <main className="flex-grow container mx-auto px-4 py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 dark:border-blue-400 mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300 text-lg">Loading bookmarks...</p>
          </div>
        </main>
        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
              📑 Bookmarks
            </h1>
            <p className="text-gray-700 dark:text-gray-300">Your saved important clauses</p>
          </div>

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
              <p className="text-red-800 dark:text-red-200">{error}</p>
            </div>
          )}

          {bookmarks.length === 0 ? (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-12 text-center border border-gray-100 dark:border-gray-700">
              <div className="text-6xl mb-4">📑</div>
              <h2 className="text-2xl font-bold mb-2 text-gray-900 dark:text-white">No Bookmarks Yet</h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                Start bookmarking important clauses from your analyses
              </p>
              <Link
                href="/history"
                className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                View Analyses
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {bookmarks.map((bookmark) => (
                <div
                  key={bookmark.id}
                  className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 hover:shadow-xl transition-all"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <Link
                          href={`/analysis/${bookmark.analysis_id}`}
                          className="text-blue-600 dark:text-blue-400 hover:underline font-semibold"
                        >
                          {bookmark.analysis_filename}
                        </Link>
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          Clause {bookmark.clause_index + 1}
                        </span>
                        <RiskBadge score={bookmark.risk_score} label={bookmark.risk_label} />
                      </div>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                        Bookmarked on {new Date(bookmark.created_at).toLocaleString()}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDelete(bookmark.id)}
                      className="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                      title="Remove bookmark"
                    >
                      🗑️
                    </button>
                  </div>
                  <p className="text-gray-900 dark:text-gray-100 leading-relaxed mb-3">
                    {bookmark.clause_text}
                  </p>
                  {bookmark.note && (
                    <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-3 mt-3">
                      <p className="text-sm font-semibold text-yellow-800 dark:text-yellow-200 mb-1">Note:</p>
                      <p className="text-sm text-yellow-900 dark:text-yellow-100">{bookmark.note}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  )
}

