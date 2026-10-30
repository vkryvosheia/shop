import { render, screen } from '@testing-library/react'
import App from './App'
import { describe, it, expect } from 'vitest'

describe('App', () => {
  it('renders store catalog page on default route', () => {
    render(<App />)
    expect(screen.getByText(/store catalog page/i)).toBeInTheDocument()
  })
})
