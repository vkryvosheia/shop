import { describe, it, expect, vi, beforeEach } from 'vitest'
import { apiGet, ApiError } from './client'

describe('apiGet client', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('returns parsed JSON when response is ok (status 200)', async () => {
    const mockData = { status: 'ok', database: 'ok' }

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockData,
      })
    )

    const result = await apiGet('/api/health')
    expect(result).toEqual(mockData)
    expect(fetch).toHaveBeenCalledWith('/api/health', undefined)
  })

  it('throws ApiError when response is not ok (status 500)', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
      })
    )

    await expect(apiGet('/api/health')).rejects.toThrow(ApiError)
    
    try {
      await apiGet('/api/health')
    } catch (error) {
      expect(error).toBeInstanceOf(ApiError)
      if (error instanceof ApiError) {
        expect(error.status).toBe(500)
        expect(error.message).toBe('HTTP error! status: 500')
      }
    }
  })
})