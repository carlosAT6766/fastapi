import { formatTime } from '../../utils/format';

// Hidden print target. @media print (in main.css) hides the app shell and
// reveals this block, so window.print() yields a clean single-book PDF.
export function PrintArea({ book }) {
  return (
    <div id="printArea">
      {book && (
        <div>
          <h1>{book.title}</h1>
          <p>
            <strong>Estilo:</strong> {book.style} · <strong>Generado:</strong>{' '}
            {formatTime(book.createdAt)}
          </p>
          <p>{book.summary}</p>
        </div>
      )}
    </div>
  );
}
