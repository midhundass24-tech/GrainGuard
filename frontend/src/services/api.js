const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend service unreachable');
  return res.json();
}

export async function createInspection({ grain_type = 'rice', farmer_reference = '' }) {
  const res = await fetch(`${API_BASE}/inspections`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ grain_type, farmer_reference })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to initialize inspection session');
  }
  return res.json();
}

export async function analyzeInspection(inspectionId, imageSource) {
  const formData = new FormData();
  
  if (imageSource instanceof Blob && !(imageSource instanceof File)) {
    formData.append('file', imageSource, 'tray_capture.jpg');
  } else {
    formData.append('file', imageSource);
  }

  const res = await fetch(`${API_BASE}/inspections/${inspectionId}/analyze`, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Image quality or analysis failed');
  }
  return res.json();
}

export async function getInspection(inspectionId) {
  const res = await fetch(`${API_BASE}/inspections/${inspectionId}`);
  if (!res.ok) throw new Error('Inspection record not found');
  return res.json();
}

export async function listInspections({ search = '', grain_type = '', category = '', skip = 0, limit = 50 } = {}) {
  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (grain_type) params.append('grain_type', grain_type);
  if (category) params.append('category', category);
  params.append('skip', skip);
  params.append('limit', limit);

  const res = await fetch(`${API_BASE}/inspections?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to retrieve inspection history');
  return res.json();
}

export async function verifyCertificateToken(token) {
  const res = await fetch(`${API_BASE}/verify/${token}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Certificate token is invalid or unverified');
  }
  return res.json();
}
