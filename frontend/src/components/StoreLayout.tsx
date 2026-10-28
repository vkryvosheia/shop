import type { ReactNode } from 'react'
import { BackendStatus } from './BackendStatus'

interface StoreLayoutProps {
  children: ReactNode
}

export function StoreLayout({ children }: StoreLayoutProps) {
  const currentYear = new Date().getFullYear()

  return (
    <div className="bg-background flex min-h-screen flex-col text-ink">
      <header className="border-b border-border bg-surface">
        <div className="mx-auto flex h-16 max-w-content items-center px-6">
          <a
            href="/"
            className="text-2xl font-extrabold text-ink transition-opacity hover:opacity-90"
          >
            Shop
          </a>
        </div>
      </header>

      <main className="mx-auto w-full max-w-content flex-1 px-6 py-8">
        {children}
      </main>

      <footer className="mt-auto border-t border-border bg-surface">
        <div className="mx-auto flex max-w-content flex-col items-center justify-between gap-4 px-6 py-4 text-small text-muted sm:flex-row">
          <div>© {currentYear} Shop</div>

          <div className="flex items-center gap-4">
            <BackendStatus />
            <span>Prices in UAH</span>
          </div>
        </div>
      </footer>
    </div>
  )
}
