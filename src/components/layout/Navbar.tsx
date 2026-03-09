import { NavLink } from 'react-router-dom';

export function Navbar() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive
        ? 'bg-indigo-600 text-white'
        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
    }`;

  return (
    <nav className="bg-gray-800 border-b border-gray-700" aria-label="Main navigation">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          <span className="text-white font-bold text-lg tracking-tight">
            SoundVisualizer
          </span>
          <div className="flex gap-2">
            <NavLink to="/setup" className={linkClass}>
              Setup
            </NavLink>
            <NavLink to="/capture" className={linkClass}>
              Capture
            </NavLink>
            <NavLink to="/results" className={linkClass}>
              Results
            </NavLink>
          </div>
        </div>
      </div>
    </nav>
  );
}
