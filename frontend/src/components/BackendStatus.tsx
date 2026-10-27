import { useEffect, useState } from 'react'
import { getHealth } from '../api/health'

export function BackendStatus() {
  const [status, setStatus] = useState<'checking' | 'ok' | 'unavailable'>(
    'checking',
  )

  useEffect(() => {
    const controller = new AbortController()

    getHealth(controller.signal)
      .then((data) => {
        if (data.status === 'ok' && data.database === 'ok') {
          setStatus('ok')
        } else {
          setStatus('unavailable')
        }
      })
      .catch((err) => {
        if (err.name !== 'AbortError') {
          setStatus('unavailable')
        }
      })

    return () => {
      controller.abort()
    }
  }, [])

  const isOk = status === 'ok'

  return (
    <div role="status" className="my-2">
      {status === 'checking' && (
        <span className="text-small text-muted">Checking backend...</span>
      )}

      {status !== 'checking' && (
        <span
          className={`inline-flex items-center rounded-control px-2.5 py-0.5 text-badge ${
            isOk ? 'bg-success-tint text-success' : 'bg-danger-tint text-danger'
          }`}
        >
          Backend: {isOk ? 'OK' : 'unavailable'}
        </span>
      )}
    </div>
  )
}
