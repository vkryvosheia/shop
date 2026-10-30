import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { buttonBaseStyles, buttonVariantStyles } from './buttonStyles'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  variant = 'primary',
  className = '',
  ...props
}: ButtonProps) {
  const variantStyles = buttonVariantStyles[variant]

  return (
    <button
      className={`${buttonBaseStyles} ${variantStyles} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
