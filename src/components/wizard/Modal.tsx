import type { ReactNode } from 'react';

interface Props {
  title: string;
  children: ReactNode;
  footer?: ReactNode;
}

export function Modal({ title, children, footer }: Props) {
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 border border-gray-700 rounded-lg max-w-lg w-full overflow-hidden shadow-2xl">
        <div className="px-5 py-3 border-b border-gray-700 bg-gray-800/60">
          <h2 className="text-base font-semibold text-gray-100">{title}</h2>
        </div>
        <div className="p-5 text-sm text-gray-200 space-y-3">{children}</div>
        {footer && (
          <div className="px-5 py-3 border-t border-gray-700 bg-gray-900/40 flex items-center justify-end gap-3">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
