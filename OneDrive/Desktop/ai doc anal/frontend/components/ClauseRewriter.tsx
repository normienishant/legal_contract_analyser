'use client'

import { useState } from 'react'

interface ClauseRewriterProps {
  originalClause: string
  riskLabel: string
  onRewrite?: (rewritten: string) => void
}

export default function ClauseRewriter({ originalClause, riskLabel, onRewrite }: ClauseRewriterProps) {
  const [rewritten, setRewritten] = useState('')
  const [loading, setLoading] = useState(false)

  const generateRewrite = async () => {
    setLoading(true)
    try {
      // Simulate AI rewrite (in production, call backend API)
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Enhanced rewrite logic based on risk
      let suggestion = originalClause
      if (riskLabel === 'HIGH') {
        // Replace high-risk patterns with safer alternatives
        suggestion = originalClause
          .replace(/unlimited\s+liability/gi, 'liability limited to the contract value')
          .replace(/without\s+limitation/gi, 'subject to reasonable limitations')
          .replace(/shall\s+be\s+penalized/gi, 'may be subject to reasonable penalties not exceeding 10% of the contract value, subject to prior written notice and opportunity to cure')
          .replace(/indemnify.*without\s+limitation/gi, 'indemnify up to the total contract value')
          .replace(/hold\s+harmless.*all\s+claims/gi, 'hold harmless for claims arising from gross negligence or willful misconduct')
          .replace(/automatic\s+renewal/gi, 'renewal subject to mutual written agreement')
          .replace(/sole\s+discretion/gi, 'reasonable discretion, subject to good faith')
          .replace(/non-refundable.*any\s+circumstances/gi, 'non-refundable except in cases of material breach by the other party')
          .replace(/binding\s+arbitration.*waiver.*jury/gi, 'dispute resolution through mediation, with arbitration as a last resort')
      } else if (riskLabel === 'MEDIUM') {
        suggestion = originalClause
          .replace(/sole\s+discretion/gi, 'mutual agreement')
          .replace(/binding/gi, 'subject to review and mutual consent')
          .replace(/exclusive\s+jurisdiction/gi, 'jurisdiction with option for alternative dispute resolution')
      }
      
      // If no replacements were made, provide a general improvement
      if (suggestion === originalClause && riskLabel === 'HIGH') {
        suggestion = `REVISED: ${originalClause}\n\nThis clause should be reviewed to:\n- Add reasonable limitations to any penalties or liabilities\n- Include notice and cure periods where applicable\n- Ensure mutual obligations and protections\n- Consider alternative dispute resolution mechanisms\n\nPlease consult with legal counsel for specific revisions tailored to your circumstances.`
      }
      
      setRewritten(suggestion)
      if (onRewrite) {
        onRewrite(suggestion)
      }
    } catch (err) {
      console.error('Failed to generate rewrite:', err)
      setRewritten('Error generating rewrite. Please try again or consult legal counsel.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold text-blue-900 dark:text-blue-100 flex items-center gap-2">
          <span>✏️</span> Rewrite Suggestion
        </h4>
        <button
          onClick={generateRewrite}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors text-sm font-semibold"
        >
          {loading ? 'Generating...' : 'Generate Rewrite'}
        </button>
      </div>
      {rewritten && (
        <div className="mt-3 p-4 bg-white dark:bg-gray-800 rounded-lg border-2 border-blue-300 dark:border-blue-600 shadow-md">
          <p className="text-sm text-black dark:text-gray-100 whitespace-pre-wrap leading-relaxed font-medium">{rewritten}</p>
          <div className="mt-3 flex gap-2">
            <button
              onClick={async () => {
                try {
                  await navigator.clipboard.writeText(rewritten)
                  alert('✅ Copied to clipboard!')
                } catch (err) {
                  alert('Failed to copy. Please select and copy manually.')
                }
              }}
              className="px-3 py-1.5 text-xs bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
            >
              📋 Copy to clipboard
            </button>
            <button
              onClick={() => setRewritten('')}
              className="px-3 py-1.5 text-xs bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors font-semibold"
            >
              Clear
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

