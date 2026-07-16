import { getBaseUrl, getToken } from './client';
import { toBook } from './mappers';

// Live book state via WebSocket /transactions/stream.
// Auth travels as a subprotocol (T4): the token is the second subprotocol value.
// Auto-reconnects with a small backoff.

function wsUrl() {
  const base = getBaseUrl().replace(/^http/, 'ws');
  return `${base}/transactions/stream`;
}

export function connectStream({ onBook, onSale, onLog, onStatus }) {
  let socket = null;
  let closedByClient = false;
  let retry = 0;

  const open = () => {
    const token = getToken();
    // Subprotocols: a marker + the JWT (backend reads the token from the protocol header).
    socket = new WebSocket(wsUrl(), token ? ['bearer', token] : undefined);

    socket.onopen = () => {
      retry = 0;
      onStatus?.('open');
    };

    socket.onmessage = (event) => {
      let msg;
      try {
        msg = JSON.parse(event.data);
      } catch {
        return;
      }
      // Wrapped envelope: { type: 'book'|'sale'|'log', payload }
      if (msg.type === 'book') onBook?.(toBook(msg.payload));
      else if (msg.type === 'sale') onSale?.(msg.payload);
      else if (msg.type === 'log') onLog?.(msg.payload); // { id, line }
      // Flat backend envelope (transaction_event): route by `tipo`.
      else if (msg.tipo === 'venta') onSale?.(msg);
      else if (msg.tipo === 'libro' || msg.titulo) onBook?.(toBook(msg));
    };

    socket.onclose = () => {
      onStatus?.('closed');
      if (closedByClient) return;
      retry += 1;
      const delay = Math.min(1000 * retry, 8000);
      setTimeout(open, delay);
    };

    socket.onerror = () => socket && socket.close();
  };

  open();

  return () => {
    closedByClient = true;
    socket && socket.close();
  };
}
