import { Outlet, Link } from 'react-router'
import { SkipLink } from './SkipLink'
import { BackendStatus } from './BackendStatus'

export function StoreLayout() {
  const currentYear = new Date().getFullYear()

  return (
    <div className="flex min-h-screen flex-col bg-ground text-ink">
      <SkipLink />

      <header className="border-b border-border bg-surface py-4">
        <div className="mx-auto flex w-full max-w-content items-center justify-between px-6">
          <Link
            to="/"
            className="text-2xl font-extrabold tracking-tight !text-ink no-underline hover:opacity-90"
          >
            Shop
          </Link>
        </div>
      </header>

      <main
        id="main-content"
        tabIndex={-1}
        className="mx-auto flex w-full max-w-content flex-1 flex-col px-6 py-8 outline-none"
      >
        <Outlet />
      </main>
      <footer className="border-t border-border bg-surface py-4">
        <div className="mx-auto flex w-full max-w-content flex-col items-center justify-between gap-2 px-6 sm:flex-row">
          <p className="text-sm text-muted">
            © {currentYear} Shop. Prices in UAH.
          </p>
          {import.meta.env.DEV && <BackendStatus />}
        </div>
      </footer>
    </div>
  )
}
