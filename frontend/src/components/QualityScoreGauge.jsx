import React from 'react';

export default function QualityScoreGauge({ score = 0, category = 'Good' }) {
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const clampedScore = Math.max(0, Math.min(100, score));
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  let strokeColor = '#10b981'; // Green (Excellent/Good)
  if (clampedScore < 60) {
    strokeColor = '#ef4444'; // Red
  } else if (clampedScore < 75) {
    strokeColor = '#f59e0b'; // Amber
  }

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative flex items-center justify-center">
        <svg className="w-36 h-36 transform -rotate-90">
          {/* Background circle */}
          <circle
            cx="72"
            cy="72"
            r={radius}
            stroke="currentColor"
            strokeWidth="10"
            className="text-slate-100"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="72"
            cy="72"
            r={radius}
            stroke={strokeColor}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-extrabold text-slate-900 tracking-tight">
            {score.toFixed(1)}
          </span>
          <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">
            out of 100
          </span>
        </div>
      </div>
      <div className="mt-2 text-center">
        <span className="text-xs font-semibold text-slate-600 uppercase tracking-widest">
          Transparent Quality Score
        </span>
      </div>
    </div>
  );
}
