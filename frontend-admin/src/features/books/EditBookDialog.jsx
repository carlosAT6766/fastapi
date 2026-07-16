import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button } from '@mui/material';
import { SelectField } from '../../components/SelectField';
import { STYLE_OPTIONS } from '../../constants';
import { sx } from '../../theme';

export function EditBookDialog({ open, book, onClose, onSubmit }) {
  const [title, setTitle] = useState('');
  const [price, setPrice] = useState('');
  const [style, setStyle] = useState('Formal');
  const [summary, setSummary] = useState('');

  useEffect(() => {
    if (open && book) {
      setTitle(book.title);
      setPrice(book.price != null ? String(book.price) : '');
      setStyle(book.style);
      setSummary(book.summary || '');
    }
  }, [open, book]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ title: title.trim(), price, style, summary });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <form onSubmit={handleSubmit}>
        <DialogTitle sx={sx.dialogTitle}>Editar libro</DialogTitle>
        <DialogContent>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 18, paddingTop: 6 }}>
            <TextField
              label="Título"
              fullWidth
              size="small"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <TextField
              label="Precio (USD)"
              type="number"
              fullWidth
              size="small"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
            />
            <SelectField
              label="Estilo"
              fullWidth
              size="small"
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              options={STYLE_OPTIONS}
            />
            <TextField
              label="Texto del resumen"
              multiline
              minRows={5}
              fullWidth
              size="small"
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
            />
          </div>
        </DialogContent>
        <DialogActions sx={sx.dialogActions}>
          <Button variant="text" onClick={onClose} sx={sx.cancelBtn}>
            Cancelar
          </Button>
          <Button type="submit" variant="contained" disableElevation sx={sx.primaryBtn}>
            Guardar cambios
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
