import { useEffect } from 'react'
import { ButtonLink } from '../components/Button'

interface NotFoundProps {
  title?: string
  message?: string
}

export function NotFound({
  title = 'Page not found',
  message = 'The page you are looking for does not exist or has been moved.',
}: NotFoundProps) {
  useEffect(() => {
    document.title = 'Page not found · Shop'
  }, [])

  return (
    <div className="flex items-center justify-center py-12">
      <div className="w-full max-w-lg rounded-card border border-border bg-surface p-8 text-center shadow-sm">
        <span className="text-subtle text-xs font-semibold tracking-wider uppercase">
          Error 404
        </span>
        <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-ink sm:text-4xl">
          {title}
        </h1>
        <p className="text-subtle mt-4 text-base">{message}</p>

        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <ButtonLink
            to="/products"
            variant="primary"
            className="w-full sm:w-auto"
          >
            Browse all products
          </ButtonLink>
          <ButtonLink to="/" variant="secondary" className="w-full sm:w-auto">
            Go to home page
          </ButtonLink>
        </div>
      </div>
    </div>
  )
}
