import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listInspections } from '../services/api';
import QualityBadge from '../components/QualityBadge';
import { formatDate } from '../utils/helpers';
import { Search, Clock, ArrowRight, Wheat } from 'lucide-react';

export default function History() {
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [grainType, setGrainType] = useState('');
  const [category, setCategory] = useState('');

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const data = await listInspections({
        search,
        grain_type: grainType,
        category,
        limit: 100
      });
      setInspections(data.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchHistory();
    }, 250);
    return () => clearTimeout(timer);
  }, [search, grainType, category]);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Inspection History & Audit Log</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Search, filter, and audit past smartphone-analyzed grain batches.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm grid grid-cols-1 sm:grid-cols-3 gap-3">
        {/* Search */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search Batch ID or Farmer..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        {/* Grain Commodity Filter */}
        <div>
          <select
            value={grainType}
            onChange={(e) => setGrainType(e.target.value)}
            className="w-full py-2 px-3 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
          >
            <option value="">All Commodities</option>
            <option value="rice">Rice</option>
            <option value="wheat">Wheat</option>
            <option value="pulses">Pulses</option>
          </select>
        </div>

        {/* Grade Category Filter */}
        <div>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full py-2 px-3 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-white"
          >
            <option value="">All Grade Categories</option>
            <option value="Excellent">Excellent (90+)</option>
            <option value="Good">Good (75-89)</option>
            <option value="Needs Review">Needs Review (60-74)</option>
            <option value="Poor">Poor / Rejected (&lt;60)</option>
          </select>
        </div>
      </div>

      {/* Inspection List Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-xs">Loading records...</div>
        ) : inspections.length === 0 ? (
          <div className="p-12 text-center">
            <Wheat className="w-10 h-10 mx-auto text-slate-300 mb-2" />
            <h3 className="font-semibold text-slate-800 text-sm">No inspections match filters</h3>
            <p className="text-xs text-slate-500 mt-1">Try modifying your search criteria.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] font-semibold border-b border-slate-200">
                <tr>
                  <th className="px-5 py-3">Inspection ID & Date</th>
                  <th className="px-4 py-3">Commodity</th>
                  <th className="px-4 py-3">Farmer / Batch</th>
                  <th className="px-4 py-3">Grains Inspected</th>
                  <th className="px-4 py-3">Quality Score</th>
                  <th className="px-4 py-3">Intake Grade</th>
                  <th className="px-5 py-3 text-right">Certificate</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {inspections.map((insp) => (
                  <tr key={insp.inspection_id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-5 py-3.5">
                      <div className="font-mono font-medium text-slate-900">
                        {insp.inspection_id.substring(0, 10)}...
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
                        Inspect <ArrowRight className="w-3 h-3" />
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
