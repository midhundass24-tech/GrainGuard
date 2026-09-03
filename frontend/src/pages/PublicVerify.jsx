import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { verifyCertificateToken } from '../services/api';
import QualityBadge from '../components/QualityBadge';
import { formatDate } from '../utils/helpers';
import { CheckCircle2, AlertTriangle, Lock } from 'lucide-react';

export default function PublicVerify() {
  const { token } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const runVerification = async () => {
      try {
        setLoading(true);
        const res = await verifyCertificateToken(token);
        setData(res);
      } catch (err) {
        setError(err.message || 'Verification failed');
      } finally {
        setLoading(false);
      }
    };
    runVerification();
  }, [token]);

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      {loading ? (
        <div className="p-16 text-center text-xs text-slate-400">
          Cryptographically verifying certificate token...
        </div>
      ) : error || !data?.verified ? (
        <div className="bg-white rounded-2xl border border-rose-200 p-8 shadow-sm text-center">
          <AlertTriangle className="w-12 h-12 text-rose-600 mx-auto mb-3" />
          <h1 className="text-lg font-bold text-slate-900">Certificate Verification Failed</h1>
          <p className="text-xs text-slate-600 mt-2 max-w-md mx-auto">
            The verification token <code className="bg-slate-100 p-1 rounded font-mono text-rose-700">{token}</code> is either invalid, revoked, or has been tampered with.
          </p>
          <Link
            to="/"
            className="mt-6 inline-flex items-center gap-1.5 bg-slate-900 text-white text-xs font-semibold px-4 py-2 rounded-lg"
          >
            Go to GrainGuard Home
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border-2 border-emerald-600 p-8 shadow-lg">
          
          {/* Verified Seal Header */}
          <div className="text-center pb-6 border-b border-slate-200">
            <div className="w-14 h-14 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mx-auto mb-3 shadow-inner">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <span className="bg-emerald-100 text-emerald-800 text-[11px] font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              Official Tamper-Proof Audit
            </span>
            <h1 className="text-xl font-black text-slate-900 mt-2 uppercase tracking-wide">
              Certificate Verified Authentic
            </h1>
            <p className="text-xs text-slate-500 font-mono mt-0.5">
              Cert ID: {data.certificate_number}
            </p>
          </div>

          {/* Core Verified Details */}
          <div className="py-5 grid grid-cols-2 gap-4 text-xs border-b border-slate-200">
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Inspection Date</span>
              <div className="font-semibold text-slate-800 mt-0.5">{formatDate(data.inspection_date)}</div>
            </div>
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Commodity Type</span>
              <div className="font-bold text-slate-900 capitalize mt-0.5">{data.grain_type}</div>
            </div>
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Batch / Farmer Reference</span>
              <div className="font-medium text-slate-800 mt-0.5">{data.farmer_reference || 'N/A'}</div>
            </div>
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Sample Analyzed</span>
              <div className="font-bold font-mono text-slate-900 mt-0.5">{data.total_objects} Grains</div>
            </div>
          </div>

          {/* Grade & Score */}
          <div className="py-4 my-4 bg-slate-50 rounded-xl px-5 flex items-center justify-between border border-slate-100">
            <div>
              <span className="text-[10px] uppercase font-bold text-slate-400">Intake Grade Category</span>
              <div className="mt-1">
                <QualityBadge category={data.category} size="large" />
              </div>
            </div>
            <div className="text-right">
              <span className="text-[10px] uppercase font-bold text-slate-400">Quality Score</span>
              <div className="text-2xl font-extrabold font-mono text-slate-900">
                {data.quality_score?.toFixed(1)} <span className="text-xs text-slate-400 font-normal">/ 100</span>
              </div>
            </div>
          </div>

          {/* Defect Metrics */}
          <div className="space-y-2 text-xs">
            <h4 className="font-bold text-slate-800 text-[11px] uppercase tracking-wider">Defect Breakdown</h4>
            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Whole Grain:</span>
                <span className="font-bold text-emerald-700">{data.statistics?.whole_percentage?.toFixed(1)}%</span>
              </div>
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Broken Grain:</span>
                <span className="font-mono font-semibold text-slate-800">{data.statistics?.broken_percentage?.toFixed(1)}%</span>
              </div>
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Discolored:</span>
                <span className="font-mono font-semibold text-slate-800">{data.statistics?.discolored_percentage?.toFixed(1)}%</span>
              </div>
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Insect Damaged:</span>
                <span className="font-mono font-bold text-rose-600">{data.statistics?.insect_damage_percentage?.toFixed(1)}%</span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-200 text-center text-[11px] text-slate-400 flex items-center justify-center gap-1">
            <Lock className="w-3.5 h-3.5 text-emerald-600" />
            Verified via GrainGuard Decentralized Mandi Node
          </div>

        </div>
      )}
    </div>
  );
}
