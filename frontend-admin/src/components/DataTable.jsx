import { Paper } from '@mui/material';
import { sx } from '../theme';

// Lightweight CSS-grid table matching the prototype's exact spacing.
// columns: [{ header, width, render(row), style }]
export function DataTable({ columns, rows, getRowKey, emptyMessage }) {
  const template = columns.map((c) => c.width).join(' ');

  return (
    <Paper elevation={0} sx={sx.table}>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: template,
          padding: '12px 18px',
          fontSize: 11.5,
          fontWeight: 700,
          letterSpacing: '.03em',
          textTransform: 'uppercase',
          color: '#6b6b80',
          borderBottom: '1px solid #ececf2',
        }}
      >
        {columns.map((c, i) => (
          <div key={i}>{c.header}</div>
        ))}
      </div>

      {rows.map((row) => (
        <div
          key={getRowKey(row)}
          style={{
            display: 'grid',
            gridTemplateColumns: template,
            padding: '12px 18px',
            fontSize: 13.5,
            borderBottom: '1px solid #f4f4f8',
            alignItems: 'center',
          }}
        >
          {columns.map((c, i) => (
            <div key={i} style={c.style}>
              {c.render(row)}
            </div>
          ))}
        </div>
      ))}

      {rows.length === 0 && (
        <div style={{ padding: 60, textAlign: 'center', color: '#8a8aa0', fontSize: 13.5 }}>
          {emptyMessage}
        </div>
      )}
    </Paper>
  );
}
