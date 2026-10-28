import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { StoreLayout } from './StoreLayout'

vi.mock('../api/health', () => ({
  getHealth: vi.fn().mockResolvedValue({ status: 'ok', database: 'ok' }),
}))

describe('StoreLayout Component', () => {
  it('renders header, main, and footer elements', () => {
    const { container } = render(
      <StoreLayout>
        <p>Test Content</p>
      </StoreLayout>,
    )

    expect(container.querySelector('header')).toBeInTheDocument()
    expect(container.querySelector('main')).toBeInTheDocument()
    expect(container.querySelector('footer')).toBeInTheDocument()
    expect(screen.getByText('Test Content')).toBeInTheDocument()
  })

  it('renders the "Shop" logo link with href="/"', () => {
    const { container } = render(
      <StoreLayout>
        <p>Content</p>
      </StoreLayout>,
    )

    const logoLink = container.querySelector('header a')
    expect(logoLink).toBeInTheDocument()
    expect(logoLink).toHaveAttribute('href', '/')
    expect(logoLink).toHaveTextContent(/shop/i)
  })

  it('displays the current year and prices in uah in the footer', () => {
    const { container } = render(
      <StoreLayout>
        <p>Content</p>
      </StoreLayout>,
    )

    const footer = container.querySelector('footer')
    const currentYear = new Date().getFullYear().toString()

    expect(footer).toHaveTextContent(currentYear)
    expect(footer).toHaveTextContent(/prices in uah/i)
  })
})
