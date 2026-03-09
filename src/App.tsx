import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar.tsx';
import { SkipLink } from './components/layout/SkipLink.tsx';
import { SetupPage } from './pages/SetupPage.tsx';
import { CapturePage } from './pages/CapturePage.tsx';
import { ResultsPage } from './pages/ResultsPage.tsx';

export function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-900 text-gray-100">
        <SkipLink />
        <Navbar />
        <main id="main-content" className="p-6">
          <Routes>
            <Route path="/" element={<Navigate to="/setup" replace />} />
            <Route path="/setup" element={<SetupPage />} />
            <Route path="/capture" element={<CapturePage />} />
            <Route path="/results" element={<ResultsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
