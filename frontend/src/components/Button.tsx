import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { Link, type LinkProps } from 'react-router-dom'

type ButtonVariant = 'primary' | 'secondary'

interface ButtonBaseProps {
  variant?: ButtonVariant
  children: ReactNode
  className?: string
}

export type ButtonProps = ButtonBaseProps &
  ButtonHTMLAttributes<HTMLButtonElement>
export type ButtonLinkProps = ButtonBaseProps & LinkProps

const baseStyles =
  'inline-flex items-center justify-center h-11 px-6 rounded-control text-button font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 no-underline'

const variantStyles: Record<ButtonVariant, string> = {
  primary: 'bg-primary text-surface hover:bg-primary-hover shadow-sm',
  secondary:
    'bg-surface text-ink border border-border hover:bg-ground shadow-sm',
}

export function Button({
  variant = 'primary',
  children,
  className = '',
  ...rest
}: ButtonProps) {
  const combinedStyles = `${baseStyles} ${variantStyles[variant]} ${className}`
  return (
    <button className={combinedStyles} {...rest}>
      {children}
    </button>
  )
}

export function ButtonLink({
  variant = 'primary',
  children,
  className = '',
  to,
  ...rest
}: ButtonLinkProps) {
  const combinedStyles = `${baseStyles} ${variantStyles[variant]} ${className}`
  return (
    <Link to={to} className={combinedStyles} {...rest}>
      {children}
    </Link>
  )
}
