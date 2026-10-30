import { useEffect } from 'react'

export function HomePage() {
  useEffect(() => {
    document.title = 'Shop'
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-extrabold tracking-tight text-ink">
        Store Catalog
      </h1>
    </div>
  )
}
