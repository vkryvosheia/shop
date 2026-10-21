import { useEffect, useState } from 'react';
import { getHealth } from '../api/health';

export function BackendStatus() {
  const [status, setStatus] = useState<'checking' | 'ok' | 'unavailable'>('checking');

  useEffect(() => {
    const controller = new AbortController();

    getHealth(controller.signal)
      .then((data) => {
        if (data.status === 'ok' && data.database === 'ok') {
          setStatus('ok');
        } else {
          setStatus('unavailable');
        }
      })
      .catch((err) => {
        if (err.name !== 'AbortError') {
          setStatus('unavailable');
        }
      });

    return () => {
      controller.abort();
    };
  }, []);

  if (!import.meta.env.DEV) {
    return null;
  }

  if (status === 'checking') {
    return (
      <div role="status" className="text-body text-muted my-2">
        Checking backend…
      </div>
    );
  }

  const isOk = status === 'ok';

  return (
    <div
      role="status"
      style={{
        display: 'inline-block',
        padding: '0.25rem 0.75rem',
        borderRadius: '9999px',
        fontSize: '0.875rem',
        fontWeight: 500,
        marginTop: '0.5rem',
        marginBottom: '0.5rem',
        backgroundColor: isOk ? '#d1fae5' : '#fee2e2',
        border: `1px solid ${isOk ? '#a7f3d0' : '#fca5a5'}`,
        color: isOk ? '#065f46' : '#991b1b',
      }}
    >
      Backend: {isOk ? 'OK' : 'unavailable'}
    </div>
  );
}