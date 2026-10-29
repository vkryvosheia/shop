import type { ReactNode } from 'react'
import { BackendStatus } from './BackendStatus'

interface StoreLayoutProps {
  children: ReactNode
}

export function StoreLayout({ children }: StoreLayoutProps) {
  return (
    <div className="flex min-h-screen flex-col bg-ground text-body">
      <header className="border-b border-border bg-surface py-4">
        <div className="mx-auto flex w-full max-w-content items-center justify-between px-6">
          <a
            href="/"
            className="text-2xl font-extrabold tracking-tight !text-ink no-underline hover:opacity-90"
          >
            Shop
          </a>
        </div>
      </header>

      <main className="mx-auto w-full max-w-content flex-1 p-6">
        {children}
      </main>

      <footer className="flex flex-col items-start justify-between gap-4 border-t border-border bg-surface px-6 py-6 text-sm sm:flex-row sm:items-center">
        <div>
          <p>© {new Date().getFullYear()} Shop. Prices in UAH.</p>
        </div>
        {import.meta.env.DEV && <BackendStatus />}
      </footer>
    </div>
  )
}
