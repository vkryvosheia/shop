import { describe, it, expect, afterEach } from 'vitest'
import { render, screen, cleanup } from '@testing-library/react'
import { StoreLayout } from './StoreLayout'

afterEach(() => {
  cleanup()
})

describe('StoreLayout Component', () => {
  it('renders header, main, and footer landmarks', () => {
    render(
      <StoreLayout>
        <p>Test Content</p>
      </StoreLayout>
    )

    expect(screen.getByRole('banner')).toBeInTheDocument()
    expect(screen.getByRole('main')).toBeInTheDocument()
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
    expect(screen.getByText('Test Content')).toBeInTheDocument()
  })

  it('renders the "Shop" logo link with href="/" using getByRole', () => {
    render(
      <StoreLayout>
        <p>Test Content</p>
      </StoreLayout>
    )

    const logoLink = screen.getByRole('link', { name: 'Shop' })
    expect(logoLink).toBeInTheDocument()
    expect(logoLink).toHaveAttribute('href', '/')
  })

  it('displays the current year and prices in uah in the footer', () => {
    render(
      <StoreLayout>
        <p>Test Content</p>
      </StoreLayout>
    )

    const footer = screen.getByRole('contentinfo')
    const currentYear = new Date().getFullYear().toString()

    expect(footer).toHaveTextContent(currentYear)
    expect(footer).toHaveTextContent(/prices in uah/i)
  })
})