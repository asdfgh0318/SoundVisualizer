import type { ReactNode } from 'react';

export function Loading({ label = 'Loading…' }: { label?: string }) {
  return <div className="text-sm text-gray-400 italic">{label}</div>;
}

export function ErrorMessage({ error, onRetry }: { error: Error; onRetry?: () => void }) {
  return (
    <div className="text-sm text-red-400 flex items-center gap-3">
      <span>Error: {error.message}</span>
      {onRetry && (
        <button
          onClick={onRetry}
          className="text-xs underline text-red-300 hover:text-red-200"
        >
          retry
        </button>
      )}
    </div>
  );
}

export function Empty({ children }: { children: ReactNode }) {
  return <div className="text-sm text-gray-400 italic">{children}</div>;
}
