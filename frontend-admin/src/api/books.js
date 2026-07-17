import { apiClient } from './client';
import { toBook } from './mappers';

// GET /books -> list of book transactions (tipo="libro")
export async function fetchBooks() {
  const data = await apiClient.get('/books');
  const list = Array.isArray(data) ? data : (data.items ?? []);
  return list.map(toBook);
}

// POST /transactions/async-process -> enqueue RPA + summarize job
export async function createBook({ title, price, style }) {
  const raw = await apiClient.post('/transactions/async-process', {
    tipo: 'libro',
    titulo: title,
    precio: Number(price) || 0,
    estilo: style,
  });
  return toBook(raw);
}

// POST /books/{id}/publish -> make a ready book visible in the storefront
export async function publishBook(id) {
  const raw = await apiClient.post(`/books/${id}/publish`, {});
  return toBook(raw);
}

// PATCH /books/{id} -> edit a book (title/price/style/summary)
export async function updateBook(id, { title, price, style, summary }) {
  const raw = await apiClient.patch(`/books/${id}`, {
    titulo: title,
    precio: Number(price) || 0,
    estilo: style,
    resumen: summary,
  });
  return toBook(raw);
}
