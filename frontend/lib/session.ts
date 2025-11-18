/**
 * Browser session management for user isolation.
 * Generates and stores a unique session ID in localStorage.
 */

const SESSION_ID_KEY = 'contract_analyzer_session_id'

/**
 * Get or create a session ID.
 * Session ID persists across page refreshes but is unique per browser/device.
 */
export function getSessionId(): string {
  if (typeof window === 'undefined') {
    // Server-side rendering - return empty string
    return ''
  }

  let sessionId = localStorage.getItem(SESSION_ID_KEY)

  if (!sessionId) {
    // Generate a new session ID
    sessionId = generateSessionId()
    localStorage.setItem(SESSION_ID_KEY, sessionId)
  }

  return sessionId
}

/**
 * Generate a unique session ID.
 */
function generateSessionId(): string {
  // Generate a unique ID using timestamp + random string
  const timestamp = Date.now().toString(36)
  const randomStr = Math.random().toString(36).substring(2, 15)
  return `session_${timestamp}_${randomStr}`
}

/**
 * Clear session ID (for testing or logout functionality).
 */
export function clearSessionId(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(SESSION_ID_KEY)
  }
}

/**
 * Get headers with session ID for API requests.
 */
export function getSessionHeaders(): Record<string, string> {
  const sessionId = getSessionId()
  return {
    'X-Session-ID': sessionId,
  }
}

