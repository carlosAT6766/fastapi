import { apiClient, setToken, clearToken } from './client';

// POST /auth/login -> { access_token, token_type }
export async function login(username, password) {
  const data = await apiClient.post('/auth/login', { username, password });
  const token = data.access_token || data.token;
  if (!token) throw new Error('La respuesta de login no incluyó un token.');
  setToken(token);
  return token;
}

export function logout() {
  clearToken();
}
