// Normalize backend payloads (Spanish domain fields) into internal English models.

// Map the backend's canonical state (pendiente/procesado/fallido + sub_estado)
// to the UI vocabulary (buscando/resumiendo/listo/fallido).
function deriveStatus(raw) {
  if (raw.sub_estado) return raw.sub_estado; // buscando | resumiendo
  const state = raw.estado ?? raw.status;
  if (state === 'procesado' || state === 'listo') return 'listo';
  if (state === 'fallido') return 'fallido';
  if (state === 'resumiendo' || state === 'buscando') return state;
  if (state === 'pendiente') return 'buscando';
  // GET /books returns only published books without an explicit state field.
  return raw.resumen ? 'listo' : 'buscando';
}

export function toBook(raw) {
  if (!raw) return null;
  return {
    id: raw.id,
    title: raw.titulo ?? raw.title ?? '',
    price: Number(raw.precio ?? raw.price ?? 0),
    style: raw.estilo ?? raw.style ?? 'Formal',
    status: deriveStatus(raw),
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
