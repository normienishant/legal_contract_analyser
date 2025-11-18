import { getSessionHeaders } from './session'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface UploadResponse {
  file_id: string
  filename: string
  message: string
}

export interface ClauseAnalysis {
  clause_text: string
  clause_index: number
  risk_label: string
  risk_score: number
  explanation: string
  suggested_mitigation: string
}

export interface DocumentAnalysis {
  global_risk_score: number
  total_clauses: number
  high_risk_count: number
  medium_risk_count: number
  low_risk_count: number
  clauses: ClauseAnalysis[]
}

export interface AnalysisResponse {
  analysis_id: number
  filename: string
  analysis: DocumentAnalysis
  created_at: string
}

export interface HistoryItem {
  id: number
  filename: string
  original_filename: string
  global_risk_score: number
  total_clauses: number
  high_risk_count: number
  medium_risk_count: number
  low_risk_count: number
  created_at: string
}

export async function uploadFile(file: FormData): Promise<UploadResponse> {
  const headers = getSessionHeaders()
  const response = await fetch(`${API_BASE_URL}/api/upload`, {
    method: 'POST',
    headers,
    body: file,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Upload failed')
  }

  return response.json()
}

export async function getAnalysis(analysisId: string): Promise<AnalysisResponse> {
  const headers = getSessionHeaders()
  const response = await fetch(`${API_BASE_URL}/api/history/${analysisId}`, {
    headers,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to get analysis')
  }

  return response.json()
}

export async function getHistory(): Promise<HistoryItem[]> {
  try {
    const headers = getSessionHeaders()
    const response = await fetch(`${API_BASE_URL}/api/history`, {
      headers,
      signal: AbortSignal.timeout(10000) // 10 second timeout
    })

    if (!response.ok) {
      // If backend is not running, return empty array instead of throwing
      if (response.status === 0 || response.status >= 500) {
        console.warn('Backend may not be running. Returning empty history.')
        return []
      }
      const error = await response.json().catch(() => ({ detail: 'Failed to get history' }))
      throw new Error(error.detail || 'Failed to get history')
    }

    const data = await response.json()
    return Array.isArray(data) ? data : []
  } catch (err: any) {
    // Network errors or timeouts - return empty array
    if (err.name === 'AbortError' || err.name === 'TypeError') {
      console.warn('Failed to connect to backend. Make sure backend is running.')
      return []
    }
    throw err
  }
}

