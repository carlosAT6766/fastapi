import { Typography } from '@mui/material';
import { sx } from '../theme';

// Screen header: title + subtitle, with an optional right-aligned action slot.
export function PageHeader({ title, subtitle, action }) {
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16 }}>
      <div>
        <Typography variant="h5" sx={sx.heading}>
          {title}
        </Typography>
        {subtitle && (
          <Typography variant="body2" sx={sx.subtitle}>
            {subtitle}
          </Typography>
        )}
      </div>
      {action}
    </div>
  );
}
