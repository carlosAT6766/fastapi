import { apiClient } from './client';

function newIdempotencyKey() {
  if (globalThis.crypto?.randomUUID) {
    return globalThis.crypto.randomUUID();
  }
  return `sale-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

export async function purchaseBook(book) {
  return apiClient.request('/transactions/create', {
    method: 'POST',
    auth: true,
    headers: { 'Idempotency-Key': newIdempotencyKey() },
    body: {
      monto: book.price,
      tipo: 'venta',
      libro_id: book.id,
    },
  });
}
