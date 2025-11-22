import { NextResponse } from 'next/server';
import { fetchWithFailover } from '@/lib/api-failover';

function buildQueryString(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.set(key, value);
    }
  });
  const queryString = searchParams.toString();
  return queryString ? `?${queryString}` : '';
}

export async function GET(request) {
  const clientId = request.nextUrl.searchParams.get('clientId');
  if (!clientId) {
    return NextResponse.json({ items: [], error: 'clientId is required' }, { status: 400 });
  }

  try {
    const queryString = buildQueryString({ client_id: clientId });
    const res = await fetchWithFailover(`/saved${queryString}`, {
      method: 'GET',
    });
    
    if (!res.ok) {
      throw new Error(`Backend returned ${res.status}`);
    }
    const json = await res.json();
    return NextResponse.json(json);
  } catch (err) {
    console.error('[api/saved] GET error:', err);
    return NextResponse.json({ items: [], error: err.message || 'Failed to load saved briefings.' }, { status: 200 });
  }
}

export async function POST(request) {
  try {
    const body = await request.json();
    if (!body?.client_id || !body?.link) {
      return NextResponse.json({ error: 'client_id and link are required' }, { status: 400 });
    }

    const res = await fetchWithFailover('/saved', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Backend returned ${res.status}: ${errorText}`);
    }

    const json = await res.json();
    return NextResponse.json(json);
  } catch (err) {
    console.error('[api/saved] POST error:', err);
    return NextResponse.json({ error: err.message || 'Failed to save briefing.' }, { status: 500 });
  }
}

export async function DELETE(request) {
  const { searchParams } = request.nextUrl;
  const clientId = searchParams.get('clientId');
  const link = searchParams.get('link');

  if (!clientId || !link) {
    return NextResponse.json({ error: 'clientId and link are required' }, { status: 400 });
  }

  try {
    const queryString = buildQueryString({ client_id: clientId, link });
    const res = await fetchWithFailover(`/saved${queryString}`, {
      method: 'DELETE',
    });
    
    if (!res.ok) {
      throw new Error(`Backend returned ${res.status}`);
    }
    const json = await res.json();
    return NextResponse.json(json);
  } catch (err) {
    console.error('[api/saved] DELETE error:', err);
    return NextResponse.json({ error: err.message || 'Failed to remove saved briefing.' }, { status: 500 });
  }
}
