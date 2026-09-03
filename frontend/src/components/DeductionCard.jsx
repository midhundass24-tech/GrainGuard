import React from 'react';
import { HelpCircle, AlertTriangle } from 'lucide-react';

export default function DeductionCard({ penalties = {}, grainType = 'rice' }) {
  const p = penalties || {};

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-semibold text-slate-900 text-sm flex items-center gap-2">
          Score Deduction Engine
          <span className="text-xs font-normal text-slate-500">(Formula Breakdown)</span>
        </h4>
        <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">
          Base: 100.0 pts
        </span>
      </div>

      <p className="text-xs text-slate-600 mb-4">
        Quality score starts at 100.0 and applies transparent weighted deductions for visual defect classes detected in this {grainType} sample.
      </p>

      <div className="space-y-2.5 text-xs">
        <div className="flex items-center justify-between p-2 rounded bg-slate-50 border border-slate-100">
          <span className="text-slate-700">Broken Grain Deduction (1.5x factor):</span>
          <span className="font-semibold font-mono text-slate-900">
            {p.broken_penalty > 0 ? `-${p.broken_penalty} pts` : '0.0 pts'}
          </span>
        </div>

        <div className="flex items-center justify-between p-2 rounded bg-slate-50 border border-slate-100">
          <span className="text-slate-700">Discoloration & Chalky Deduction (2.0x factor):</span>
          <span className="font-semibold font-mono text-slate-900">
            {p.discoloration_penalty > 0 ? `-${p.discoloration_penalty} pts` : '0.0 pts'}
          </span>
        </div>

        <div className="flex items-center justify-between p-2 rounded bg-slate-50 border border-slate-100">
          <span className="text-slate-700">Insect Damage Penalty (5.0x high-severity factor):</span>
          <span className="font-semibold font-mono text-rose-600">
            {p.insect_penalty > 0 ? `-${p.insect_penalty} pts` : '0.0 pts'}
          </span>
        </div>

        <div className="flex items-center justify-between p-2 rounded bg-slate-50 border border-slate-100">
          <span className="text-slate-700">Foreign Matter & Stones (10.0x critical factor):</span>
          <span className="font-semibold font-mono text-purple-700">
            {p.foreign_matter_penalty > 0 ? `-${p.foreign_matter_penalty} pts` : '0.0 pts'}
          </span>
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold">
        <span className="text-slate-800">Total Deductions Applied:</span>
        <span className="text-rose-600 font-mono text-sm">
          -{p.total_penalty || 0} pts
        </span>
      </div>
    </div>
  );
}
