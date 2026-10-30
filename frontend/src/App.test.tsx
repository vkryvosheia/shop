import { render, screen } from '@testing-library/react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { describe, it, expect } from 'vitest'
import { StoreLayout } from './components/StoreLayout'
import { HomePage } from './pages/HomePage'
import { NotFoundPage } from './pages/NotFoundPage'

const createTestRouter = (initialEntry: string) =>
  createMemoryRouter(
    [
      {
        path: '/',
        element: <StoreLayout />,
        children: [
          { index: true, element: <HomePage /> },
          { path: '*', element: <NotFoundPage /> },
        ],
      },
    ],
    { initialEntries: [initialEntry] },
  )

describe('Routing and 404 Tests', () => {
  it('shows home heading on / and correct links', () => {
    const router = createTestRouter('/')
    render(<RouterProvider router={router} />)

    expect(
      screen.getByRole('heading', { name: /Store Catalog/i }),
    ).toBeInTheDocument()

    const logoLink = screen.getByRole('link', { name: /^Shop$/i })
    expect(logoLink).toHaveAttribute('href', '/')
  })

  it('shows 404 heading on /does-not-exist and links point to the right URLs', () => {
    const router = createTestRouter('/does-not-exist')
    render(<RouterProvider router={router} />)

    expect(
      screen.getByRole('heading', { name: /Page not found/i }),
    ).toBeInTheDocument()

    const browseLink = screen.getByRole('link', {
      name: /Browse all products/i,
    })
    expect(browseLink).toBeInTheDocument()
    expect(browseLink).toHaveAttribute('href', '/products')

    const homeLink = screen.getByRole('link', { name: /Go to home page/i })
    expect(homeLink).toBeInTheDocument()
    expect(homeLink).toHaveAttribute('href', '/')
  })
})
