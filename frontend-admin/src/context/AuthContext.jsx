import { createContext, useContext, useMemo, useState } from 'react';
import { getToken } from '../api/client';
import { login as apiLogin, logout as apiLogout } from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setTokenState] = useState(() => getToken());

  const value = useMemo(
    () => ({
      isAuthenticated: Boolean(token),
      async login(username, password) {
        const newToken = await apiLogin(username, password);
        setTokenState(newToken);
      },
      logout() {
        apiLogout();
        setTokenState(null);
      },
    }),
    [token],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
