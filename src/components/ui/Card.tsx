import type { ReactNode } from 'react';

interface CardProps {
  title?: string;
  description?: string;
  right?: ReactNode;
  children: ReactNode;
}

export function Card({ title, description, right, children }: CardProps) {
  return (
    <section className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
      {(title || right) && (
        <div className="px-5 py-3 border-b border-gray-700 bg-gray-800/60 flex items-start justify-between gap-4">
          <div>
            {title && (
              <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-200">
                {title}
              </h2>
            )}
            {description && <p className="text-xs text-gray-400 mt-1">{description}</p>}
          </div>
          {right && <div className="shrink-0">{right}</div>}
        </div>
      )}
      <div className="p-5">{children}</div>
    </section>
  );
}
