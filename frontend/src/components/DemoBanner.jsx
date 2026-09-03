import React from 'react';
import { Info, Cpu } from 'lucide-react';
import { useApp } from '../context/AppContext';

export default function DemoBanner() {
  const { systemHealth } = useApp();

  if (systemHealth.ai_mode === 'model' && systemHealth.model_loaded) {
    return (
      <div className="bg-emerald-900 text-emerald-100 text-xs px-4 py-1.5 flex items-center justify-between">
        <div className="flex items-center gap-2 max-w-7xl mx-auto w-full">
          <Cpu className="w-3.5 h-3.5 text-emerald-400" />
          <span><strong>PRODUCTION AI INFERENCE ACTIVE:</strong> Edge YOLO/TorchScript weights loaded.</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-amber-950 text-amber-200 text-xs px-4 py-1.5 border-b border-amber-800">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Info className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
          <span>
            <strong>DEMO INFERENCE MODE:</strong> Morphological computer vision is active. To enable custom trained neural network weights, place <code className="bg-amber-900 px-1 py-0.5 rounded text-amber-100">grain_model.pt</code> into <code className="bg-amber-900 px-1 py-0.5 rounded text-amber-100">backend/models/</code>.
          </span>
        </div>
        <span className="hidden sm:inline-block bg-amber-800/80 px-2 py-0.5 rounded text-[11px] font-mono">
          AI_MODE=demo
        </span>
      </div>
    </div>
  );
}
