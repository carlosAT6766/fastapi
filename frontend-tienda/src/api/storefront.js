import { apiClient } from './client';

// Public real-time catalog stream. The backend broadcasts a message whenever the
// catalog changes (e.g. a book is published), and we let the caller react
// (typically by refetching the published books). Auto-reconnects with backoff.
export function connectStorefront(onChange) {
  const wsUrl = `${apiClient.API_URL.replace(/^http/, 'ws')}/storefront/stream`;
  let socket = null;
  let closedByClient = false;
  let retry = 0;

  const open = () => {
    socket = new WebSocket(wsUrl);
    socket.onopen = () => {
      retry = 0;
    };
    socket.onmessage = () => onChange?.();
    socket.onclose = () => {
      if (closedByClient) return;
      retry += 1;
      setTimeout(open, Math.min(1000 * retry, 8000));
    };
    socket.onerror = () => socket && socket.close();
  };

  open();

  return () => {
    closedByClient = true;
    socket && socket.close();
  };
}
