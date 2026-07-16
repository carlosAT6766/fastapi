import { Alert } from '@mui/material';

// Fixed top-right stack of auto-dismissing alerts.
export function Toasts({ toasts }) {
  return (
    <div
      style={{
        position: 'fixed',
        top: 20,
        right: 20,
        display: 'flex',
        flexDirection: 'column',
        gap: 10,
        zIndex: 1300,
        width: 340,
      }}
    >
      {toasts.map((t) => (
        <div key={t.id} style={{ animation: 'toastIn .2s ease' }}>
          <Alert severity={t.severity} elevation={3}>
            {t.text}
          </Alert>
        </div>
      ))}
    </div>
  );
}
