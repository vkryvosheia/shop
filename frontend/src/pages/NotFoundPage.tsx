import { useEffect } from 'react'
import { NotFound } from '../components/NotFound'

export function NotFoundPage() {
  useEffect(() => {
    document.title = 'Page not found · Shop'
  }, [])

  return (
    <NotFound
      heading="Page not found"
      message="The page you are looking for does not exist or has been moved."
    />
  )
}
