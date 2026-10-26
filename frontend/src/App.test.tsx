import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import App from './App.tsx'

vi.mock('./api/health', () => ({
  getHealth: vi.fn().mockResolvedValue({ status: 'ok', database: 'ok' }),
}))

describe('App', () => {
  it('renders the shop heading', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'Shop' })).toBeInTheDocument()
  })
})
