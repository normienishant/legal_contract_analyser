/**
 * API Client with Automatic Failover
 * Tries Railway first, falls back to Render if Railway fails
 */

import { getSessionHeaders } from './session'

// Backend URLs - Primary first, then fallback
const BACKEND_URLS = [
  process.env.NEXT_PUBLIC_RAILWAY_API_URL || '', // Railway (Primary)
  process.env.NEXT_PUBLIC_RENDER_API_URL || '',  // Render (Backup)
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000', // Fallback
].filter(Boolean) // Remove empty strings

// Cache for working backend URL
const WORKING_BACKEND_KEY = 'working_backend_url'
const BACKEND_CHECK_INTERVAL = 5 * 60 * 1000 // Check every 5 minutes

/**
 * Get the working backend URL from cache or detect it
 */
async function getWorkingBackend(): Promise<string> {
  // Check cache first
  if (typeof window !== 'undefined') {
    const cached = localStorage.getItem(WORKING_BACKEND_KEY)
    const cacheTime = localStorage.getItem(`${WORKING_BACKEND_KEY}_time`)
    
    if (cached && cacheTime) {
      const age = Date.now() - parseInt(cacheTime, 10)
      if (age < BACKEND_CHECK_INTERVAL) {
        // Verify cached backend is still working
        if (await checkBackendHealth(cached)) {
          return cached
        }
      }
    }
  }

  // Try each backend in order
  for (const url of BACKEND_URLS) {
    if (await checkBackendHealth(url)) {
      // Cache the working backend
      if (typeof window !== 'undefined') {
        localStorage.setItem(WORKING_BACKEND_KEY, url)
        localStorage.setItem(`${WORKING_BACKEND_KEY}_time`, Date.now().toString())
      }
      return url
    }
  }

  // If all fail, return the first one (will show error to user)
  return BACKEND_URLS[0] || 'http://localhost:8000'
}

/**
 * Check if a backend is healthy
 */
async function checkBackendHealth(url: string): Promise<boolean> {
  if (!url || url.trim() === '') {
    return false
  }
  
  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 3000) // 3 second timeout
    
    const response = await fetch(`${url}/health`, {
      signal: controller.signal,
      method: 'GET',
    })
    
    clearTimeout(timeoutId)
    return response.ok
  } catch {
    return false
  }
}

/**
 * Make API request with automatic failover
 */
async function fetchWithFailover(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  let lastError: Error | null = null
  
  // Try each backend in order
  for (const url of BACKEND_URLS) {
    try {
      const fullUrl = `${url}${endpoint}`
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 30000) // 30 second timeout
      
      const response = await fetch(fullUrl, {
        ...options,
        signal: controller.signal,
      })
      
      clearTimeout(timeoutId)
      
      // If successful, cache this backend
      if (response.ok && typeof window !== 'undefined') {
        localStorage.setItem(WORKING_BACKEND_KEY, url)
        localStorage.setItem(`${WORKING_BACKEND_KEY}_time`, Date.now().toString())
      }
      
      // If not a network error, return the response (even if status is not ok)
      // This allows the caller to handle 4xx/5xx errors
      if (response.status !== 0) {
        return response
      }
      
      // If status is 0, it's a network error, try next backend
      lastError = new Error(`Network error: ${url}`)
    } catch (error: any) {
      lastError = error
      // Continue to next backend
      continue
    }
  }
  
  // All backends failed
  throw lastError || new Error('All backends are unavailable')
}

/**
 * Get current working backend URL (for display/debugging)
 */
export function getCurrentBackend(): string {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(WORKING_BACKEND_KEY) || BACKEND_URLS[0] || 'Not configured'
  }
  return BACKEND_URLS[0] || 'Not configured'
}

/**
 * Clear backend cache (force re-detection)
 */
export function clearBackendCache(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(WORKING_BACKEND_KEY)
    localStorage.removeItem(`${WORKING_BACKEND_KEY}_time`)
  }
}

// Export the fetch function
export { fetchWithFailover, getWorkingBackend }

