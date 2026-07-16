import { Paper } from '@mui/material';
import { sx } from '../theme';

// Metric card: uppercase label + big value (optional accent color).
export function StatCard({ label, value, color }) {
  return (
    <Paper elevation={0} sx={sx.stat}>
      <div
        style={{
          fontSize: 12,
          fontWeight: 600,
          color: '#6b6b80',
          textTransform: 'uppercase',
          letterSpacing: '.03em',
        }}
      >
        {label}
      </div>
      <div style={{ fontSize: 30, fontWeight: 800, marginTop: 6, color }}>{value}</div>
    </Paper>
  );
}

export function StatGrid({ columns = 3, maxWidth, children }) {
  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gap: 16,
        margin: '20px 0 28px',
        maxWidth,
      }}
    >
      {children}
    </div>
  );
}
