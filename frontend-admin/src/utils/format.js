export function formatPrice(value) {
  return '$' + (Number(value) || 0).toFixed(2);
}

export function formatTime(ts) {
  return new Date(ts).toLocaleTimeString('es-MX', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

export function formatDateTime(ts) {
  return new Date(ts).toLocaleString('es-MX', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });
}
