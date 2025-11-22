import { NextResponse } from 'next/server';
import { fetchWithFailover } from '@/lib/api-failover';

export async function GET(request) {
  const { searchParams } = request.nextUrl;
  const clientId = searchParams.get('clientId');

  if (!clientId) {
    return NextResponse.json({ error: 'clientId is required' }, { status: 400 });
  }

  try {
    const res = await fetchWithFailover(`/export/pdf?client_id=${encodeURIComponent(clientId)}`, {
      method: 'GET',
    });

    if (!res.ok) {
      throw new Error(`Backend returned ${res.status}`);
    }

    const blob = await res.blob();
    return new NextResponse(blob, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="ai-cti-briefings-${new Date().toISOString().split('T')[0]}.pdf"`,
      },
    });
  } catch (err) {
    console.error('[api/export/pdf] Error:', err);
    return NextResponse.json({ error: err.message || 'Failed to generate PDF.' }, { status: 500 });
  }
}


