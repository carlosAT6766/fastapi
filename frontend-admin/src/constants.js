// Select options and status metadata shared across screens.

export const STYLE_OPTIONS = [
  { value: 'Formal', label: 'Formal' },
  { value: 'Casual', label: 'Casual' },
  { value: 'Técnico', label: 'Técnico' },
  { value: 'Ejecutivo', label: 'Ejecutivo (breve)' },
  { value: 'Divertido', label: 'Divertido' },
];

export const SOURCE_OPTIONS = [
  { value: 'Wikipedia (ES)', label: 'Wikipedia (Español)' },
  { value: 'Wikipedia (EN)', label: 'Wikipedia (Inglés)' },
  { value: 'Wikipedia (PT)', label: 'Wikipedia (Portugués)' },
];

export const ROLE_OPTIONS = [
  { value: 'Admin', label: 'Admin' },
  { value: 'Editor', label: 'Editor' },
  { value: 'Lector', label: 'Lector' },
];

// Backend "estado" -> chip label + MUI color.
const STATUS_META = {
  buscando: { label: 'buscando', color: 'warning' },
  resumiendo: { label: 'resumiendo', color: 'info' },
  listo: { label: 'listo', color: 'success' },
  fallido: { label: 'fallido', color: 'error' },
};

export function statusInfo(status) {
  return STATUS_META[status] || STATUS_META.buscando;
}

export const NAV_ITEMS = [
  { key: 'books', label: 'Libros' },
  { key: 'sales', label: 'Ventas' },
  { key: 'config', label: 'Configuración' },
  { key: 'users', label: 'Usuarios' },
];
