import { type ReactNode } from 'react'
import { BackendStatus } from './BackendStatus'

interface StoreLayoutProps {
  children: ReactNode
}

export function StoreLayout({ children }: StoreLayoutProps) {
  return (
    <div className="min-h-screen bg-ground flex flex-col text-body text-main">
      <header className="border-b border-border bg-surface px-6 py-4 flex items-center justify-between">
        <a href="/" className="text-2xl font-extrabold tracking-tight text-main">
          Shop
        </a>
      </header>

      <main className="mx-auto w-full max-w-content flex-1 p-6">
        {children}
      </main>

      <footer className="border-t border-border bg-surface px-6 py-6 text-muted text-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <p>© {new Date().getFullYear()} Shop. Prices in UAH.</p>
        </div>
        {import.meta.env.DEV && <BackendStatus />}
      </footer>
    </div>
  )
}