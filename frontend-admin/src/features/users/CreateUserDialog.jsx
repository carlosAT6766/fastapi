import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button } from '@mui/material';
import { SelectField } from '../../components/SelectField';
import { ROLE_OPTIONS } from '../../constants';
import { sx } from '../../theme';

export function CreateUserDialog({ open, onClose, onSubmit }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('Lector');

  useEffect(() => {
    if (open) {
      setName('');
      setEmail('');
      setRole('Lector');
    }
  }, [open]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim() || !email.trim()) return;
    onSubmit({ name: name.trim(), email: email.trim(), role });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <form onSubmit={handleSubmit}>
        <DialogTitle sx={sx.dialogTitle}>Nuevo usuario</DialogTitle>
        <DialogContent>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 18, paddingTop: 6 }}>
            <TextField
              label="Nombre"
              autoFocus
              fullWidth
              size="small"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <TextField
              label="Email"
              type="email"
              fullWidth
              size="small"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <SelectField
              label="Rol"
              fullWidth
              size="small"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              options={ROLE_OPTIONS}
            />
          </div>
        </DialogContent>
        <DialogActions sx={sx.dialogActions}>
          <Button variant="text" onClick={onClose} sx={sx.cancelBtn}>
            Cancelar
          </Button>
          <Button type="submit" variant="contained" disableElevation sx={sx.primaryBtn}>
            Crear usuario
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
