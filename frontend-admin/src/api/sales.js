import { apiClient } from './client';
import { toSale } from './mappers';

// GET /sales -> registered sales (tipo="venta")
export async function fetchSales() {
  const data = await apiClient.get('/sales');
  const list = Array.isArray(data) ? data : (data.sales ?? data.items ?? []);
  return list.map(toSale);
}

// POST /transactions/create -> idempotent sale of a "listo" book.
// Requires an Idempotency-Key header (T2).
export async function sellBook(book) {
  const raw = await apiClient.post(
    '/transactions/create',
    { tipo: 'venta', monto: Number(book.price), libro_id: book.id },
    { headers: { 'Idempotency-Key': crypto.randomUUID() } },
  );
  return toSale(raw);
}
