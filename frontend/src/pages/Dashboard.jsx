import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlusCircle, 
  AlertOctagon, 
  TrendingUp, 
  Clock, 
  ArrowRight, 
  FileCheck,
  Wheat,
  ShieldCheck
} from 'lucide-react';
import { listInspections } from '../services/api';
import QualityBadge from '../components/QualityBadge';
import { formatDate } from '../utils/helpers';
import { useApp } from '../context/AppContext';

export default function Dashboard() {
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const { systemHealth } = useApp();

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await listInspections({ limit: 8 });
      setInspections(data.items || []);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Compute summary stats
  const total = inspections.length;
  const avgScore = total > 0 
    ? (inspections.reduce((acc, i) => acc + (i.quality_score || 0), 0) / total).toFixed(1)
    : '0.0';
  const flaggedCount = inspections.filter(i => (i.quality_score || 0) < 75).length;

  return (
    <div className="space-y-6">
      
      {/* Top Welcome & Fast Action Banner */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white rounded-2xl p-6 shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
              Rural Intake Station #01
            </span>
            <span className="text-xs text-slate-400">Node Active</span>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight">Grain Quality Intake Hub</h1>
          <p className="text-slate-300 text-sm mt-1 max-w-xl">
            Objective, explainable smartphone-based grain defect inspection and auditable digital certification.
          </p>
        </div>

        <Link
          to="/inspect/new"
          className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-6 py-3 rounded-xl shadow-lg flex items-center gap-2 text-sm transition-all transform hover:-translate-y-0.5"
        >
          <PlusCircle className="w-5 h-5" /> Start New Inspection
        </Link>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Recent Intake Batches</span>
            <FileCheck className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{total}</span>
            <span className="text-xs text-slate-500">inspected</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Average Quality Score</span>
            <TrendingUp className="w-4 h-4 text-blue-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{avgScore}</span>
            <span className="text-xs text-slate-400 font-mono">/ 100</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Flagged / Review</span>
            <AlertOctagon className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-amber-600">{flaggedCount}</span>
            <span className="text-xs text-slate-500">require re-check</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">AI Pipeline Mode</span>
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-sm font-bold text-slate-800 uppercase font-mono">
              {systemHealth.ai_mode === 'model' ? 'ONNX Neural Net' : 'Morphological CV'}
            </span>
          </div>
        </div>
      </div>

      {/* Recent Inspections Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-5 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h2 className="font-bold text-slate-900 text-base">Recent Grain Inspections</h2>
            <p className="text-xs text-slate-500">Live feed of verified Mandi intake assessments</p>
          </div>
          <Link
            to="/history"
            className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-1"
          >
            View All History <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading inspection records...</div>
        ) : inspections.length === 0 ? (
          <div className="p-12 text-center">
            <Wheat className="w-12 h-12 mx-auto text-slate-300 mb-3" />
            <h3 className="font-semibold text-slate-800 text-sm">No inspections recorded yet</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              Place a grain sample on the tray and start your first smartphone AI inspection.
            </p>
            <Link
              to="/inspect/new"
              className="mt-4 inline-flex items-center gap-1.5 bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-lg"
            >
              <PlusCircle className="w-4 h-4" /> Start Inspection
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] font-semibold border-b border-slate-200">
                <tr>
                  <th className="px-5 py-3">Inspection ID & Time</th>
                  <th className="px-4 py-3">Grain</th>
                  <th className="px-4 py-3">Farmer / Batch Reference</th>
                  <th className="px-4 py-3">Grains Analyzed</th>
                  <th className="px-4 py-3">Quality Score</th>
                  <th className="px-4 py-3">Grade Category</th>
                  <th className="px-5 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {inspections.map((insp) => (
                  <tr key={insp.inspection_id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-5 py-3.5">
                      <div className="font-mono font-medium text-slate-900">
                        {insp.inspection_id.substring(0, 8)}...
                      </div>
                      <div className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
                        <Clock className="w-3 h-3" /> {formatDate(insp.created_at)}
                      </div>
                    </td>
                    <td className="px-4 py-3.5 capitalize font-semibold text-slate-800">
                      {insp.grain_type}
                    </td>
                    <td className="px-4 py-3.5 text-slate-600">
                      {insp.farmer_reference || <span className="text-slate-400 italic">Unassigned</span>}
                    </td>
                    <td className="px-4 py-3.5 font-mono text-slate-700">
                      {insp.total_objects} items
                    </td>
                    <td className="px-4 py-3.5 font-bold font-mono text-slate-900">
                      {insp.quality_score.toFixed(1)} / 100
                    </td>
                    <td className="px-4 py-3.5">
                      <QualityBadge category={insp.quality_result?.category} />
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <Link
                        to={`/inspect/${insp.inspection_id}`}
                        className="font-semibold text-emerald-700 hover:text-emerald-900 text-xs inline-flex items-center gap-1"
                      >
                        View Results <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
}
