import type { ReactNode } from 'react'
import { Link, type LinkProps } from 'react-router-dom'

interface ButtonLinkProps extends LinkProps {
  children: ReactNode
  variant?: 'primary' | 'secondary'
}

export function ButtonLink({
  children,
  to,
  variant = 'primary',
  className = '',
  ...props
}: ButtonLinkProps) {
  const baseStyles =
    'inline-flex items-center justify-center h-[44px] px-6 rounded-control text-button font-bold transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2'

  const variantStyles =
    variant === 'primary'
      ? 'bg-primary text-primary-contrast hover:bg-primary-hover'
      : 'border border-border bg-surface text-ink hover:bg-ground'

  return (
    <Link
      to={to}
      className={`${baseStyles} ${variantStyles} ${className}`}
      {...props}
    >
      {children}
    </Link>
  )
}
