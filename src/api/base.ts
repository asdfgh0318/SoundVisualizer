// In dev (`npm run dev`), the frontend is served by Vite at :5173 and talks to
// the FastAPI server at :8000 — so the default is the absolute
// `http://localhost:8000`.
//
// In production builds (`npm run build`), the FastAPI server serves the React
// bundle itself on the same port, so the default is an empty string and requests
// go same-origin (whatever host the browser loaded the page from). This avoids
// the foot-gun where a bundle built without VITE_API_BASE="" bakes in the dev
// `http://localhost:8000` and fetches die with ERR_CONNECTION_REFUSED for any
// LAN client. `VITE_API_BASE` can still be set explicitly to override either way.
//
// WebSocket URLs in same-origin mode must still be absolute (`ws://host:port/...`),
// so we synthesize them from window.location.
export const API_BASE: string =
  (import.meta.env.VITE_API_BASE as string | undefined) ??
  (import.meta.env.PROD ? '' : 'http://localhost:8000');

export const WS_BASE: string = API_BASE
  ? API_BASE.replace(/^http/, 'ws')
  : `${typeof window !== 'undefined' && window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${
      typeof window !== 'undefined' ? window.location.host : 'localhost:8000'
    }`;
