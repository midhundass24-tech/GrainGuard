import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createInspection, analyzeInspection } from '../services/api';
import CameraCapture from '../components/CameraCapture';
import { ArrowRight, ShieldCheck, AlertCircle, Loader2 } from 'lucide-react';

const GRAIN_OPTIONS = [
  { id: 'rice', label: 'Rice / Paddy', badge: 'Active MVP', supported: true },
  { id: 'wheat', label: 'Wheat', badge: 'Configured', supported: true },
  { id: 'pulses', label: 'Pulses / Lentils', badge: 'Configured', supported: true }
];

export default function NewInspection() {
  const navigate = useNavigate();
  const [grainType, setGrainType] = useState('rice');
  const [farmerRef, setFarmerRef] = useState('');
  const [imageBlob, setImageBlob] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisStep, setAnalysisStep] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!imageBlob) {
      setError('Please capture or upload a grain sample image first.');
      return;
    }

    try {
      setError(null);
      setLoading(true);

      // 1. Initialize session
      setAnalysisStep('Initializing inspection session...');
      const initRes = await createInspection({
        grain_type: grainType,
        farmer_reference: farmerRef.trim() || undefined
      });

      // 2. Upload & analyze
      setAnalysisStep('Pre-processing image & running AI CV detection...');
      const analyzeRes = await analyzeInspection(initRes.inspection_id, imageBlob);

      // 3. Navigate to results
      setAnalysisStep('Finalizing certification metrics...');
      navigate(`/inspect/${analyzeRes.inspection_id}`);
    } catch (err) {
      console.error('Inspection error:', err);
      setError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setLoading(false);
      setAnalysisStep('');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">New Grain Inspection</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Follow the 2-step workflow: Set batch parameters, then photograph the contrasting tray sample.
        </p>
      </div>

      {error && (
        <div className="bg-rose-50 border border-rose-200 text-rose-800 p-4 rounded-xl text-xs flex items-start gap-2 shadow-sm">
          <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
          <div>
            <strong>Inspection Notice:</strong> {error}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Step 1: Batch Configuration */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <span className="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-bold">1</span>
            <h2 className="font-bold text-slate-900 text-sm">Select Commodity & Batch Details</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Grain Commodity Type
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {GRAIN_OPTIONS.map(g => (
                  <label
                    key={g.id}
                    className={`flex items-center justify-between p-3 rounded-xl border-2 cursor-pointer transition-all ${
                      grainType === g.id
                        ? 'border-emerald-600 bg-emerald-50/50 shadow-sm'
                        : 'border-slate-200 hover:border-slate-300 bg-white'
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <input
                        type="radio"
                        name="grainType"
                        value={g.id}
                        checked={grainType === g.id}
                        onChange={() => setGrainType(g.id)}
                        className="text-emerald-600 focus:ring-emerald-500"
                      />
                      <span className="text-xs font-bold text-slate-900">{g.label}</span>
                    </div>
                    <span className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-medium">
                      {g.badge}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Farmer / Batch Reference ID <span className="text-slate-400 font-normal">(Optional)</span>
              </label>
              <input
                type="text"
                value={farmerRef}
                onChange={(e) => setFarmerRef(e.target.value)}
                placeholder="e.g. MANDI-LOT-4091 or Farmer Ramesh"
                className="w-full text-xs px-3.5 py-2.5 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>
        </div>

        {/* Step 2: Camera Capture */}
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <span className="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-bold">2</span>
            <h2 className="font-bold text-slate-900 text-sm">Capture Tray Grain Sample</h2>
          </div>

          <CameraCapture
            onCapture={(blob) => setImageBlob(blob)}
          />
        </div>

        {/* Action Button */}
        <div className="flex items-center justify-between pt-2">
          <div className="text-xs text-slate-500">
            {imageBlob ? (
              <span className="text-emerald-700 font-semibold flex items-center gap-1">
                <ShieldCheck className="w-4 h-4" /> Ready for AI Analysis
              </span>
            ) : (
              'Capture a tray photo above to proceed'
            )}
          </div>

          <button
            type="submit"
            disabled={!imageBlob || loading}
            className={`font-bold px-8 py-3 rounded-xl shadow-md flex items-center gap-2 text-sm transition-all ${
              imageBlob && !loading
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white cursor-pointer transform hover:-translate-y-0.5'
                : 'bg-slate-300 text-slate-500 cursor-not-allowed'
            }`}
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>{analysisStep || 'Analyzing Sample...'}</span>
              </>
            ) : (
              <>
                <span>Run AI Analysis</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
