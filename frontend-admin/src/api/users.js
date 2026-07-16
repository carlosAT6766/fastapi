import { apiClient } from './client';
import { toUser } from './mappers';

// GET /users
export async function fetchUsers() {
  const data = await apiClient.get('/users');
  const list = Array.isArray(data) ? data : (data.items ?? []);
  return list.map(toUser);
}

// POST /users
export async function createUser({ name, email, role }) {
  const raw = await apiClient.post('/users', { nombre: name, email, rol: role });
  return toUser(raw);
}

// PATCH /users/{id} -> toggle active / edit
export async function updateUser(id, patch) {
  const body = {};
  if (patch.active !== undefined) body.activo = patch.active;
  if (patch.name !== undefined) body.nombre = patch.name;
  if (patch.role !== undefined) body.rol = patch.role;
  const raw = await apiClient.patch(`/users/${id}`, body);
  return toUser(raw);
}

// DELETE /users/{id}
export async function deleteUser(id) {
  await apiClient.del(`/users/${id}`);
}
