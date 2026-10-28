import { StoreLayout } from './components/StoreLayout'

function App() {
  return (
    <StoreLayout>
      <div className="space-y-4 rounded-card bg-surface p-6 shadow-raised">
        <h1 className="text-2xl font-bold">Shop</h1>
        <p className="text-body text-muted">
          Тестова сторінка перевірки стилів Tailwind CSS v4.
        </p>
      </div>
    </StoreLayout>
  )
}

export default App
