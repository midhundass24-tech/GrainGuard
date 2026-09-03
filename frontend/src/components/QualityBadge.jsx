import React from 'react';
import { getGradeBadge } from '../utils/helpers';

export default function QualityBadge({ category, size = 'normal' }) {
  const badge = getGradeBadge(category);
  const sizeClasses = size === 'large' 
    ? 'text-sm px-3.5 py-1.5 font-bold tracking-wider' 
    : 'text-xs px-2.5 py-0.5 font-semibold';

  return (
    <span className={`inline-flex items-center rounded-full border ${badge.bg} ${sizeClasses}`}>
      {badge.label}
    </span>
  );
}
