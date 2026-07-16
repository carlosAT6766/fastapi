import { useCallback, useRef, useState } from 'react';

const TOAST_TTL_MS = 4000;

export function useToasts() {
  const [notifications, setNotifications] = useState([]);
  const seqRef = useRef(1);

  const pushToast = useCallback((text, severity = 'success') => {
    const id = seqRef.current;
    seqRef.current += 1;
    setNotifications((prev) => [...prev, { id, text, severity }]);
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, TOAST_TTL_MS);
  }, []);

  return { notifications, pushToast };
}
