import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getInspection } from '../services/api';
import { QRCodeSVG } from 'qrcode.react';
import { formatDate } from '../utils/helpers';
import QualityBadge from '../components/QualityBadge';
import { ShieldCheck, Printer, ArrowLeft, Lock, ExternalLink } from 'lucide-react';

export default function CertificateView() {
  const { id } = useParams();
  const [inspection, setInspection] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCert = async () => {
      try {
        const data = await getInspection(id);
        setInspection(data);
      } catch (err) {
        console.error('Certificate fetch failed:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCert();
  }, [id]);

  if (loading || !inspection) {
    return <div className="py-20 text-center text-xs text-slate-400">Loading Certificate...</div>;
  }

  const cert = inspection.certificate || {};
  const qr = inspection.quality_result || {};
  const verifyPath = `/verify/${cert.verification_token}`;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* Action Bar */}
      <div className="flex items-center justify-between no-print">
        <Link
          to={`/inspect/${inspection.inspection_id}`}
          className="text-xs font-semibold text-slate-600 hover:text-slate-900 flex items-center gap-1"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Results
        </Link>
        <div className="flex items-center gap-2">
          <Link
            to={verifyPath}
            target="_blank"
            className="border border-slate-300 hover:bg-slate-100 text-slate-700 text-xs font-semibold px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-sm"
          >
            <ExternalLink className="w-3.5 h-3.5" /> Test Public QR Link
          </Link>
          <button
            onClick={() => window.print()}
            className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-sm"
          >
            <Printer className="w-4 h-4" /> Print / Save PDF
          </button>
        </div>
      </div>

      {/* Official Certificate Paper Container */}
      <div className="bg-white rounded-2xl border-4 border-slate-900 p-8 sm:p-10 shadow-xl relative overflow-hidden">
        
        {/* Certificate Header */}
        <div className="border-b-2 border-slate-900 pb-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <div className="bg-emerald-700 text-white p-2 rounded-lg">
              <ShieldCheck className="w-7 h-7" />
            </div>
            <span className="text-2xl font-black tracking-wider uppercase text-slate-900">
              GrainGuard
            </span>
          </div>
          <h1 className="text-lg font-bold uppercase tracking-widest text-slate-800">
            Digital Grain Quality Intake Certificate
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Cryptographically Tamper-Evident Mandi Audit Record
          </p>
        </div>

        {/* Certificate Metadata Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-6 border-b border-slate-200 text-xs">
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Certificate Number</span>
            <div className="font-bold font-mono text-slate-900 mt-0.5">
              {cert.certificate_number || 'GG-2025-001'}
            </div>
          </div>
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Date & Time</span>
            <div className="font-medium text-slate-800 mt-0.5">
              {formatDate(inspection.created_at)}
            </div>
          </div>
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Commodity</span>
            <div className="font-bold text-slate-900 capitalize mt-0.5">
              {inspection.grain_type}
            </div>
          </div>
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Batch / Farmer Ref</span>
            <div className="font-medium text-slate-800 mt-0.5">
              {inspection.farmer_reference || 'N/A'}
            </div>
          </div>
        </div>

        {/* Quality Score & Grade Hero */}
        <div className="py-6 border-b border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-6 bg-slate-50 rounded-xl px-6 my-6">
          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-slate-500">
              Assigned Intake Grade
            </span>
            <div className="mt-1 flex items-center gap-3">
              <QualityBadge category={qr.category} size="large" />
              <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-1 rounded">
                STATUS: {qr.decision || 'ACCEPTABLE'}
              </span>
            </div>
          </div>

          <div className="text-center sm:text-right">
            <span className="text-xs uppercase tracking-wider font-semibold text-slate-500">
              Verified Quality Score
            </span>
            <div className="text-3xl font-extrabold text-slate-900 font-mono">
              {inspection.quality_score.toFixed(1)} <span className="text-sm font-normal text-slate-400">/ 100</span>
            </div>
          </div>
        </div>

        {/* Defect Statistics Table */}
        <div className="mb-6">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2.5">
            Defect Composition (Sample Count: {inspection.total_objects} items)
          </h3>
          <table className="w-full text-xs text-left border border-slate-200">
            <thead className="bg-slate-100 text-slate-700 font-semibold text-[11px]">
              <tr>
                <th className="p-2.5 border-b border-slate-200">Visual Quality Class</th>
                <th className="p-2.5 border-b border-slate-200 text-right">Composition %</th>
                <th className="p-2.5 border-b border-slate-200 text-right">Assigned Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              <tr>
                <td className="p-2.5 font-medium">Whole Sound Grain</td>
                <td className="p-2.5 text-right font-mono font-bold text-emerald-700">{qr.whole_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-emerald-700 font-semibold">PASS</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Broken Grain Fragment (&lt; 3/4)</td>
                <td className="p-2.5 text-right font-mono">{qr.broken_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-slate-600">AUDITED</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Discolored / Chalky Grain</td>
                <td className="p-2.5 text-right font-mono">{qr.discolored_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-slate-600">AUDITED</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Insect Damaged Kernels</td>
                <td className="p-2.5 text-right font-mono text-rose-600">{qr.insect_damage_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-rose-600 font-semibold">FLAGGED</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Foreign Matter / Non-Grain</td>
                <td className="p-2.5 text-right font-mono text-purple-700">{qr.foreign_matter_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-purple-700 font-semibold">FLAGGED</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Verification QR & Legal Footer */}
        <div className="pt-6 border-t-2 border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <Link
              to={verifyPath}
              className="p-2 bg-white border border-slate-300 rounded-lg shadow-sm hover:border-emerald-500 transition-colors"
              title="Click to verify online"
            >
              <QRCodeSVG value={window.location.origin + verifyPath} size={84} level="M" />
            </Link>
            <div className="text-xs">
              <div className="font-bold text-slate-900 flex items-center gap-1">
                <Lock className="w-3.5 h-3.5 text-emerald-600" /> Click or Scan QR to Verify
              </div>
              <p className="text-[11px] text-slate-500 max-w-xs mt-0.5">
                Token: <span className="font-mono text-slate-800">{cert.verification_token}</span>
              </p>
            </div>
          </div>

          <div className="text-center sm:text-right text-[11px] text-slate-400">
            <div>Authorized Procurement Officer Node</div>
            <div className="font-mono text-slate-700 font-bold mt-0.5">DIGITALLY SIGNED & SEALED</div>
          </div>
        </div>

      </div>
    </div>
  );
}
