export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiGet<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  let response: Response

  try {
    response = await fetch(path, options)
  } catch (error) {
    throw new ApiError(
      0,
      error instanceof Error ? error.message : 'Network error',
    )
  }

  if (!response.ok) {
    throw new ApiError(
      response.status,
      `HTTP error! status: ${response.status}`,
    )
  }

  return response.json()
}
