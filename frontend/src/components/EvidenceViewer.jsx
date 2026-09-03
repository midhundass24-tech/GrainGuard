import React, { useState, useRef } from 'react';
import { CLASS_METADATA, resolveImageUrl } from '../utils/helpers';
import { Eye, Filter, AlertCircle, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';

export default function EvidenceViewer({ imageUrl, annotatedImageUrl, detections = [] }) {
  const [selectedFilter, setSelectedFilter] = useState('ALL');
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [showAnnotated, setShowAnnotated] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(1);

  const filteredDetections = detections.filter(d => {
    if (selectedFilter === 'ALL') return true;
    return d.class_name === selectedFilter;
  });

  const rawImage = showAnnotated && annotatedImageUrl ? annotatedImageUrl : imageUrl;
  const activeImage = resolveImageUrl(rawImage);

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      {/* Header Controls */}
      <div className="p-4 border-b border-slate-200 bg-slate-50 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <Eye className="w-5 h-5 text-emerald-600" />
            Interactive AI Evidence Viewer
          </h3>
          <p className="text-xs text-slate-500">
            Auditable visual proof. Click individual detected grains to inspect bounding box and confidence score.
          </p>
        </div>

        {/* Toggle Original vs AI Annotated */}
        <div className="flex items-center gap-2 bg-slate-200 p-1 rounded-lg text-xs font-medium">
          <button
            onClick={() => setShowAnnotated(true)}
            className={`px-3 py-1.5 rounded-md transition-all ${
              showAnnotated ? 'bg-white text-slate-900 shadow-sm font-semibold' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            AI Annotated Evidence
          </button>
          <button
            onClick={() => setShowAnnotated(false)}
            className={`px-3 py-1.5 rounded-md transition-all ${
              !showAnnotated ? 'bg-white text-slate-900 shadow-sm font-semibold' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Original Raw Photo
          </button>
        </div>
      </div>

      {/* Class Filter Bar */}
      <div className="px-4 py-2.5 bg-slate-100 border-b border-slate-200 flex flex-wrap items-center gap-2 text-xs">
        <span className="font-semibold text-slate-700 flex items-center gap-1 mr-1">
          <Filter className="w-3.5 h-3.5" /> Filter:
        </span>
        <button
          onClick={() => setSelectedFilter('ALL')}
          className={`px-2.5 py-1 rounded-full border transition-all ${
            selectedFilter === 'ALL'
              ? 'bg-slate-900 text-white border-slate-900 font-semibold'
              : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-200'
          }`}
        >
          All ({detections.length})
        </button>
        {Object.keys(CLASS_METADATA).map(clsKey => {
          const count = detections.filter(d => d.class_name === clsKey).length;
          const meta = CLASS_METADATA[clsKey];
          return (
            <button
              key={clsKey}
              onClick={() => setSelectedFilter(clsKey)}
              className={`px-2.5 py-1 rounded-full border transition-all flex items-center gap-1.5 ${
                selectedFilter === clsKey
                  ? 'bg-slate-900 text-white border-slate-900 font-semibold'
                  : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-200'
              }`}
            >
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: meta.color }} />
              {meta.label} ({count})
            </button>
          );
        })}
      </div>

      {/* Main Evidence Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3">
        {/* Visual Canvas / Image Display */}
        <div className="lg:col-span-2 bg-slate-950 relative min-h-[380px] max-h-[550px] flex items-center justify-center overflow-auto p-2">
          {activeImage ? (
            <div className="relative max-w-full max-h-full flex items-center justify-center">
              <img
                src={activeImage}
                alt="Grain Sample AI Evidence"
                className="max-h-[500px] object-contain rounded shadow-md select-none"
                style={{ transform: `scale(${zoomLevel})`, transition: 'transform 0.2s ease' }}
              />
            </div>
          ) : (
            <div className="text-slate-400 text-xs text-center p-8">
              Sample image preview unavailable.
            </div>
          )}

          {/* Zoom controls overlay */}
          <div className="absolute bottom-3 right-3 flex items-center gap-1 bg-slate-900/80 backdrop-blur p-1 rounded-lg border border-slate-700 text-white text-xs">
            <button
              onClick={() => setZoomLevel(prev => Math.min(prev + 0.25, 2.5))}
              className="p-1.5 hover:bg-slate-700 rounded"
              title="Zoom in"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
            <span className="px-1 text-[11px] font-mono">{Math.round(zoomLevel * 100)}%</span>
            <button
              onClick={() => setZoomLevel(prev => Math.max(prev - 0.25, 0.75))}
              className="p-1.5 hover:bg-slate-700 rounded"
              title="Zoom out"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
            <button
              onClick={() => setZoomLevel(1)}
              className="p-1.5 hover:bg-slate-700 rounded"
              title="Reset Zoom"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Detected Objects Sidebar & Inspector */}
        <div className="p-4 border-t lg:border-t-0 lg:border-l border-slate-200 bg-white flex flex-col h-[500px]">
          <div className="mb-3">
            <h4 className="font-semibold text-slate-900 text-sm">Detected Objects List</h4>
            <p className="text-xs text-slate-500">
              Showing {filteredDetections.length} grains matching filter
            </p>
          </div>

          {/* Scrollable list of items */}
          <div className="flex-1 overflow-y-auto space-y-2 pr-1">
            {filteredDetections.length === 0 ? (
              <div className="text-center py-10 text-slate-400 text-xs">
                No objects detected for the selected filter.
              </div>
            ) : (
              filteredDetections.map((det, index) => {
                const meta = CLASS_METADATA[det.class_name] || { label: det.class_name, color: '#64748b' };
                const isSelected = selectedDetection?.id === det.id || (selectedDetection?.bbox === det.bbox && selectedDetection?.confidence === det.confidence);
                const isLowConfidence = det.confidence < 0.85;

                return (
                  <div
                    key={det.id || index}
                    onClick={() => setSelectedDetection(det)}
                    className={`p-2.5 rounded-lg border text-xs cursor-pointer transition-all ${
                      isSelected
                        ? 'border-emerald-600 bg-emerald-50/70 shadow-sm'
                        : 'border-slate-200 hover:border-slate-300 bg-white'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center gap-2">
                        <span
                          className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                          style={{ backgroundColor: meta.color }}
                        />
                        <span className="font-semibold text-slate-900">
                          {meta.label} #{index + 1}
                        </span>
                      </div>
                      <span className="font-mono font-medium text-slate-600">
                        {(det.confidence * 100).toFixed(1)}% Conf
                      </span>
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-slate-500">
                      <span>Area: {Math.round(det.area || 0)} px²</span>
                      <span>
                        BBox: [{det.bbox ? det.bbox.join(', ') : 'N/A'}]
                      </span>
                    </div>

                    {isLowConfidence && (
                      <div className="mt-1.5 flex items-center gap-1 text-[10px] text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
                        <AlertCircle className="w-3 h-3 flex-shrink-0" />
                        <span>Low-confidence detection — manual check advised</span>
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>

          {/* Detailed Inspector Modal/Card for Selected Grain */}
          {selectedDetection && (
            <div className="mt-3 pt-3 border-t border-slate-200 bg-slate-50 p-3 rounded-lg text-xs">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-slate-900">AI Explainer Card</span>
                <button
                  onClick={() => setSelectedDetection(null)}
                  className="text-slate-400 hover:text-slate-600 font-bold"
                >
                  ✕
                </button>
              </div>
              <p className="text-slate-700 mb-1">
                <strong>Class:</strong> {CLASS_METADATA[selectedDetection.class_name]?.label || selectedDetection.class_name}
              </p>
              <p className="text-slate-600 text-[11px] mb-2">
                {CLASS_METADATA[selectedDetection.class_name]?.desc}
              </p>
              <div className="flex justify-between text-[11px] text-slate-500 font-mono">
                <span>Confidence: {(selectedDetection.confidence * 100).toFixed(2)}%</span>
                <span>Area: {selectedDetection.area} px</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
