import { Button, Chip, Switch } from '@mui/material';
import { PageHeader } from '../../components/PageHeader';
import { DataTable } from '../../components/DataTable';
import { sx } from '../../theme';

const COLUMNS = (handlers) => [
  { header: 'Nombre', width: '1.2fr', style: { fontWeight: 600 }, render: (u) => u.name },
  { header: 'Email', width: '1.6fr', style: { color: '#57576b' }, render: (u) => u.email },
  {
    header: 'Rol',
    width: '1fr',
    render: (u) => <Chip size="small" label={u.role} variant="outlined" />,
  },
  {
    header: 'Activo',
    width: '0.8fr',
    render: (u) => (
      <Switch checked={u.active} onChange={() => handlers.onToggle(u)} size="small" />
    ),
  },
  {
    header: '',
    width: '0.8fr',
    render: (u) => (
      <Button variant="text" onClick={() => handlers.onDelete(u)} sx={sx.deleteBtn}>
        Eliminar
      </Button>
    ),
  },
];

export function UsersPage({ users, onCreate, onToggle, onDelete }) {
  return (
    <div>
      <PageHeader
        title="Usuarios"
        subtitle="Alta, baja y estado de los usuarios con acceso."
        action={
          <Button variant="contained" disableElevation onClick={onCreate} sx={sx.primaryBtn}>
            + Nuevo usuario
          </Button>
        }
      />

      <div style={{ marginTop: 20 }}>
        <DataTable
          columns={COLUMNS({ onToggle, onDelete })}
          rows={users}
          getRowKey={(u) => u.id}
          emptyMessage="No hay usuarios."
        />
      </div>
    </div>
  );
}
