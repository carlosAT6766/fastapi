import { apiClient } from './client';

const PREVIEW_LENGTH = 130;

function toPreview(summary = '') {
  const text = summary || '';
  return text.length > PREVIEW_LENGTH ? `${text.slice(0, PREVIEW_LENGTH)}…` : text;
}

function normalizeBook(raw) {
  const price = Number(raw.precio ?? raw.price ?? 0);
  return {
    id: raw.id,
    title: raw.titulo ?? raw.tema ?? raw.title ?? 'Sin título',
    style: raw.estilo ?? raw.style ?? '',
    price,
    priceLabel: `$${price.toFixed(2)}`,
    preview: toPreview(raw.resumen ?? raw.summary ?? ''),
  };
}

function isPublished(book) {
  return book.estado === 'listo' && Number(book.precio ?? book.price ?? 0) > 0;
}

export async function fetchPublishedBooks() {
  const data = await apiClient.request('/books?estado=listo');
  const list = Array.isArray(data) ? data : (data?.items ?? []);
  return list.filter(isPublished).map(normalizeBook);
}
