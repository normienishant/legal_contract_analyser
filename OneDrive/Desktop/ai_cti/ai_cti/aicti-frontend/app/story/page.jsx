import { Suspense } from 'react';
import StoryClient from './StoryClient';
import { fetchWithFailover } from '@/lib/api-failover';

async function fetchArticle(link) {
  if (!link) return null;
  try {
    // Use failover system for backend calls
    const res = await fetchWithFailover(`/article?link=${encodeURIComponent(link)}`, {
      method: 'GET',
    });
    if (!res.ok) return null;
    const json = await res.json();
    return json.article || null;
  } catch (err) {
    console.error('[story/page] Error fetching article:', err);
    return null;
  }
}

function StoryFallback() {
  return (
    <section className="container" style={{ padding: '60px 24px', maxWidth: 900 }}>
      <div className="sidebar-card">Preparing intelligence briefing…</div>
    </section>
  );
}

export default async function StoryPage({ searchParams }) {
  const link = searchParams?.link || '';
  const serverArticle = await fetchArticle(link);

  return (
    <Suspense fallback={<StoryFallback />}>
      <StoryClient initialArticle={serverArticle} linkParam={link} />
    </Suspense>
  );
}
