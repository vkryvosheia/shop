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

  const isOk = status === 'ok';

  return (
    <div role="status" className="my-2">
      {status === 'checking' && (
        <span className="text-sm text-gray-500">Checking backend…</span>
      )}

      {status !== 'checking' && (
        <span
          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            isOk
              ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
              : 'bg-red-100 text-red-800 border border-red-300'
          }`}
        >
          Backend: {isOk ? 'OK' : 'unavailable'}
        </span>
      )}
    </div>
  );
}