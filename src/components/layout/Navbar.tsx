import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { api } from '../../api/client';
import type { ResearchTreeRef } from '../../api/types';

/** Translate a backend base_url (e.g. http://localhost:8124) into a URL the
 *  browser can actually open. The backend speaks to the tree on localhost,
 *  but the browser may be on a LAN client — swap the hostname to whatever
 *  this page was loaded from. The port stays. */
function browserUrlFor(baseUrl: string): string {
  if (typeof window === 'undefined') return baseUrl;
  try {
    const u = new URL(baseUrl);
    u.hostname = window.location.hostname;
    return u.toString();
  } catch {
    return baseUrl;
  }
}

export function Navbar() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive
        ? 'bg-indigo-600 text-white'
        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
    }`;

  const [trees, setTrees] = useState<ResearchTreeRef[]>([]);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;
    api.listResearchTreeNodes().then(
      (r) => !cancelled && setTrees(r.enabled ? r.trees : []),
      () => {},
    );
    return () => { cancelled = true; };
  }, []);

  // Close the dropdown on outside click.
  useEffect(() => {
    if (!menuOpen) return;
    const onDown = () => setMenuOpen(false);
    window.addEventListener('mousedown', onDown);
    return () => window.removeEventListener('mousedown', onDown);
  }, [menuOpen]);

  const treeLinkClass =
    'ml-2 px-3 py-2 rounded-md text-sm font-medium text-emerald-300 ' +
    'border border-emerald-500/40 hover:bg-emerald-500/10 hover:text-emerald-200 transition-colors';

  let treeLink: React.ReactNode = null;
  if (trees.length === 1) {
    treeLink = (
      <a
        href={browserUrlFor(trees[0].base_url)}
        target="_blank"
        rel="noopener noreferrer"
        className={treeLinkClass}
        title={`Open the ${trees[0].name} research-tree editor in a new tab`}
      >
        🌳 Research tree ↗
      </a>
    );
  } else if (trees.length > 1) {
    treeLink = (
      <div className="relative ml-2" onMouseDown={(e) => e.stopPropagation()}>
        <button
          type="button"
          onClick={() => setMenuOpen((v) => !v)}
          className={treeLinkClass.replace('ml-2 ', '')}
          aria-haspopup="menu"
          aria-expanded={menuOpen}
        >
          🌳 Research trees ▾
        </button>
        {menuOpen && (
          <div
            role="menu"
            className="absolute right-0 mt-1 min-w-[14rem] bg-gray-800 border border-gray-700 rounded-md shadow-lg z-10"
          >
            {trees.map((t) => (
              <a
                key={t.name}
                role="menuitem"
                href={browserUrlFor(t.base_url)}
                target="_blank"
                rel="noopener noreferrer"
                className="block px-3 py-2 text-sm text-emerald-200 hover:bg-emerald-500/10"
                onClick={() => setMenuOpen(false)}
              >
                {t.name} ↗
              </a>
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <nav className="bg-gray-800 border-b border-gray-700" aria-label="Main navigation">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          <span className="text-white font-bold text-lg tracking-tight">
            SoundVisualizer
          </span>
          <div className="flex items-center gap-2">
            <NavLink to="/setup" className={linkClass}>Setup</NavLink>
            <NavLink to="/capture" className={linkClass}>Capture</NavLink>
            <NavLink to="/results" className={linkClass}>Results</NavLink>
            {treeLink}
          </div>
        </div>
      </div>
    </nav>
  );
}
