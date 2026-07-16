import { Dialog, DialogTitle, DialogContent, DialogActions, Chip, Button } from '@mui/material';
import { statusInfo } from '../../constants';
import { formatTime } from '../../utils/format';
import { sx } from '../../theme';

export function ViewBookDialog({ open, book, onClose }) {
  const info = book ? statusInfo(book.status) : null;
  const showLog = book && book.status !== 'listo' && book.status !== 'fallido';

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={sx.dialogTitle}>{book?.title}</DialogTitle>
      <DialogContent>
        {book && (
          <>
            <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
              <Chip size="small" label={book.style} variant="outlined" />
              <Chip size="small" label={info.label} color={info.color} />
            </div>

            {showLog && book.log?.length > 0 && (
              <div style={{ background: '#f7f7fb', borderRadius: 8, padding: '12px 14px', marginBottom: 14 }}>
                {book.log.map((line, i) => (
                  <div
                    key={i}
                    style={{
                      fontFamily: 'ui-monospace, monospace',
                      fontSize: 12,
                      color: '#57576b',
                      padding: '2px 0',
                    }}
                  >
                    {line}
                  </div>
                ))}
              </div>
            )}

            {book.summary && (
              <div style={{ fontSize: 13.5, lineHeight: 1.6, color: '#33334a' }}>{book.summary}</div>
            )}

            <div style={{ fontSize: 11.5, color: '#a0a0b0', marginTop: 16 }}>
              {formatTime(book.createdAt)}
            </div>
          </>
        )}
      </DialogContent>
      <DialogActions sx={sx.dialogActions}>
        <Button variant="text" onClick={onClose} sx={sx.cancelBtn}>
          Cerrar
        </Button>
      </DialogActions>
    </Dialog>
  );
}
