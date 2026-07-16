import { Fragment, useState } from 'react';
import { IconButton, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';

// Row kebab menu: Ver / Vender / Descargar PDF / Editar.
// Icons are inline SVG lifted from the design's mui-theme.jsx (MuiRowActionsMenu).
const dotsIcon = (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
    <circle cx="9" cy="3.5" r="1.6" />
    <circle cx="9" cy="9" r="1.6" />
    <circle cx="9" cy="14.5" r="1.6" />
  </svg>
);
const eyeIcon = (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4">
    <ellipse cx="8" cy="8" rx="6.2" ry="3.4" />
    <circle cx="8" cy="8" r="1.5" fill="currentColor" stroke="none" />
  </svg>
);
const downloadIcon = (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
    <line x1="8" y1="2" x2="8" y2="10" />
    <polyline points="4.5 7 8 10.5 11.5 7" />
    <line x1="3" y1="13.5" x2="13" y2="13.5" />
  </svg>
);
const editIcon = (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2.8" y="9.6" width="3.2" height="3.2" transform="rotate(-45 4.4 11.2)" />
    <line x1="5.6" y1="10.4" x2="11" y2="5" />
    <line x1="11" y1="5" x2="13" y2="7" />
  </svg>
);
const sellIcon = (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3">
    <rect x="3" y="3" width="7" height="7" rx="1" transform="rotate(45 6.5 6.5)" />
    <circle cx="6.5" cy="6.5" r="1" fill="currentColor" stroke="none" />
  </svg>
);

export function RowActionsMenu({ onView, onSell, sellDisabled, onPdf, pdfDisabled, onEdit }) {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const close = () => setAnchorEl(null);
  const wrap = (fn) => () => {
    close();
    fn?.();
  };

  return (
    <Fragment>
      <IconButton size="small" onClick={(e) => setAnchorEl(e.currentTarget)} sx={{ color: '#6b6b80' }}>
        {dotsIcon}
      </IconButton>
      <Menu anchorEl={anchorEl} open={open} onClose={close}>
        <MenuItem onClick={wrap(onView)}>
          <ListItemIcon sx={{ minWidth: 30 }}>{eyeIcon}</ListItemIcon>
          <ListItemText>Ver</ListItemText>
        </MenuItem>
        <MenuItem onClick={wrap(onSell)} disabled={sellDisabled}>
          <ListItemIcon sx={{ minWidth: 30 }}>{sellIcon}</ListItemIcon>
          <ListItemText>Vender</ListItemText>
        </MenuItem>
        <MenuItem onClick={wrap(onPdf)} disabled={pdfDisabled}>
          <ListItemIcon sx={{ minWidth: 30 }}>{downloadIcon}</ListItemIcon>
          <ListItemText>Descargar PDF</ListItemText>
        </MenuItem>
        <MenuItem onClick={wrap(onEdit)}>
          <ListItemIcon sx={{ minWidth: 30 }}>{editIcon}</ListItemIcon>
          <ListItemText>Editar</ListItemText>
        </MenuItem>
      </Menu>
    </Fragment>
  );
}
