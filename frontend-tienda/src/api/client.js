const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8080').replace(/\/$/, '');
const EXPLICIT_TOKEN = import.meta.env.VITE_CUSTOMER_TOKEN || '';
const CUSTOMER_EMAIL = import.meta.env.VITE_CUSTOMER_EMAIL || 'customer@resumeai.com';
const CUSTOMER_PASSWORD = import.meta.env.VITE_CUSTOMER_PASSWORD || 'customer123';

// The storefront is public (no login UI) but the sale endpoint requires auth.
// We transparently sign in as the seeded customer and cache the token in memory.
let cachedToken = EXPLICIT_TOKEN;
let pendingLogin = null;

async function login() {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: CUSTOMER_EMAIL, password: CUSTOMER_PASSWORD }),
  });
  if (!response.ok) throw new Error(`Customer login failed (${response.status})`);
  const data = await response.json();
  return data.access_token || data.token;
}

async function getToken() {
  if (cachedToken) return cachedToken;
  if (!pendingLogin) pendingLogin = login().then((token) => (cachedToken = token));
  return pendingLogin;
}

async function request(path, { method = 'GET', body, headers, auth = false } = {}) {
  const finalHeaders = { 'Content-Type': 'application/json', ...headers };
  if (auth) {
    const token = await getToken().catch(() => '');
    if (token) finalHeaders.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: finalHeaders,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => '');
    throw new Error(`API ${method} ${path} failed (${response.status}): ${detail}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

export const apiClient = { request, API_URL };
