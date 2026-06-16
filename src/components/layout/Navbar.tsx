import { NavLink } from 'react-router-dom';

export function Navbar() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive
        ? 'bg-indigo-600 text-white'
        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
    }`;

  // The research-tree editor runs as its own service on the same host (Pi or
  // dev laptop) at :8123. Derive the URL from window.location so it works
  // unchanged on jama.local, localhost, or any other deployment.
  const researchTreeUrl =
    typeof window !== 'undefined'
      ? `${window.location.protocol}//${window.location.hostname}:8123/`
      : '#';

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
            <a
              href={researchTreeUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 px-3 py-2 rounded-md text-sm font-medium text-emerald-300 border border-emerald-500/40 hover:bg-emerald-500/10 hover:text-emerald-200 transition-colors"
              title="Open the duct-research-tree editor on this host (port 8123) in a new tab"
            >
              🌳 Research tree ↗
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}
