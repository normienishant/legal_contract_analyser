'use client';

export default function LoadingState({ message = 'Loading threat intelligence data...' }) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '400px',
        padding: '48px 24px',
        gap: 24,
      }}
    >
      <div
        style={{
          position: 'relative',
          width: 64,
          height: 64,
        }}
      >
        <div
          className="loading-spinner"
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            border: '4px solid rgba(37, 99, 235, 0.1)',
            borderTop: '4px solid #2563eb',
            borderRadius: '50%',
          }}
        />
      </div>
      
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 12,
          textAlign: 'center',
          maxWidth: '480px',
        }}
      >
        <h3
          style={{
            fontSize: '1.25rem',
            fontWeight: 600,
            color: 'var(--text-default)',
            margin: 0,
          }}
        >
          {message}
        </h3>
        <p
          style={{
            fontSize: '0.9rem',
            color: 'var(--text-muted)',
            margin: 0,
            lineHeight: 1.6,
          }}
        >
          Initial load may take 30-60 seconds as the backend service spins up on free tier hosting.
          <br />
          <span style={{ fontSize: '0.85rem', opacity: 0.8 }}>
            Please wait while we fetch the latest threat intelligence...
          </span>
        </p>
      </div>

      <div
        style={{
          display: 'flex',
          gap: 8,
          marginTop: 8,
        }}
      >
        <div
          className="loading-dot"
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: '#2563eb',
            animationDelay: '0s',
          }}
        />
        <div
          className="loading-dot"
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: '#2563eb',
            animationDelay: '0.2s',
          }}
        />
        <div
          className="loading-dot"
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: '#2563eb',
            animationDelay: '0.4s',
          }}
        />
      </div>
    </div>
  );
}

