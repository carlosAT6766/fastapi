// Normalize backend payloads (Spanish domain fields) into internal English models.

export function toBook(raw) {
  if (!raw) return null;
  return {
    id: raw.id,
    title: raw.titulo ?? raw.title ?? '',
    price: Number(raw.precio ?? raw.price ?? 0),
    style: raw.estilo ?? raw.style ?? 'Formal',
    status: raw.estado ?? raw.status ?? 'buscando',
    summary: raw.resumen ?? raw.summary ?? '',
    log: raw.log ?? [],
    createdAt: raw.created_at ?? raw.createdAt ?? Date.now(),
  };
}

export function toSale(raw) {
  if (!raw) return null;
  return {
    id: raw.id,
    bookId: raw.libro_id ?? raw.bookId ?? null,
    bookTitle: raw.libro_titulo ?? raw.bookTitle ?? raw.titulo ?? '—',
    amount: Number(raw.monto ?? raw.amount ?? 0),
    date: raw.created_at ?? raw.date ?? Date.now(),
  };
}

export function toUser(raw) {
  if (!raw) return null;
  return {
    id: raw.id,
    name: raw.nombre ?? raw.name ?? '',
    email: raw.email ?? '',
    role: raw.rol ?? raw.role ?? 'Lector',
    active: raw.activo ?? raw.active ?? true,
  };
}
