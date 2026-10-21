import { apiGet } from './client';

export type Health = {
  status: 'ok' | 'error';
  database: 'ok' | 'unavailable';
};

export async function getHealth(signal?: AbortSignal): Promise<Health> {
  return apiGet<Health>('/api/health', { signal });
}