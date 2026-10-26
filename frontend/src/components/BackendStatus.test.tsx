import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { BackendStatus } from './BackendStatus'
import * as healthApi from '../api/health'

vi.mock('../api/health', () => ({
  getHealth: vi.fn(),
}))

const mockedGetHealth = vi.mocked(healthApi.getHealth)

describe('BackendStatus Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders checking state initially and checks muted text style', () => {
    mockedGetHealth.mockReturnValue(new Promise(() => {}))
    render(<BackendStatus />)

    const checkingText = screen.getByText(/Checking backend.../i)
    expect(checkingText).toBeInTheDocument()
    expect(checkingText).toHaveClass('text-muted')
  })

  it('renders "Backend: OK" with success badge styles when health check succeeds', async () => {
    mockedGetHealth.mockResolvedValue({
      status: 'ok',
      database: 'ok',
    })

    render(<BackendStatus />)

    await waitFor(() => {
      const badge = screen.getByText(/Backend: OK/i)
      expect(badge).toBeInTheDocument()
      expect(badge).toHaveClass('bg-success-tint', 'text-success')
    })
  })

  it('renders "Backend: unavailable" with danger badge styles on 503/500 error', async () => {
    mockedGetHealth.mockRejectedValue(new Error('Service Unavailable'))

    render(<BackendStatus />)

    await waitFor(() => {
      const badge = screen.getByText(/Backend: unavailable/i)
      expect(badge).toBeInTheDocument()
      expect(badge).toHaveClass('bg-danger-tint', 'text-danger')
    })
  })
})