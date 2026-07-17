import { apiClient } from './client';
import { toSale } from './mappers';

// GET /sales -> registered sales (tipo="venta")
export async function fetchSales() {
  const data = await apiClient.get('/sales');
  const list = Array.isArray(data) ? data : (data.sales ?? data.items ?? []);
  return list.map(toSale);
}
