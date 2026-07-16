import { useCallback, useRef, useState } from 'react';

const AUTO_DISMISS_MS = 4500;

// Top-right toasts (MUI Alert), auto-dismiss ~4.5s. Mirrors the prototype.
export function useToasts() {
  const [toasts, setToasts] = useState([]);
  const seq = useRef(1);

  const dismiss = useCallback((id) => {
    setToasts((current) => current.filter((t) => t.id !== id));
  }, []);

  const notify = useCallback(
    (text, severity = 'info') => {
      const id = seq.current++;
      setToasts((current) => [...current, { id, text, severity }]);
      setTimeout(() => dismiss(id), AUTO_DISMISS_MS);
    },
    [dismiss],
  );

  return { toasts, notify, dismiss };
}
