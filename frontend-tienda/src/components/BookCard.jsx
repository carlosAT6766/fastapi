import PropTypes from 'prop-types';
import { Box, Button, Chip, Paper } from '@mui/material';

export default function BookCard({ book, onBuy, disabled }) {
  return (
    <Paper elevation={0} sx={{ p: '20px 22px', borderRadius: '12px', border: '1px solid #ececf2' }}>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          gap: 1.25,
          mb: 1,
        }}
      >
        <Box sx={{ fontSize: 16, fontWeight: 700, letterSpacing: '-0.01em' }}>{book.title}</Box>
        {book.style ? <Chip size="small" label={book.style} variant="outlined" /> : null}
      </Box>
      <Box sx={{ fontSize: 13, color: '#57576b', lineHeight: 1.5, mb: 1.75, minHeight: 40 }}>
        {book.preview}
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ fontSize: 18, fontWeight: 800, color: 'primary.main' }}>{book.priceLabel}</Box>
        <Button
          onClick={() => onBuy(book)}
          disabled={disabled}
          variant="contained"
          disableElevation
          sx={{
            textTransform: 'none',
            fontWeight: 600,
            bgcolor: 'primary.main',
            '&:hover': { bgcolor: 'primary.dark' },
          }}
        >
          Comprar
        </Button>
      </Box>
    </Paper>
  );
}

BookCard.propTypes = {
  book: PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    title: PropTypes.string,
    style: PropTypes.string,
    preview: PropTypes.string,
    priceLabel: PropTypes.string,
  }).isRequired,
  onBuy: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
};

BookCard.defaultProps = {
  disabled: false,
};
