import { Button, Typography, Avatar } from '@mui/material';
import { useAuth } from '../../context/AuthContext';
import { NAV_ITEMS } from '../../constants';
import { sx, navBaseSx } from '../../theme';

export function Sidebar({ activeSection, onNavigate }) {
  const { logout } = useAuth();

  return (
    <div
      style={{
        width: 220,
        flex: 'none',
        background: '#fff',
        borderRight: '1px solid #ececf2',
        padding: '22px 14px',
        display: 'flex',
        flexDirection: 'column',
        gap: 6,
        boxSizing: 'border-box',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '0 8px 22px' }}>
        <div
          style={{
            width: 30,
            height: 30,
            borderRadius: 8,
            background: '#4f46e5',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontWeight: 700,
            fontSize: 14,
          }}
        >
          R
        </div>
        <Typography variant="subtitle1" sx={sx.brand}>
          ResumeAI
        </Typography>
      </div>

      {NAV_ITEMS.map((item) => {
        const active = activeSection === item.key;
        return (
          <Button
            key={item.key}
            variant="text"
            onClick={() => onNavigate(item.key)}
            sx={{
              ...navBaseSx,
              bgcolor: active ? '#eeecfc' : 'transparent',
              color: active ? '#4f46e5' : '#33334a',
            }}
          >
            {item.label}
          </Button>
        );
      })}

      <div style={{ flex: 1 }} />

      <div
        style={{
          borderTop: '1px solid #ececf2',
          paddingTop: 14,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          paddingLeft: 8,
        }}
      >
        <Avatar sx={sx.avatar}>A</Avatar>
        <div style={{ fontSize: 13, fontWeight: 600 }}>admin</div>
      </div>
      <Button variant="text" onClick={logout} sx={sx.logout}>
        Cerrar sesión
      </Button>
    </div>
  );
}
