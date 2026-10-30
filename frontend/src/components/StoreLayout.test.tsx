import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { StoreLayout } from './StoreLayout'
import { describe, it, expect } from 'vitest'

describe('StoreLayout Component', () => {
  it('renders header, main, and footer landmarks', () => {
    render(
      <MemoryRouter>
        <StoreLayout />
      </MemoryRouter>,
    )
    expect(screen.getByRole('banner')).toBeInTheDocument()
    expect(screen.getByRole('main')).toBeInTheDocument()
    expect(screen.getAllByRole('contentinfo').length).toBeGreaterThan(0)
  })

  it('renders the "Shop" logo link with href="/" using getByRole', () => {
    render(
      <MemoryRouter>
        <StoreLayout />
      </MemoryRouter>,
    )

    const logoLinks = screen.getAllByRole('link', { name: /shop/i })
    expect(logoLinks.length).toBeGreaterThan(0)
    expect(logoLinks[0]).toHaveAttribute('href', '/')
  })

  it('displays the current year and prices in uah in the footer', () => {
    const { container } = render(
      <MemoryRouter>
        <StoreLayout />
      </MemoryRouter>,
    )
    const currentYear = new Date().getFullYear().toString()
    const footer = container.querySelector('footer')

    expect(footer).toBeInTheDocument()
    expect(footer).toHaveTextContent(new RegExp(currentYear))
    expect(footer).toHaveTextContent(/prices in uah/i)
  })
})
