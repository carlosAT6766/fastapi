import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button } from '@mui/material';
import { SelectField } from '../../components/SelectField';
import { STYLE_OPTIONS } from '../../constants';
import { sx } from '../../theme';

export function CreateBookDialog({ open, defaultStyle, onClose, onSubmit }) {
  const [title, setTitle] = useState('');
  const [price, setPrice] = useState('');
  const [style, setStyle] = useState(defaultStyle || 'Formal');

  useEffect(() => {
    if (open) {
      setTitle('');
      setPrice('');
      setStyle(defaultStyle || 'Formal');
    }
  }, [open, defaultStyle]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    onSubmit({ title: title.trim(), price, style });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <form onSubmit={handleSubmit}>
        <DialogTitle sx={sx.dialogTitle}>Crear libro</DialogTitle>
        <DialogContent>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 18, paddingTop: 6 }}>
            <TextField
              label="Título del libro"
              placeholder="Inteligencia artificial"
              autoFocus
              fullWidth
              size="small"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <TextField
              label="Precio (USD)"
              type="number"
              placeholder="9.99"
              fullWidth
              size="small"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
            <SelectField
              label="Estilo del resumen"
              fullWidth
              size="small"
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              options={STYLE_OPTIONS}
            />
          </div>
        </DialogContent>
        <DialogActions sx={sx.dialogActions}>
          <Button variant="text" onClick={onClose} sx={sx.cancelBtn}>
            Cancelar
          </Button>
          <Button type="submit" variant="contained" disableElevation sx={sx.primaryBtn}>
            Generar libro
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
