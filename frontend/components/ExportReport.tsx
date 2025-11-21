'use client'

import { useState } from 'react'

interface ExportReportProps {
  analysis: {
    filename: string
    created_at: string
    global_risk_score: number
    total_clauses: number
    high_risk_count: number
    medium_risk_count: number
    low_risk_count: number
    clauses: Array<{
      clause_text: string
      clause_index: number
      risk_label: string
      risk_score: number
      explanation: string
      suggested_mitigation: string
    }>
  }
  analysisId: number
}

export default function ExportReport({ analysis, analysisId }: ExportReportProps) {
  const exportToPDF = () => {
    // Create HTML content for PDF
    const htmlContent = `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Contract Analysis Report - ${analysis.filename}</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 40px; line-height: 1.6; }
            h1 { color: #2563eb; border-bottom: 3px solid #2563eb; padding-bottom: 10px; }
            h2 { color: #1e40af; margin-top: 30px; }
            .summary { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0; }
            .risk-high { color: #dc2626; font-weight: bold; }
            .risk-medium { color: #d97706; font-weight: bold; }
            .risk-low { color: #16a34a; font-weight: bold; }
            .clause { margin: 20px 0; padding: 15px; border-left: 4px solid #e5e7eb; }
            .clause-high { border-left-color: #dc2626; }
            .clause-medium { border-left-color: #d97706; }
            .clause-low { border-left-color: #16a34a; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }
            th { background: #f9fafb; font-weight: bold; }
          </style>
        </head>
        <body>
          <h1>Contract Analysis Report</h1>
          <p><strong>Document:</strong> ${analysis.filename}</p>
          <p><strong>Analyzed:</strong> ${new Date(analysis.created_at).toLocaleString()}</p>
          
          <div class="summary">
            <h2>Executive Summary</h2>
            <p><strong>Global Risk Score:</strong> <span class="risk-${analysis.global_risk_score >= 70 ? 'high' : analysis.global_risk_score >= 40 ? 'medium' : 'low'}">${analysis.global_risk_score.toFixed(1)}/100</span></p>
            <table>
              <tr><th>Metric</th><th>Count</th></tr>
              <tr><td>Total Clauses</td><td>${analysis.total_clauses}</td></tr>
              <tr><td>High Risk</td><td class="risk-high">${analysis.high_risk_count}</td></tr>
              <tr><td>Medium Risk</td><td class="risk-medium">${analysis.medium_risk_count}</td></tr>
              <tr><td>Low Risk</td><td class="risk-low">${analysis.low_risk_count}</td></tr>
            </table>
          </div>

          <h2>Detailed Clause Analysis</h2>
          ${analysis.clauses.map((clause, idx) => `
            <div class="clause clause-${clause.risk_label.toLowerCase()}">
              <h3>Clause ${clause.clause_index + 1} - <span class="risk-${clause.risk_label.toLowerCase()}">${clause.risk_label} Risk (${clause.risk_score.toFixed(1)})</span></h3>
              <p><strong>Text:</strong> ${clause.clause_text.substring(0, 500)}${clause.clause_text.length > 500 ? '...' : ''}</p>
              <p><strong>Explanation:</strong> ${clause.explanation}</p>
              <p><strong>Suggested Mitigation:</strong> ${clause.suggested_mitigation}</p>
            </div>
          `).join('')}
        </body>
      </html>
    `

    // Open in new window for printing
    const printWindow = window.open('', '_blank')
    if (printWindow) {
      printWindow.document.write(htmlContent)
      printWindow.document.close()
      printWindow.onload = () => {
        printWindow.print()
      }
    }
  }

  const exportToJSON = () => {
    const report = {
      filename: analysis.filename,
      analyzed_at: analysis.created_at,
      global_risk_score: analysis.global_risk_score,
      summary: {
        total_clauses: analysis.total_clauses,
        high_risk: analysis.high_risk_count,
        medium_risk: analysis.medium_risk_count,
        low_risk: analysis.low_risk_count,
      },
      clauses: analysis.clauses,
    }
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `contract-analysis-${analysisId}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const exportToText = () => {
    let text = `CONTRACT ANALYSIS REPORT\n`
    text += `========================\n\n`
    text += `Document: ${analysis.filename}\n`
    text += `Analyzed: ${new Date(analysis.created_at).toLocaleString()}\n\n`
    text += `EXECUTIVE SUMMARY\n`
    text += `-----------------\n`
    text += `Global Risk Score: ${analysis.global_risk_score.toFixed(1)}/100\n`
    text += `Total Clauses: ${analysis.total_clauses}\n`
    text += `High Risk: ${analysis.high_risk_count}\n`
    text += `Medium Risk: ${analysis.medium_risk_count}\n`
    text += `Low Risk: ${analysis.low_risk_count}\n\n`
    text += `DETAILED CLAUSE ANALYSIS\n`
    text += `------------------------\n\n`
    
    analysis.clauses.forEach((clause) => {
      text += `Clause ${clause.clause_index + 1}: ${clause.risk_label} Risk (${clause.risk_score.toFixed(1)})\n`
      text += `Text: ${clause.clause_text}\n`
      text += `Explanation: ${clause.explanation}\n`
      text += `Mitigation: ${clause.suggested_mitigation}\n\n`
    })

    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `contract-analysis-${analysisId}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  const [showMenu, setShowMenu] = useState(false)

  return (
    <div className="relative">
      <button
        onClick={() => setShowMenu(!showMenu)}
        className="bg-white dark:bg-[#141414] border-2 border-gray-300 dark:border-[#404040] text-gray-700 dark:text-[#e5e5e5] px-6 py-3 rounded-xl font-semibold hover:bg-gray-50 dark:hover:bg-[#1a1a1a] transition-all shadow-lg hover:shadow-xl flex items-center gap-2"
      >
        📥 Export Report
        <span className="text-xs">▼</span>
      </button>
      {showMenu && (
        <>
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setShowMenu(false)}
          ></div>
          <div className="absolute top-full left-0 mt-2 bg-white dark:bg-[#141414] border-2 border-gray-200 dark:border-[#262626] rounded-xl shadow-xl p-2 min-w-[200px] z-20">
            <button
              onClick={() => { exportToPDF(); setShowMenu(false); }}
              className="w-full text-left px-4 py-3 hover:bg-gray-100 dark:hover:bg-[#1a1a1a] rounded-lg transition-colors flex items-center gap-2 text-gray-900 dark:text-[#e5e5e5]"
            >
              <span>📄</span> Export as PDF
            </button>
            <button
              onClick={() => { exportToJSON(); setShowMenu(false); }}
              className="w-full text-left px-4 py-3 hover:bg-gray-100 dark:hover:bg-[#1a1a1a] rounded-lg transition-colors flex items-center gap-2 text-gray-900 dark:text-[#e5e5e5]"
            >
              <span>📋</span> Export as JSON
            </button>
            <button
              onClick={() => { exportToText(); setShowMenu(false); }}
              className="w-full text-left px-4 py-3 hover:bg-gray-100 dark:hover:bg-[#1a1a1a] rounded-lg transition-colors flex items-center gap-2 text-gray-900 dark:text-[#e5e5e5]"
            >
              <span>📝</span> Export as TXT
            </button>
          </div>
        </>
      )}
    </div>
  )
}

