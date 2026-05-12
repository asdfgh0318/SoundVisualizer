export const API_BASE: string =
  (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000';

export const WS_BASE: string = API_BASE.replace(/^http/, 'ws');
