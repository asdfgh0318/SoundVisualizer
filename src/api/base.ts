// In dev (`npm run dev`), the frontend is served by Vite at :5173 and talks to
// the FastAPI server at :8000 — so `VITE_API_BASE` defaults to the absolute
// `http://localhost:8000`.
//
// In production (Docker image), the FastAPI server serves the React bundle
// itself on the same port, so VITE_API_BASE is built in as an empty string and
// requests are same-origin. WebSocket URLs in same-origin mode must still be
// absolute (`ws://host:port/...`), so we synthesize them from window.location.
export const API_BASE: string =
  (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000';

export const WS_BASE: string = API_BASE
  ? API_BASE.replace(/^http/, 'ws')
  : `${typeof window !== 'undefined' && window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${
      typeof window !== 'undefined' ? window.location.host : 'localhost:8000'
    }`;
