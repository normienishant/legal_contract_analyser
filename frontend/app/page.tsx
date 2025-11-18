'use client'

import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-16 animate-fadeIn">
            <div className="inline-block mb-4 animate-bounce-slow">
              <span className="bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 text-sm font-semibold px-4 py-2 rounded-full">
                AI-Powered Contract Analysis
              </span>
            </div>
            <h1 className="text-6xl font-extrabold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent animate-slideDown">
              Contract Risk Analyzer
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-10 max-w-2xl mx-auto leading-relaxed animate-fadeIn delay-200">
              Instantly analyze your contracts with advanced AI. Detect risks, get detailed insights, and receive actionable recommendations to protect your business.
            </p>
            <div className="flex gap-4 justify-center flex-wrap animate-fadeIn delay-300">
              <Link
                href="/upload"
                className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-10 py-4 rounded-xl font-semibold hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 hover:scale-105 animate-pulse-slow"
              >
                🚀 Analyze Document
              </Link>
              <Link
                href="/history"
                className="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 px-10 py-4 rounded-xl font-semibold hover:bg-gray-50 dark:hover:bg-gray-700 transition-all shadow-lg hover:shadow-xl border-2 border-gray-200 dark:border-gray-700 transform hover:-translate-y-0.5 hover:scale-105"
              >
                📊 View History
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2 hover:scale-105 border border-gray-100 dark:border-gray-700 animate-slideUp delay-100">
              <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform">
                <span className="text-3xl">🤖</span>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">AI-Powered Analysis</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Advanced machine learning models trained on real-world contracts analyze every clause for potential risks and legal issues.
              </p>
            </div>
            <div className="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2 hover:scale-105 border border-gray-100 dark:border-gray-700 animate-slideUp delay-200">
              <div className="w-14 h-14 bg-red-100 dark:bg-red-900/30 rounded-xl flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform">
                <span className="text-3xl">⚠️</span>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">Risk Scoring</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Get detailed risk scores for each clause and an overall document risk assessment with color-coded visualizations.
              </p>
            </div>
            <div className="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2 hover:scale-105 border border-gray-100 dark:border-gray-700 animate-slideUp delay-300">
              <div className="w-14 h-14 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform">
                <span className="text-3xl">💡</span>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">Smart Recommendations</h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                Receive actionable suggestions and rewrite recommendations to reduce risks and improve contract terms.
              </p>
            </div>
          </div>

          {/* Stats Section */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white text-center shadow-2xl transform hover:scale-105 transition-transform animate-fadeIn delay-400">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="transform hover:scale-110 transition-transform">
                <div className="text-4xl font-bold mb-2 animate-countUp">100%</div>
                <div className="text-blue-100">AI Accuracy</div>
              </div>
              <div className="transform hover:scale-110 transition-transform">
                <div className="text-4xl font-bold mb-2">&lt;30s</div>
                <div className="text-blue-100">Analysis Time</div>
              </div>
              <div className="transform hover:scale-110 transition-transform">
                <div className="text-4xl font-bold mb-2">PDF/DOCX</div>
                <div className="text-blue-100">Supported Formats</div>
              </div>
              <div className="transform hover:scale-110 transition-transform">
                <div className="text-4xl font-bold mb-2">24/7</div>
                <div className="text-blue-100">Available</div>
              </div>
            </div>
          </div>

          {/* How It Works */}
          <div className="mt-16">
            <h2 className="text-4xl font-bold text-center mb-12 text-gray-900 dark:text-white animate-fadeIn">How It Works</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { step: '1', title: 'Upload', desc: 'Upload your contract document (PDF, DOCX, or TXT)', delay: 'delay-100' },
                { step: '2', title: 'Analyze', desc: 'AI extracts text and segments into clauses automatically', delay: 'delay-200' },
                { step: '3', title: 'Detect', desc: 'Advanced models identify risks and score each clause', delay: 'delay-300' },
                { step: '4', title: 'Review', desc: 'Get detailed insights and recommendations instantly', delay: 'delay-400' },
              ].map((item, idx) => (
                <div key={item.step} className={`text-center animate-slideUp ${item.delay} transform hover:scale-105 transition-transform`}>
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4 shadow-lg transform hover:rotate-360 transition-transform duration-500">
                    {item.step}
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{item.title}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}

