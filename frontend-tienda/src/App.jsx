import { useCallback, useEffect, useMemo, useState } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';
import StoreHeader from './components/StoreHeader';
import BookCard from './components/BookCard';
import ToastStack from './components/ToastStack';
import { useToasts } from './hooks/useToasts';
import { fetchPublishedBooks } from './api/books';
import { purchaseBook } from './api/transactions';

export default function App() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [purchases, setPurchases] = useState([]);
  const [pendingId, setPendingId] = useState(null);
  const { notifications, pushToast } = useToasts();

  const loadBooks = useCallback(async () => {
    setLoading(true);
    try {
      setBooks(await fetchPublishedBooks());
    } catch (error) {
      pushToast('No se pudieron cargar los libros.', 'error');
      setBooks([]);
    } finally {
      setLoading(false);
    }
  }, [pushToast]);

  useEffect(() => {
    loadBooks();
  }, [loadBooks]);

  const handleBuy = useCallback(
    async (book) => {
      setPendingId(book.id);
      try {
        await purchaseBook(book);
        setPurchases((prev) => [...prev, { id: book.id, amount: book.price }]);
        pushToast(`Compraste "${book.title}"`, 'success');
      } catch (error) {
        pushToast(`No se pudo comprar "${book.title}".`, 'error');
      } finally {
        setPendingId(null);
      }
    },
    [pushToast],
  );

  const purchaseTotalLabel = useMemo(() => {
    const total = purchases.reduce((sum, p) => sum + p.amount, 0);
    return `$${total.toFixed(2)}`;
  }, [purchases]);

  const isEmpty = !loading && books.length === 0;

  return (
    <Box sx={{ minHeight: '100vh' }}>
      <StoreHeader purchaseCount={purchases.length} purchaseTotalLabel={purchaseTotalLabel} />

      <Box sx={{ maxWidth: 980, mx: 'auto', px: 5, py: 4, boxSizing: 'border-box' }}>
        <Typography variant="h5" sx={{ fontWeight: 700, letterSpacing: '-0.01em' }}>
          Libros publicados
        </Typography>
        <Typography variant="body2" sx={{ color: '#6b6b80', mb: 3 }}>
          Cada libro fue generado con RPA + IA. Compra uno para simular una venta.
        </Typography>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 2.25 }}>
            {books.map((book) => (
              <BookCard
                key={book.id}
                book={book}
                onBuy={handleBuy}
                disabled={pendingId === book.id}
              />
            ))}
          </Box>
        )}

        {isEmpty ? (
          <Box
            sx={{
              p: '60px',
              textAlign: 'center',
              color: '#8a8aa0',
              fontSize: 13.5,
              bgcolor: '#fff',
              border: '1px solid #ececf2',
              borderRadius: '12px',
            }}
          >
            Aún no hay libros publicados.
          </Box>
        ) : null}
      </Box>

      <ToastStack notifications={notifications} />
    </Box>
  );
}
