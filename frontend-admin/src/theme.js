import { createTheme } from '@mui/material/styles';

// Design contract: mui-theme.jsx (ResumeAI handoff)
export const theme = createTheme({
  typography: { fontFamily: '"Plus Jakarta Sans", -apple-system, sans-serif' },
  palette: {
    primary: { main: '#4f46e5' },
    background: { default: '#fafafa' },
    text: { primary: '#1a1a2e' },
  },
  shape: { borderRadius: 10 },
});

// Reusable sx snippets lifted verbatim from the prototype for pixel fidelity.
export const sx = {
  loginPaper: { p: 4.5, width: 380, maxWidth: '100%', borderRadius: '14px' },
  title: { fontWeight: 700, letterSpacing: '-0.01em' },
  subtitle: { color: '#6b6b80', mb: 3 },
  primaryBtn: {
    textTransform: 'none',
    fontWeight: 600,
    bgcolor: '#4f46e5',
    '&:hover': { bgcolor: '#4338ca' },
  },
  cancelBtn: { textTransform: 'none', fontWeight: 600, color: '#6b6b80' },
  deleteBtn: { textTransform: 'none', fontWeight: 600, color: '#d32f2f', fontSize: 12.5 },
  brand: { fontWeight: 700, letterSpacing: '-0.01em' },
  avatar: { width: 28, height: 28, fontSize: 12, fontWeight: 700, bgcolor: '#e4e4ee', color: '#4a4a5e' },
  logout: { textTransform: 'none', justifyContent: 'flex-start', color: '#6b6b80', fontSize: 13, mt: 1 },
  heading: { fontWeight: 700, letterSpacing: '-0.01em' },
  card: { p: '20px 22px', borderRadius: '12px', border: '1px solid #ececf2' },
  stat: { p: '18px 20px', borderRadius: '12px', border: '1px solid #ececf2' },
  table: { borderRadius: '12px', border: '1px solid #ececf2', overflow: 'hidden' },
  dialogTitle: { fontWeight: 700 },
  dialogActions: { p: '0 24px 20px' },
};

export const navBaseSx = {
  justifyContent: 'flex-start',
  textTransform: 'none',
  fontWeight: 600,
  fontSize: 14,
  borderRadius: '8px',
  px: 1.5,
  py: 1,
};
