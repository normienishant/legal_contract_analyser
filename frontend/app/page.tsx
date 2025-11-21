'use client'

import Link from 'next/link'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:bg-[#0a0a0a] dark:text-[#e5e5e5]">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-16 animate-fadeIn">
            <div className="inline-block mb-4 animate-bounce-slow">
              <span className="bg-blue-100 dark:bg-[#141414] dark:border dark:border-[#262626] text-blue-800 dark:text-[#e5e5e5] text-sm font-semibold px-4 py-2 rounded-full">
                AI-Powered Contract Analysis
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold mb-4 sm:mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent animate-slideDown px-2 break-words">
              Contract Risk Analyzer
            </h1>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 dark:text-[#a3a3a3] mb-8 sm:mb-10 max-w-2xl mx-auto leading-relaxed animate-fadeIn delay-200 px-4">
              Instantly analyze your contracts with advanced AI. Detect risks, get detailed insights, and receive actionable recommendations to protect your business.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center flex-wrap animate-fadeIn delay-300 px-4">
              <Link
                href="/upload"
                className="w-full sm:w-auto bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 sm:px-10 py-3 sm:py-4 rounded-xl font-semibold hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 hover:scale-105 animate-pulse-slow text-center"
              >
                🚀 Analyze Document
              </Link>
              <Link
                href="/history"
                className="w-full sm:w-auto bg-white dark:bg-[#141414] text-gray-800 dark:text-[#e5e5e5] px-8 sm:px-10 py-3 sm:py-4 rounded-xl font-semibold hover:bg-gray-50 dark:hover:bg-[#1a1a1a] transition-all shadow-lg hover:shadow-xl border-2 border-gray-200 dark:border-[#262626] transform hover:-translate-y-0.5 hover:scale-105 text-center"
              >
                📊 View History
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="p-8 bg-white dark:bg-[#141414] rounded-2xl shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2 hover:scale-105 border border-gray-100 dark:border-[#262626] animate-slideUp delay-100">
              <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform">
                <span className="text-3xl">🤖</span>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-[#e5e5e5]">AI-Powered Analysis</h3>
              <p className="text-gray-600 dark:text-[#a3a3a3] leading-relaxed">
                Advanced machine learning models trained on real-world contracts analyze every clause for potential risks and legal issues.
              </p>
            </div>
            <div className="p-8 bg-white dark:bg-[#141414] rounded-2xl shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2 hover:scale-105 border border-gray-100 dark:border-[#262626] animate-slideUp delay-200">
              <div className="w-14 h-14 bg-red-100 dark:bg-red-900/30 rounded-xl flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform">
                <span className="text-3xl">⚠️</span>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-[#e5e5e5]">Risk Scoring</h3>
              <p className="text-gray-600 dark:text-[#e5e5e5] leading-relaxed">
                Get detailed risk scores for each clause and an overall document risk assessment with color-coded visualizations.
              </p>
            </div>
            <div className="p-8 bg-white dark:bg-[#141414] rounded-2xl shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2 hover:scale-105 border border-gray-100 dark:border-[#262626] animate-slideUp delay-300">
              <div className="w-14 h-14 bg-green-100 dark:bg-green-900/30 rounded-xl flex items-center justify-center mb-4 transform hover:rotate-12 transition-transform">
                <span className="text-3xl">💡</span>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-[#e5e5e5]">Smart Recommendations</h3>
              <p className="text-gray-600 dark:text-[#e5e5e5] leading-relaxed">
                Receive actionable suggestions and rewrite recommendations to reduce risks and improve contract terms.
              </p>
            </div>
          </div>

          {/* Stats Section */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 sm:p-8 md:p-12 text-white text-center shadow-2xl transform hover:scale-105 transition-transform animate-fadeIn delay-400 mx-2 sm:mx-0">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6 md:gap-8">
              <div className="transform hover:scale-110 transition-transform">
                <div className="text-4xl font-bold mb-2 animate-countUp">95%+</div>
                <div className="text-blue-100">Test Accuracy</div>
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
          <div className="mt-12 sm:mt-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-center mb-8 sm:mb-12 text-gray-900 dark:text-[#e5e5e5] animate-fadeIn px-4">How It Works</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6 px-2">
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
                  <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-[#e5e5e5]">{item.title}</h3>
                  <p className="text-gray-600 dark:text-[#a3a3a3]">{item.desc}</p>
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

