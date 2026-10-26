export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string, options?: ErrorOptions) {
    super(message, options);
    this.name = 'ApiError';
    this.status = status;
  }
}

export async function apiGet<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(path, options);
  } catch (error) {
    
    if (error instanceof Error && error.name === 'AbortError') {
      throw error;
    }
  
    throw new ApiError(
      0,
      error instanceof Error ? error.message : 'Network error',
      { cause: error },
    );
  }

  if (!response.ok) {
    throw new ApiError(
      response.status,
      `HTTP error! status: ${response.status}`,
    );
  }

  return response.json();
}