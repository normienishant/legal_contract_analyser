/*
 app/api/results/route.js
 Server-side proxy: forwards requests with automatic failover (Railway → Render)
*/
import { fetchWithFailover } from '@/lib/api-failover';

export async function GET(request) {
  try {
    const res = await fetchWithFailover('/results', {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache, no-store, must-revalidate",
      },
    });
    
    const json = await res.json();
    return new Response(JSON.stringify(json), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  } catch (err) {
    console.error("[api/results] Error after failover:", err);
    const errorMsg = err?.name === 'AbortError' 
      ? "Backend is taking too long to respond. It might be spinning up (free tier). Please wait 30-60 seconds and refresh."
      : err?.message || "Failed to connect to backend after failover attempts";
    
    // Return empty data structure instead of error to prevent frontend crash
    return new Response(JSON.stringify({ 
      iocs: [],
      clusters: {},
      feeds: [],
      error: errorMsg 
    }), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  }
}
