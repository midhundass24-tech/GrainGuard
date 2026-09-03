import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import DemoBanner from './components/DemoBanner';
import Dashboard from './pages/Dashboard';
import NewInspection from './pages/NewInspection';
import InspectionResult from './pages/InspectionResult';
import CertificateView from './pages/CertificateView';
import History from './pages/History';
import PublicVerify from './pages/PublicVerify';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <DemoBanner />
      <Navbar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inspect/new" element={<NewInspection />} />
          <Route path="/inspect/:id" element={<InspectionResult />} />
          <Route path="/inspect/:id/certificate" element={<CertificateView />} />
          <Route path="/history" element={<History />} />
          <Route path="/verify/:token" element={<PublicVerify />} />
        </Routes>
      </main>
      
      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-400 no-print">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>GrainGuard — AI Smartphone Grain Quality Assessment & Certification</span>
          <span>Targeting Visually Observable Grain Characteristics</span>
        </div>
      </footer>
    </div>
  );
}
