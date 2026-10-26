import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { BackendStatus } from './BackendStatus';
import * as healthApi from '../api/health';

vi.mock('../api/health', () => ({
  getHealth: vi.fn(),
}));

describe('BackendStatus Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders checking state initially', () => {
    vi.spyOn(healthApi, 'getHealth').mockReturnValue(new Promise(() => {}));
    
    render(<BackendStatus />);
    
    expect(screen.getByText(/Checking backend…/i)).toBeInTheDocument();
  });

  it('renders "Backend: OK" when health check succeeds', async () => {
    vi.spyOn(healthApi, 'getHealth').mockResolvedValue({
      status: 'ok',
      database: 'ok',
    });

    render(<BackendStatus />);

    await waitFor(() => {
      expect(screen.getByText(/Backend: OK/i)).toBeInTheDocument();
    });
  });

  it('renders "Backend: unavailable" when health check fails', async () => {
    vi.spyOn(healthApi, 'getHealth').mockRejectedValue(new Error('Network error'));

    render(<BackendStatus />);

    await waitFor(() => {
      expect(screen.getByText(/Backend: unavailable/i)).toBeInTheDocument();
    });
  });
});