// `crypto.randomUUID()` is gated to secure contexts (HTTPS or localhost). On
// plain-HTTP deployments (e.g. an internal-network demo server on port 8000)
// it throws "crypto.randomUUID is not a function" the moment the user clicks
// "Add mic". These IDs are only used as React keys / Zustand row identifiers,
// never sent to the server, so a non-crypto fallback is fine.
export function localId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `id-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 11)}`;
}
