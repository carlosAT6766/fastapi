import { Typography } from '@mui/material';
import { StatCard, StatGrid } from '../../components/StatCard';
import { DataTable } from '../../components/DataTable';
import { formatPrice, formatDateTime } from '../../utils/format';
import { sx } from '../../theme';

const COLUMNS = [
  { header: 'Libro', width: '1.6fr', style: { fontWeight: 600 }, render: (v) => v.bookTitle },
  {
    header: 'Fecha',
    width: '1fr',
    style: { color: '#8a8aa0', fontSize: 12 },
    render: (v) => formatDateTime(v.date),
  },
  {
    header: 'Monto',
    width: '1fr',
    style: { fontWeight: 600, color: '#2e7d32' },
    render: (v) => formatPrice(v.amount),
  },
];

export function SalesPage({ sales }) {
  const total = sales.reduce((sum, v) => sum + v.amount, 0);

  return (
    <div>
      <Typography variant="h5" sx={sx.heading}>
        Ventas
      </Typography>
      <Typography variant="body2" sx={sx.subtitle}>
        Libros vendidos y monto recaudado.
      </Typography>

      <StatGrid columns={2} maxWidth={520}>
        <StatCard label="Libros vendidos" value={sales.length} />
        <StatCard label="Total recaudado" value={formatPrice(total)} color="#2e7d32" />
      </StatGrid>

      <DataTable
        columns={COLUMNS}
        rows={sales}
        getRowKey={(v) => v.id}
        emptyMessage="Aún no se ha vendido ningún libro."
      />
    </div>
  );
}
