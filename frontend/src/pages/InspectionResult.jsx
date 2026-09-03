import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getInspection } from '../services/api';
import QualityScoreGauge from '../components/QualityScoreGauge';
import QualityBadge from '../components/QualityBadge';
import DeductionCard from '../components/DeductionCard';
import EvidenceViewer from '../components/EvidenceViewer';
import { formatDate } from '../utils/helpers';
import { 
  ArrowLeft, 
  Award, 
  AlertTriangle 
} from 'lucide-react';

export default function InspectionResult() {
  const { id } = useParams();
  const [inspection, setInspection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecord = async () => {
      try {
        setLoading(true);
        const data = await getInspection(id);
        setInspection(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch inspection results');
      } finally {
        setLoading(false);
      }
    };
    fetchRecord();
  }, [id]);

  if (loading) {
    return (
      <div className="py-20 text-center text-slate-500 text-sm">
        Loading AI inspection results & evidence...
      </div>
    );
  }

  if (error || !inspection) {
    return (
      <div className="max-w-2xl mx-auto py-16 text-center">
        <AlertTriangle className="w-12 h-12 text-rose-500 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-slate-900">Inspection Record Not Found</h2>
        <p className="text-xs text-slate-500 mt-1">{error}</p>
        <Link to="/" className="mt-4 inline-block bg-slate-900 text-white text-xs font-semibold px-4 py-2 rounded-lg">
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const qr = inspection.quality_result || {};
  const penalties = qr.penalties || {};

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      
      {/* Top Breadcrumb & Action Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Link
          to="/"
          className="text-xs font-semibold text-slate-600 hover:text-slate-900 flex items-center gap-1.5"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Dashboard
        </Link>

        <div className="flex items-center gap-2">
          <Link
            to={`/inspect/${inspection.inspection_id}/certificate`}
            className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-4 py-2 rounded-lg shadow-sm flex items-center gap-1.5"
          >
            <Award className="w-4 h-4" /> Generate Certificate
          </Link>
        </div>
      </div>

      {/* Hero Result Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-6">
          
          {/* Left Metadata & Score Badge */}
          <div className="flex-1 space-y-2 text-center lg:text-left">
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-2">
              <span className="text-xs bg-slate-100 text-slate-700 font-mono px-2 py-0.5 rounded font-semibold">
                ID: {inspection.inspection_id.substring(0, 12)}
              </span>
              <QualityBadge category={qr.category} size="large" />
            </div>

            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              {inspection.grain_type.toUpperCase()} Quality Inspection Result
            </h1>

            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-4 text-xs text-slate-500 pt-1">
              <span><strong>Batch / Farmer:</strong> {inspection.farmer_reference || 'Unassigned'}</span>
              <span><strong>Objects Detected:</strong> {inspection.total_objects} grains</span>
              <span><strong>Proc. Time:</strong> {inspection.processing_time_ms} ms</span>
              <span><strong>Date:</strong> {formatDate(inspection.created_at)}</span>
            </div>
          </div>

          {/* Right Circular Gauge */}
          <div className="flex-shrink-0 border-t lg:border-t-0 lg:border-l border-slate-100 lg:pl-8">
            <QualityScoreGauge score={inspection.quality_score} category={qr.category} />
          </div>
        </div>
      </div>

      {/* 5-Class Defect Percentage Distribution */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-slate-900 text-sm">Visual Class Distribution</h3>
            <p className="text-xs text-slate-500">Breakdown of 5 standard inspection defect classes</p>
          </div>
          <span className="text-xs font-mono font-semibold text-slate-600 bg-slate-100 px-2 py-1 rounded">
            100% Sample Composition
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {/* Whole Grain */}
          <div className="bg-emerald-50/60 border border-emerald-200 rounded-xl p-3.5 text-center">
            <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-emerald-800 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
              Whole Grain
            </div>
            <div className="text-2xl font-extrabold text-emerald-950 font-mono">
              {qr.whole_percentage?.toFixed(1)}%
            </div>
            <div className="text-[11px] text-emerald-700 mt-1">Sound Kernel</div>
          </div>

          {/* Broken Grain */}
          <div className="bg-blue-50/60 border border-blue-200 rounded-xl p-3.5 text-center">
            <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-blue-800 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-blue-500" />
              Broken Grain
            </div>
            <div className="text-2xl font-extrabold text-blue-950 font-mono">
              {qr.broken_percentage?.toFixed(1)}%
            </div>
            <div className="text-[11px] text-blue-700 mt-1">&lt; 3/4 Size</div>
          </div>

          {/* Discolored Grain */}
          <div className="bg-amber-50/60 border border-amber-200 rounded-xl p-3.5 text-center">
            <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-amber-800 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
              Discolored
            </div>
            <div className="text-2xl font-extrabold text-amber-950 font-mono">
              {qr.discolored_percentage?.toFixed(1)}%
            </div>
            <div className="text-[11px] text-amber-700 mt-1">Chalky / Pecked</div>
          </div>

          {/* Insect Damaged */}
          <div className="bg-rose-50/60 border border-rose-200 rounded-xl p-3.5 text-center">
            <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-rose-800 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
              Insect Damaged
            </div>
            <div className="text-2xl font-extrabold text-rose-950 font-mono">
              {qr.insect_damage_percentage?.toFixed(1)}%
            </div>
            <div className="text-[11px] text-rose-700 mt-1">Boreholes</div>
          </div>

          {/* Foreign Matter */}
          <div className="bg-purple-50/60 border border-purple-200 rounded-xl p-3.5 text-center">
            <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-purple-800 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-purple-500" />
              Foreign Matter
            </div>
            <div className="text-2xl font-extrabold text-purple-950 font-mono">
              {qr.foreign_matter_percentage?.toFixed(1)}%
            </div>
            <div className="text-[11px] text-purple-700 mt-1">Husk / Stones</div>
          </div>
        </div>
      </div>

      {/* Deduction Explainer Engine */}
      <DeductionCard penalties={penalties} grainType={inspection.grain_type} />

      {/* Interactive AI Evidence Viewer */}
      <EvidenceViewer
        imageUrl={inspection.image_url}
        annotatedImageUrl={inspection.annotated_image_url}
        detections={inspection.detections || []}
      />

    </div>
  );
}
