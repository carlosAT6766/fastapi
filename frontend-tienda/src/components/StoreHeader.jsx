import PropTypes from 'prop-types';
import { Box, Typography } from '@mui/material';

export default function StoreHeader({ purchaseCount, purchaseTotalLabel }) {
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        px: 5,
        py: 2.25,
        bgcolor: '#fff',
        borderBottom: '1px solid #ececf2',
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.25 }}>
        <Box
          sx={{
            width: 30,
            height: 30,
            borderRadius: '8px',
            bgcolor: 'primary.main',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontWeight: 700,
            fontSize: 14,
          }}
        >
          R
        </Box>
        <Typography variant="subtitle1" sx={{ fontWeight: 700, letterSpacing: '-0.01em' }}>
          Tienda ResumeAI
        </Typography>
      </Box>
      <Box sx={{ textAlign: 'right' }}>
        <Box sx={{ fontSize: 12, color: '#8a8aa0' }}>Tus compras</Box>
        <Box sx={{ fontSize: 14, fontWeight: 700 }}>
          {purchaseCount} · {purchaseTotalLabel}
        </Box>
      </Box>
    </Box>
  );
}

StoreHeader.propTypes = {
  purchaseCount: PropTypes.number.isRequired,
  purchaseTotalLabel: PropTypes.string.isRequired,
};
