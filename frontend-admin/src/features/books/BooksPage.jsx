import { Button, Chip } from '@mui/material';
import { PageHeader } from '../../components/PageHeader';
import { StatCard, StatGrid } from '../../components/StatCard';
import { DataTable } from '../../components/DataTable';
import { RowActionsMenu } from '../../components/RowActionsMenu';
import { statusInfo } from '../../constants';
import { formatPrice, formatTime } from '../../utils/format';
import { sx } from '../../theme';

const COLUMNS = (handlers) => [
  {
    header: 'Título',
    width: '1.5fr',
    style: { fontWeight: 600 },
    render: (b) => b.title,
  },
  { header: 'Precio', width: '0.7fr', render: (b) => formatPrice(b.price) },
  {
    header: 'Estilo',
    width: '0.9fr',
    render: (b) => <Chip size="small" label={b.style} variant="outlined" />,
  },
  {
    header: 'Estado',
    width: '0.9fr',
    render: (b) => {
      const info = statusInfo(b.status);
      return <Chip size="small" label={info.label} color={info.color} />;
    },
  },
  {
    header: 'Creado',
    width: '0.9fr',
    style: { color: '#8a8aa0', fontSize: 12 },
    render: (b) => formatTime(b.createdAt),
  },
  {
    header: '',
    width: '0.5fr',
    render: (b) => {
      const notReady = b.status !== 'listo';
      return (
        <RowActionsMenu
          onView={() => handlers.onView(b)}
          onSell={() => handlers.onSell(b)}
          sellDisabled={notReady || !b.price}
          onPdf={() => handlers.onPdf(b)}
          pdfDisabled={notReady || !b.summary}
          onEdit={() => handlers.onEdit(b)}
        />
      );
    },
  },
];

export function BooksPage({ books, onCreate, onView, onSell, onPdf, onEdit }) {
  const metrics = {
    total: books.length,
    ready: books.filter((b) => b.status === 'listo').length,
    inProgress: books.filter((b) => b.status === 'buscando' || b.status === 'resumiendo').length,
  };

  return (
    <div>
      <PageHeader
        title="Libros"
        subtitle="Cada libro busca el tema en Wikipedia (RPA) y lo resume con IA en el estilo elegido."
        action={
          <Button variant="contained" disableElevation onClick={onCreate} sx={sx.primaryBtn}>
            + Crear libro
          </Button>
        }
      />

      <StatGrid columns={3}>
        <StatCard label="Total libros" value={metrics.total} />
        <StatCard label="Listos" value={metrics.ready} color="#2e7d32" />
        <StatCard label="En proceso" value={metrics.inProgress} color="#ed6c02" />
      </StatGrid>

      <DataTable
        columns={COLUMNS({ onView, onSell, onPdf, onEdit })}
        rows={books}
        getRowKey={(b) => b.id}
        emptyMessage="Aún no hay libros. Crea el primero con el botón de arriba."
      />
    </div>
  );
}
