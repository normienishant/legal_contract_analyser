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
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 1200))
      
      let suggestion = originalClause
      let changesMade = false
      
      // Smart rewrite that preserves meaning while reducing risk
      const improvements: string[] = []
      
      // HIGH RISK: More aggressive improvements while maintaining core meaning
      if (riskLabel === 'HIGH') {
        // Liability limitations - preserve intent but add caps
        if (/\bunlimited\s+liability\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bunlimited\s+liability\b/gi, 'liability limited to the total contract value')
          changesMade = true
          improvements.push('Added liability cap to protect both parties')
        }
        
        // Without limitation - add reasonable bounds
        if (/\bwithout\s+limitation\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bwithout\s+limitation\b/gi, 'subject to reasonable limitations as set forth herein')
          changesMade = true
          improvements.push('Added reasonable limitations clause')
        }
        
        // Penalties - add notice and cure period
        if (/\b(shall|will)\s+be\s+penalized\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\b(shall|will)\s+be\s+penalized\b/gi, 'may be subject to reasonable penalties, not exceeding 10% of the contract value, after providing written notice and a 30-day opportunity to cure')
          changesMade = true
          improvements.push('Added notice and cure period for penalties')
        }
        
        // Indemnification - limit scope
        if (/\bindemnify.*without\s+limitation\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bindemnify(.*?)(without\s+limitation)/gi, 'indemnify$1up to the total contract value')
          changesMade = true
          improvements.push('Limited indemnification to contract value')
        }
        
        // Hold harmless - narrow to specific circumstances
        if (/\bhold\s+harmless.*all\s+claims\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bhold\s+harmless.*all\s+claims\b/gi, 'hold harmless for claims arising solely from gross negligence or willful misconduct')
          changesMade = true
          improvements.push('Narrowed hold harmless to specific circumstances')
        }
        
        // Automatic renewal - require mutual consent
        if (/\bautomatic\s+renewal\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bautomatic\s+renewal\b/gi, 'renewal subject to mutual written agreement at least 30 days prior to expiration')
          changesMade = true
          improvements.push('Changed to mutual renewal agreement')
        }
        
        // Sole discretion - add good faith requirement
        if (/\bsole\s+discretion\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bsole\s+discretion\b/gi, 'reasonable discretion, exercised in good faith')
          changesMade = true
          improvements.push('Added good faith requirement')
        }
        
        // Non-refundable - add exceptions
        if (/\bnon-refundable.*(any|all)\s+circumstances\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bnon-refundable(.*?)(any|all)\s+circumstances\b/gi, 'non-refundable$1except in cases of material breach by the other party or as otherwise provided herein')
          changesMade = true
          improvements.push('Added exceptions for material breach')
        }
        
        // Binding arbitration - add mediation option
        if (/\bbinding\s+arbitration.*waiver.*jury\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bbinding\s+arbitration.*waiver.*jury\b/gi, 'dispute resolution through good faith negotiation, followed by mediation if necessary, with binding arbitration as a last resort')
          changesMade = true
          improvements.push('Added negotiation and mediation steps')
        }
      }
      
      // MEDIUM RISK: Moderate improvements
      else if (riskLabel === 'MEDIUM') {
        if (/\bsole\s+discretion\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bsole\s+discretion\b/gi, 'mutual agreement')
          changesMade = true
          improvements.push('Changed to mutual agreement')
        }
        
        if (/\bexclusive\s+jurisdiction\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\bexclusive\s+jurisdiction\b/gi, 'jurisdiction, with option for alternative dispute resolution')
          changesMade = true
          improvements.push('Added alternative dispute resolution option')
        }
        
        if (/\b(shall|must)\s+comply\s+immediately\b/gi.test(suggestion)) {
          suggestion = suggestion.replace(/\b(shall|must)\s+comply\s+immediately\b/gi, 'shall comply within a reasonable time period, not to exceed 30 days')
          changesMade = true
          improvements.push('Added reasonable compliance period')
        }
      }
      
      // LOW RISK: Minor clarifications
      else {
        // Just add clarity without changing meaning
        if (/\b(shall|will)\b/gi.test(suggestion) && !/\b(shall|will)\s+endeavor\b/gi.test(suggestion)) {
          // Keep as is, but note it's already well-written
          improvements.push('Clause is well-structured. Minor clarifications suggested below.')
        }
      }
      
      // If no specific patterns matched, provide contextual improvement
      if (!changesMade) {
        if (riskLabel === 'HIGH') {
          suggestion = `${originalClause}\n\n[SUGGESTED REVISION - Preserving Original Meaning]\n\nConsider adding:\n• Reasonable limitations on any penalties or liabilities\n• Notice and cure periods (typically 30 days) before enforcement\n• Mutual obligations and protections for both parties\n• Alternative dispute resolution mechanisms before litigation\n\nNote: This revision maintains the core intent while adding protective measures. Please review with legal counsel to ensure it meets your specific needs.`
          improvements.push('General risk mitigation suggestions provided')
        } else if (riskLabel === 'MEDIUM') {
          suggestion = `${originalClause}\n\n[SUGGESTED CLARIFICATION]\n\nConsider:\n• Adding specific timeframes where deadlines are mentioned\n• Clarifying mutual obligations\n• Including dispute resolution procedures\n\nThis clause is generally acceptable but could benefit from minor clarifications.`
          improvements.push('Clarification suggestions provided')
        } else {
          suggestion = `${originalClause}\n\n[REVIEW NOTE]\n\nThis clause appears well-structured. Consider:\n• Ensuring all terms are clearly defined\n• Verifying compliance with applicable laws\n• Confirming mutual understanding of obligations\n\nNo significant changes recommended.`
          improvements.push('Minor review suggestions provided')
        }
      } else {
        // Add note about changes
        suggestion = `${suggestion}\n\n[Changes made while preserving original meaning: ${improvements.join('; ')}]`
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

