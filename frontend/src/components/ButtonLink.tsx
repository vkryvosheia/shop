import type { ReactNode } from 'react'
import { Link, type LinkProps } from 'react-router'
import { buttonBaseStyles, buttonVariantStyles } from './buttonStyles'

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
  const variantStyles = buttonVariantStyles[variant]

  return (
    <Link
      to={to}
      className={`${buttonBaseStyles} ${variantStyles} ${className}`}
      {...props}
    >
      {children}
    </Link>
  )
}
