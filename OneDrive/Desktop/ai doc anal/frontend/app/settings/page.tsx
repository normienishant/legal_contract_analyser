'use client'

import { useEffect, useState } from 'react'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import DarkModeToggle from '@/components/DarkModeToggle'

export default function SettingsPage() {
  const [mlMode, setMlMode] = useState<'ml' | 'rules'>('ml')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)
  const [backendConnected, setBackendConnected] = useState(false)

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout
        
        const response = await fetch('http://localhost:8000/health', {
          signal: controller.signal
        })
        clearTimeout(timeoutId)
        
        if (response.ok) {
          const data = await response.json()
          setMlMode(data.ml_mode || 'ml')
          setBackendConnected(true)
        } else {
          setBackendConnected(false)
        }
      } catch (err) {
        console.error('Failed to load settings:', err)
        setBackendConnected(false)
        // Default to ML mode if backend not available
        setMlMode('ml')
      } finally {
        setLoading(false)
      }
    }
    fetchSettings()
  }, [])

  const handleSave = async () => {
    if (!backendConnected) {
      setMessage({ type: 'error', text: 'Backend not connected. Cannot save settings.' })
      return
    }

    setSaving(true)
    setMessage(null)
    try {
      const response = await fetch('http://localhost:8000/api/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ml_mode: mlMode }),
      })

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Failed to save settings' }))
        throw new Error(error.detail || 'Failed to save settings')
      }

      const result = await response.json()
      setMessage({ type: 'success', text: result.message || 'Settings saved successfully! Mode changed without restart.' })
    } catch (err: any) {
      setMessage({ type: 'error', text: err.message || 'Failed to save settings' })
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12 max-w-4xl">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Settings
          </h1>
          <p className="text-gray-600 dark:text-gray-300">Configure your analysis preferences</p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
            <p className="text-gray-600 dark:text-gray-300">Loading settings...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Backend Connection Status */}
            {!backendConnected && (
              <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-4">
                <div className="flex items-center gap-2">
                  <span className="text-xl">⚠️</span>
                  <div>
                    <p className="font-semibold text-yellow-900 dark:text-yellow-100">Backend Not Connected</p>
                    <p className="text-sm text-yellow-800 dark:text-yellow-200">
                      Make sure the backend server is running on http://localhost:8000
                    </p>
                  </div>
                </div>
              </div>
            )}

            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-100 dark:border-gray-700 space-y-8">
            {/* ML Mode Setting */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Analysis Mode</h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Choose how contracts should be analyzed for risks
              </p>
              <div className="space-y-4">
                <div className={`flex items-start gap-4 p-4 border-2 rounded-xl transition-colors ${
                  mlMode === 'ml' 
                    ? 'border-blue-500 dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                    : 'border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500'
                }`}>
                  <input
                    type="radio"
                    id="ml-mode"
                    name="mode"
                    value="ml"
                    checked={mlMode === 'ml'}
                    onChange={(e) => setMlMode(e.target.value as 'ml' | 'rules')}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <label htmlFor="ml-mode" className="block font-semibold text-gray-900 dark:text-white cursor-pointer">
                        🤖 ML-Powered Analysis
                      </label>
                      <span className="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs font-semibold rounded">
                        Recommended
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                      Uses AI model trained on 5000+ real contract clauses. Provides accurate, context-aware risk classification.
                    </p>
                    <ul className="text-xs text-gray-500 dark:text-gray-400 space-y-1 list-disc list-inside ml-4">
                      <li>Better accuracy on complex clauses</li>
                      <li>Understands context and nuance</li>
                      <li>Trained on real-world legal documents</li>
                    </ul>
                  </div>
                </div>

                <div className={`flex items-start gap-4 p-4 border-2 rounded-xl transition-colors ${
                  mlMode === 'rules' 
                    ? 'border-blue-500 dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                    : 'border-gray-200 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500'
                }`}>
                  <input
                    type="radio"
                    id="rules-mode"
                    name="mode"
                    value="rules"
                    checked={mlMode === 'rules'}
                    onChange={(e) => setMlMode(e.target.value as 'ml' | 'rules')}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <label htmlFor="rules-mode" className="block font-semibold text-gray-900 dark:text-white mb-1 cursor-pointer">
                      ⚙️ Rule-Based Analysis
                    </label>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                      Uses keyword matching and pattern detection. Faster but less accurate than ML mode.
                    </p>
                    <ul className="text-xs text-gray-500 dark:text-gray-400 space-y-1 list-disc list-inside ml-4">
                      <li>Faster processing</li>
                      <li>No model loading required</li>
                      <li>Good for simple contracts</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Additional Settings */}
            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">General Settings</h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Configure application preferences
              </p>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white">Dark Mode</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Toggle dark/light theme</p>
                  </div>
                  <DarkModeToggle />
                </div>
                
                <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white">Export Format</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Default export format for reports</p>
                  </div>
                  <select className="px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white text-gray-900 dark:text-white rounded-lg text-sm focus:outline-none focus:border-blue-500">
                    <option className="text-gray-900 dark:text-white">PDF</option>
                    <option className="text-gray-900 dark:text-white">JSON</option>
                    <option className="text-gray-900 dark:text-white">TXT</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Info Section */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
              <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2 flex items-center gap-2">
                <span>ℹ️</span> How It Works
              </h3>
              <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-2 list-disc list-inside">
                <li><strong>ML Mode:</strong> AI model analyzes each clause using patterns learned from 5000+ real contracts</li>
                <li><strong>Rules Mode:</strong> Uses keyword matching - faster but may miss complex risks</li>
                <li><strong>Recommendation:</strong> Use ML mode for best accuracy (default)</li>
                <li><strong>Note:</strong> Mode changes take effect immediately - no restart needed!</li>
              </ul>
            </div>

            {/* Save Button */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
              {message && (
                <div className={`px-4 py-2 rounded-lg text-sm ${
                  message.type === 'success' 
                    ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800' 
                    : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800'
                }`}>
                  {message.text}
                </div>
              )}
              <div className="ml-auto flex gap-3">
                <button
                  onClick={() => {
                    setMlMode('ml')
                    setMessage({ type: 'success', text: 'Settings reset to defaults' })
                  }}
                  className="px-6 py-3 bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-xl font-semibold hover:border-blue-400 transition-all"
                >
                  Reset
                </button>
                <button
                  onClick={handleSave}
                  disabled={saving || !backendConnected}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
                >
                  {saving ? 'Saving...' : 'Save Settings'}
                </button>
              </div>
            </div>
          </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

