import { useAuth } from './context/AuthContext';
import { LoginPage } from './features/auth/LoginPage';
import { Shell } from './features/shell/Shell';

export default function App() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Shell /> : <LoginPage />;
}
