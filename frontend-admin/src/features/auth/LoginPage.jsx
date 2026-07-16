import { useState } from 'react';
import { Paper, Typography, TextField, Alert, Button } from '@mui/material';
import { useAuth } from '../../context/AuthContext';
import { sx } from '../../theme';

export function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim() || !password) {
      setError('Ingresa usuario y contraseña.');
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      await login(username.trim(), password);
    } catch (err) {
      setError(err.status === 401 ? 'Usuario o contraseña incorrectos.' : err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 24,
        boxSizing: 'border-box',
      }}
    >
      <Paper elevation={2} sx={sx.loginPaper}>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
            <div
              style={{
                width: 34,
                height: 34,
                borderRadius: 9,
                background: '#4f46e5',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff',
                fontWeight: 700,
                fontSize: 16,
              }}
            >
              R
            </div>
            <Typography variant="h6" sx={sx.title}>
              ResumeAI
            </Typography>
          </div>
          <Typography variant="body2" sx={sx.subtitle}>
            Generador automático de resúmenes vía RPA + IA
          </Typography>

          <div style={{ marginTop: 24, display: 'flex', flexDirection: 'column', gap: 16 }}>
            <TextField
              label="Usuario"
              placeholder="admin"
              fullWidth
              size="small"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <TextField
              label="Contraseña"
              type="password"
              placeholder="••••••••"
              fullWidth
              size="small"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            {error && <Alert severity="error">{error}</Alert>}

            <Button
              type="submit"
              variant="contained"
              fullWidth
              disableElevation
              disabled={submitting}
              sx={sx.primaryBtn}
            >
              {submitting ? 'Entrando…' : 'Iniciar sesión'}
            </Button>
          </div>
        </form>
      </Paper>
    </div>
  );
}
