export const CLASS_METADATA = {
  whole_grain: {
    label: 'Whole Grain',
    color: '#10b981', // Emerald
    bgColor: 'bg-emerald-50',
    textColor: 'text-emerald-700',
    borderColor: 'border-emerald-300',
    desc: 'Sound, unblemished full grain kernels.'
  },
  broken_grain: {
    label: 'Broken Grain',
    color: '#3b82f6', // Blue
    bgColor: 'bg-blue-50',
    textColor: 'text-blue-700',
    borderColor: 'border-blue-300',
    desc: 'Kernels fragmented to less than 3/4 size.'
  },
  discolored_grain: {
    label: 'Discolored / Chalky',
    color: '#f59e0b', // Amber
    bgColor: 'bg-amber-50',
    textColor: 'text-amber-700',
    borderColor: 'border-amber-300',
    desc: 'Chalky, pecked, yellowed or black-tipped grains.'
  },
  insect_damaged: {
    label: 'Insect Damaged',
    color: '#ef4444', // Red
    bgColor: 'bg-red-50',
    textColor: 'text-red-700',
    borderColor: 'border-red-300',
    desc: 'Grains with boreholes or internal weevil feeding.'
  },
  foreign_matter: {
    label: 'Foreign Matter',
    color: '#8b5cf6', // Purple
    bgColor: 'bg-purple-50',
    textColor: 'text-purple-700',
    borderColor: 'border-purple-300',
    desc: 'Husk, chaff, weed seeds, stones or non-grain particles.'
  }
};

export function formatDate(dateString) {
  if (!dateString) return 'N/A';
  const d = new Date(dateString);
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

export function getGradeBadge(category) {
  switch ((category || '').toLowerCase()) {
    case 'excellent':
      return { label: 'EXCELLENT GRADE', bg: 'bg-emerald-100 text-emerald-800 border-emerald-300' };
    case 'good':
      return { label: 'GOOD GRADE', bg: 'bg-emerald-50 text-emerald-700 border-emerald-200' };
    case 'needs review':
      return { label: 'NEEDS REVIEW', bg: 'bg-amber-100 text-amber-800 border-amber-300' };
    case 'poor':
      return { label: 'REJECTED / POOR', bg: 'bg-rose-100 text-rose-800 border-rose-300' };
    default:
      return { label: category || 'UNKNOWN', bg: 'bg-slate-100 text-slate-700 border-slate-300' };
  }
}
