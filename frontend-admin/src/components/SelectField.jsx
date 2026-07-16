import { TextField, MenuItem } from '@mui/material';

// Reusable select (mirrors MuiSelectField from the design's mui-theme.jsx).
export function SelectField({ label, value, onChange, options = [], fullWidth, size, sx, autoFocus }) {
  return (
    <TextField
      select
      label={label}
      value={value}
      onChange={onChange}
      fullWidth={fullWidth}
      size={size}
      sx={sx}
      autoFocus={autoFocus}
    >
      {options.map((opt) => (
        <MenuItem key={opt.value} value={opt.value}>
          {opt.label}
        </MenuItem>
      ))}
    </TextField>
  );
}
