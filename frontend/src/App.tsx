import { BackendStatus } from './components/BackendStatus'
function App() {
  return (
    <main className="mx-auto min-h-screen max-w-content p-6">
      <div className="rounded-card bg-surface p-6 shadow-raised">
        <h1>Shop</h1>
        <BackendStatus />
        <p className="text-body text-muted">
          Тестова сторінка перевірки стилів Tailwind CSS v4.
        </p>
      </div>
    </main>
  )
}
export default App
