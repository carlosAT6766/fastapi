import { useCallback, useEffect, useRef, useState } from 'react';
import { Sidebar } from './Sidebar';
import { BooksPage } from '../books/BooksPage';
import { CreateBookDialog } from '../books/CreateBookDialog';
import { EditBookDialog } from '../books/EditBookDialog';
import { ViewBookDialog } from '../books/ViewBookDialog';
import { SalesPage } from '../sales/SalesPage';
import { ConfigPage } from '../config/ConfigPage';
import { UsersPage } from '../users/UsersPage';
import { CreateUserDialog } from '../users/CreateUserDialog';
import { PrintArea } from '../print/PrintArea';
import { Toasts } from '../../components/Toasts';
import { useToasts } from '../../hooks/useToasts';
import { statusInfo } from '../../constants';
import { fetchBooks, createBook, updateBook } from '../../api/books';
import { fetchSales, sellBook } from '../../api/sales';
import { fetchUsers, createUser, updateUser, deleteUser } from '../../api/users';
import { fetchSettings, saveSettings } from '../../api/settings';
import { connectStream } from '../../api/websocket';
import { toSale } from '../../api/mappers';

export function Shell() {
  const { toasts, notify } = useToasts();
  const [section, setSection] = useState('books');

  const [books, setBooks] = useState([]);
  const [sales, setSales] = useState([]);
  const [users, setUsers] = useState([]);
  const [settings, setSettings] = useState({ defaultSource: 'Wikipedia (ES)', defaultStyle: 'Formal' });

  const seenSaleIds = useRef(new Set());

  const [createOpen, setCreateOpen] = useState(false);
  const [userOpen, setUserOpen] = useState(false);
  const [editBook, setEditBook] = useState(null);
  const [viewBook, setViewBook] = useState(null);
  const [printBook, setPrintBook] = useState(null);

  const upsertBook = useCallback((incoming) => {
    if (!incoming) return;
    setBooks((current) => {
      const idx = current.findIndex((b) => b.id === incoming.id);
      if (idx === -1) return [incoming, ...current];
      const next = [...current];
      next[idx] = { ...next[idx], ...incoming };
      return next;
    });
  }, []);

  // Initial data load. Failures degrade gracefully (endpoints may land in Ola 2).
  useEffect(() => {
    fetchBooks().then(setBooks).catch(() => notify('No se pudieron cargar los libros', 'warning'));
    fetchSales()
      .then((initial) => {
        initial.forEach((s) => seenSaleIds.current.add(s.id));
        setSales(initial);
      })
      .catch(() => {});
    fetchUsers().then(setUsers).catch(() => {});
    fetchSettings().then(setSettings).catch(() => {});
  }, [notify]);

  // Live updates over WebSocket: refresh table + fire toasts on status changes.
  useEffect(() => {
    const disconnect = connectStream({
      onBook: (book, meta = {}) => {
        upsertBook(book);
        if (meta.snapshot) return; // initial sync — no notification
        const info = statusInfo(book.status);
        if (book.status === 'listo') notify(`Resumen de "${book.title}" listo`, 'success');
        else if (book.status === 'fallido') notify(`Falló la generación de "${book.title}"`, 'error');
        else notify(`"${book.title}": ${info.label}`, 'info');
      },
      onSale: (raw, meta = {}) => {
        const sale = toSale(raw);
        if (seenSaleIds.current.has(sale.id)) return;
        seenSaleIds.current.add(sale.id);
        setSales((current) => [sale, ...current]);
        if (meta.snapshot) return; // initial sync — no notification
        // PDF: notify when a transaction changes state (a sale arriving in real time).
        const title = sale.bookTitle && sale.bookTitle !== '—' ? sale.bookTitle : 'un libro';
        notify(`Venta registrada: "${title}" · $${Number(sale.amount).toFixed(2)}`, 'success');
      },
      onLog: ({ id, line }) =>
        setBooks((current) =>
          current.map((b) => (b.id === id ? { ...b, log: [...(b.log || []), line] } : b)),
        ),
    });
    return disconnect;
  }, [notify, upsertBook]);

  const handleCreateBook = async (payload) => {
    setCreateOpen(false);
    try {
      const book = await createBook(payload);
      upsertBook(book);
      notify(`Generando resumen de "${payload.title}"…`, 'info');
    } catch (err) {
      notify(err.message || 'No se pudo crear el libro', 'error');
    }
  };

  const handleEditBook = async (payload) => {
    const id = editBook.id;
    setEditBook(null);
    try {
      const book = await updateBook(id, payload);
      upsertBook(book);
      notify('Libro actualizado', 'success');
    } catch (err) {
      notify(err.message || 'No se pudo actualizar', 'error');
    }
  };

  const handleSell = async (book) => {
    if (book.status !== 'listo' || !book.price) {
      notify('El libro debe estar listo y tener precio para venderse', 'warning');
      return;
    }
    try {
      const sale = await sellBook(book);
      seenSaleIds.current.add(sale.id);
      setSales((current) => [{ ...sale, bookTitle: sale.bookTitle || book.title }, ...current]);
      notify(`Venta registrada: "${book.title}"`, 'success');
    } catch (err) {
      notify(err.message || 'No se pudo registrar la venta', 'error');
    }
  };

  const handlePdf = (book) => {
    setPrintBook(book);
    setTimeout(() => window.print(), 100);
  };

  const handleCreateUser = async (payload) => {
    setUserOpen(false);
    try {
      const user = await createUser(payload);
      setUsers((current) => [...current, user]);
      notify(`Usuario ${payload.name} dado de alta`, 'success');
    } catch (err) {
      notify(err.message || 'No se pudo crear el usuario', 'error');
    }
  };

  const handleToggleUser = async (user) => {
    const nextActive = !user.active;
    setUsers((current) => current.map((u) => (u.id === user.id ? { ...u, active: nextActive } : u)));
    try {
      await updateUser(user.id, { active: nextActive });
    } catch {
      setUsers((current) => current.map((u) => (u.id === user.id ? { ...u, active: user.active } : u)));
      notify('No se pudo actualizar el usuario', 'error');
    }
  };

  const handleDeleteUser = async (user) => {
    try {
      await deleteUser(user.id);
      setUsers((current) => current.filter((u) => u.id !== user.id));
      notify('Usuario eliminado', 'info');
    } catch (err) {
      notify(err.message || 'No se pudo eliminar', 'error');
    }
  };

  const handleSaveSettings = async (next) => {
    try {
      await saveSettings(next);
      setSettings(next);
      notify('Configuración guardada', 'success');
    } catch (err) {
      notify(err.message || 'No se pudo guardar', 'error');
    }
  };

  return (
    <>
      <div id="mainAppShell" style={{ minHeight: '100vh', display: 'flex' }}>
        <Sidebar activeSection={section} onNavigate={setSection} />

        <div style={{ flex: 1, padding: '32px 40px', boxSizing: 'border-box', minWidth: 0 }}>
          {section === 'books' && (
            <BooksPage
              books={books}
              onCreate={() => setCreateOpen(true)}
              onView={setViewBook}
              onSell={handleSell}
              onPdf={handlePdf}
              onEdit={setEditBook}
            />
          )}
          {section === 'sales' && <SalesPage sales={sales} />}
          {section === 'config' && <ConfigPage settings={settings} onSave={handleSaveSettings} />}
          {section === 'users' && (
            <UsersPage
              users={users}
              onCreate={() => setUserOpen(true)}
              onToggle={handleToggleUser}
              onDelete={handleDeleteUser}
            />
          )}
        </div>
      </div>

      <CreateBookDialog
        open={createOpen}
        defaultStyle={settings.defaultStyle}
        onClose={() => setCreateOpen(false)}
        onSubmit={handleCreateBook}
      />
      <EditBookDialog
        open={Boolean(editBook)}
        book={editBook}
        onClose={() => setEditBook(null)}
        onSubmit={handleEditBook}
      />
      <ViewBookDialog open={Boolean(viewBook)} book={viewBook} onClose={() => setViewBook(null)} />
      <CreateUserDialog open={userOpen} onClose={() => setUserOpen(false)} onSubmit={handleCreateUser} />

      <PrintArea book={printBook} />
      <Toasts toasts={toasts} />
    </>
  );
}
