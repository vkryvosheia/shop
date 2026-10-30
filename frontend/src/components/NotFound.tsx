import { ButtonLink } from './ButtonLink'

interface NotFoundProps {
  heading: string
  message: string
}

export function NotFound({ heading, message }: NotFoundProps) {
  return (
    <div className="mx-auto max-w-xl rounded-card border border-border bg-surface p-8 text-center shadow-raised sm:p-12">
      <span className="text-label tracking-wider text-muted uppercase">
        Error 404
      </span>
      <h1 className="mt-3 text-2xl font-extrabold tracking-tight text-ink sm:text-3xl">
        {heading}
      </h1>
      <p className="mt-3 text-body text-muted">{message}</p>
      <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
        <ButtonLink to="/products" variant="primary">
          Browse all products
        </ButtonLink>
        <ButtonLink to="/" variant="secondary">
          Go to home page
        </ButtonLink>
      </div>
    </div>
  )
}
