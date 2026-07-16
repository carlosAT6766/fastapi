import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  typography: { fontFamily: '"Plus Jakarta Sans", -apple-system, sans-serif' },
  palette: {
    primary: { main: '#4f46e5', dark: '#4338ca' },
    background: { default: '#fafafa' },
    text: { primary: '#1a1a2e' },
  },
  shape: { borderRadius: 10 },
});
