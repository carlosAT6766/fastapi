import { apiClient } from './client';

// GET /settings -> { fuente_default, estilo_default }
export async function fetchSettings() {
  const data = await apiClient.get('/settings');
  return {
    defaultSource: data.fuente_default ?? data.defaultSource ?? 'Wikipedia (ES)',
    defaultStyle: data.estilo_default ?? data.defaultStyle ?? 'Formal',
  };
}

// PUT /settings
export async function saveSettings({ defaultSource, defaultStyle }) {
  await apiClient.put('/settings', {
    fuente_default: defaultSource,
    estilo_default: defaultStyle,
  });
}
