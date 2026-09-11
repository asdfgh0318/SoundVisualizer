import { useEffect, useId, useRef, useState, type ReactNode } from 'react';

interface Props {
  /** What the toggle explains — used for the accessible name. */
  label: string;
  children: ReactNode;
}

/** A small ⓘ button that shows or hides a short explanation of a parameter.
 *  Closed by default; toggles on click, closes on Escape or an outside click. */
export function InfoToggle({ label, children }: Props) {
  const [open, setOpen] = useState(false);
  // Popovers near the right edge of the window open to the left so they stay on screen.
  const [alignRight, setAlignRight] = useState(false);
  const id = useId();
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    window.addEventListener('mousedown', onDown);
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('mousedown', onDown);
      window.removeEventListener('keydown', onKey);
    };
  }, [open]);

  return (
    <span ref={ref} className="relative inline-block align-middle">
      <button
        type="button"
        aria-expanded={open}
        aria-controls={id}
        aria-label={`About ${label}`}
        title={`About ${label}`}
        onClick={() => {
          const r = ref.current?.getBoundingClientRect();
          setAlignRight(!!r && r.left > window.innerWidth * 0.6);
          setOpen((v) => !v);
        }}
        className={`ml-1 inline-flex items-center justify-center w-4 h-4 rounded-full border text-[10px] leading-none font-serif italic transition-colors ${
          open
            ? 'border-indigo-400 text-indigo-300 bg-indigo-500/20'
            : 'border-gray-600 text-gray-400 hover:border-gray-400 hover:text-gray-200'
        }`}
      >
        i
      </button>
      {open && (
        <span
          id={id}
          role="note"
          className={`absolute ${alignRight ? 'right-0' : 'left-0'} top-full mt-1 z-20 block w-72 max-w-[80vw] normal-case tracking-normal font-normal text-xs leading-relaxed text-gray-200 bg-gray-900 border border-gray-600 rounded-md shadow-lg p-3`}
        >
          {children}
        </span>
      )}
    </span>
  );
}
