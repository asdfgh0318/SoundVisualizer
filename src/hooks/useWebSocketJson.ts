import { useEffect, useRef, useState } from 'react';

export type WsConnectionState = 'idle' | 'connecting' | 'open' | 'closed' | 'error';

export interface WsResult<T> {
  message: T | null;
  state: WsConnectionState;
}

/** Subscribe to a WebSocket that streams JSON frames. Reconnects when `url` changes
 *  or `active` flips true. Closes cleanly on unmount or when active=false. */
export function useWebSocketJson<T>(url: string | null, active: boolean): WsResult<T> {
  const [message, setMessage] = useState<T | null>(null);
  const [state, setState] = useState<WsConnectionState>('idle');
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!active || !url) {
      setState('idle');
      return;
    }
    setState('connecting');
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => setState('open');
    ws.onerror = () => setState('error');
    ws.onclose = () => setState('closed');
    ws.onmessage = (e) => {
      try {
        setMessage(JSON.parse(e.data) as T);
      } catch {
        /* ignore non-JSON */
      }
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [url, active]);

  return { message, state };
}
