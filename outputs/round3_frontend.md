# GrainGuard — Frontend Architecture & Complete Implementation

---

## 1. Frontend Technology
* **Framework**: **React 18** + **Vite 5** (ultra-fast builds, instant hot module replacement, zero bloat).
* **Styling & Design System**: **Tailwind CSS v3** customized with high-contrast agricultural/procurement-gate tokens (`emerald-700` forest primary, `amber-500` review warning, `rose-600` reject red, `slate-900` slate darks).
* **Icons**: **Lucide React** (`lucide-react`) for clear, crisp, non-distracting iconography.
* **Camera / Media API**: Native HTML5 `navigator.mediaDevices.getUserMedia` with real-time video stream, top-down tray framing reticle, automatic canvas frame capture, front/back camera switching, and fallback local sample image picker.
* **Charts & Visuals**: Lightweight custom SVG charts and interactive canvas bounding box overlays for pinpoint object inspection.
* **Routing**: `react-router-dom` v6 for clean client-side routing.
* **QR Code Rendering**: `qrcode.react` for instant client-side QR verification badge rendering alongside backend generated assets.

---

## 2. Pages

1. **`Dashboard.jsx` (`/`)**:
   - High-level procurement intake summary (today's inspection count, average quality score, flagged batches, recent inspections stream).
   - Instant "Start New Inspection" hero action.
   - Live backend connectivity & AI mode status badge (`DEMO CV ENGINE` vs `MODEL ONNX/TORCH`).

2. **`NewInspection.jsx` (`/inspect/new`)**:
   - Fast 2-step setup: Grain selection (Rice default, Wheat/Pulses pre-configured) and optional Farmer/Lot reference ID.
   - Streamlined camera interface with visual tray alignment guide and live camera capture or sample image selection.
   - Interactive capture feedback and pre-flight validation status.

3. **`InspectionResult.jsx` (`/inspect/:id`)**:
   - The visual centerpiece of GrainGuard.
   - Circular quality score gauge (0–100) with dynamic color categorization (Excellent / Good / Needs Review / Poor).
   - Defect distribution percentage bars (Whole, Broken, Discolored, Insect-damaged, Foreign matter).
   - Transparent mathematical deduction breakdown card explaining exact point penalties.
   - **Interactive AI Evidence Viewer**: Zoomable image canvas with toggleable bounding boxes; clicking any detected grain displays Object ID, classification, confidence level, and pixel area with low-confidence warning tags.
   - Direct button to view/print the official Digital Certificate.

4. **`CertificateView.jsx` (`/inspect/:id/certificate`)**:
   - Official tamper-evident Digital Grain Quality Certificate.
   - Includes Certificate Number, timestamp, verified lot details, defect breakdown, annotated sample snapshot, and scannable QR code.
   - Print-optimized stylesheet (`@media print`) for 1-click physical printing or PDF saving.

5. **`PublicVerify.jsx` (`/verify/:token`)**:
   - Publicly accessible, unauthenticated certificate verification page (matching QR code destination).
   - Displays authentic seal, timestamp, grade decision, and defect statistics, preventing counterfeit inspection reports.

6. **`History.jsx` (`/history`)**:
   - Filterable, searchable audit log of all historical inspections.
   - Instant search by Farmer ID / Batch Ref and filter by Grain Type or Quality Category.

---

## 3. Components

- **`Navbar.jsx`**: Responsive top bar with system status, active AI mode indicator (`DEMO` vs `MODEL`), and direct navigation links.
- **`CameraCapture.jsx`**: Fullscreen/modal camera viewport with interactive rectangular tray guide, camera flip, flash hint, capture button, and drag-and-drop sample loader.
- **`EvidenceViewer.jsx`**: Interactive canvas/SVG overlay allowing users to hover/click individual grain detections, highlight defects, and filter by class.
- **`QualityScoreGauge.jsx`**: High-impact circular SVG score gauge with dynamic color-coding.
- **`DefectProgressBar.jsx`**: Multi-class stacked/individual progress bars with configurable warning thresholds.
- **`DeductionCard.jsx`**: Plain-English, transparent formula breakdown explaining exact score deductions.
- **`QualityBadge.jsx`**: Reusable status pills (Excellent, Good, Needs Review, Rejected).
- **`DemoBanner.jsx`**: Prominent disclaimer banner displayed when backend operates in Demo CV mode.

---

## 4. State Management
- Lightweight native React state with Context API (`InspectionContext`) for managing:
  - Active inspection session draft.
  - Camera device permissions and captured blobs.
  - Global backend health & active AI mode cache.
- Local component states for modal popups, interactive image zoom/hover, and filtering.

---

## 5. API Communication
- Centralized Axios-free native `fetch` client in `src/services/api.js`:
  - `getHealth()`: Checks backend connectivity and active AI mode.
  - `createInspection(data)`: Initializes draft session (`POST /api/inspections`).
  - `analyzeInspection(id, imageBlob)`: Transmits image via `multipart/form-data` to (`POST /api/inspections/{id}/analyze`).
  - `getInspection(id)`: Fetches full result with detections (`GET /api/inspections/{id}`).
  - `listInspections(params)`: Retrieves filtered history (`GET /api/inspections`).
  - `verifyCertificate(token)`: Public lookup (`GET /api/verify/{token}`).

---

## 6. User Flow

```
[ Dashboard ] ──► [ Click "New Inspection" ]
                         │
                         ▼
        [ Step 1: Select Rice & Enter Batch ID ]
                         │
                         ▼
        [ Step 2: Align Camera Over Tray & Snap ]
                         │
                         ▼
        [ Uploading & Analyzing... Progress State ]
                         │
                         ▼
        [ Results Screen: Score + AI Evidence Inspector ]
                         │
                         ▼
        [ Click "Generate Digital Certificate" ]
                         │
                         ▼
        [ Official Certificate with Live QR Code ]
                         │
                         ▼
   (Scan QR) ──► [ Public /verify/:token Screen ]
```

---

## 7. Frontend Folder Structure

```
frontend/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── index.css
    ├── context/
    │   └── AppContext.jsx
    ├── services/
    │   └── api.js
    ├── components/
    │   ├── Navbar.jsx
    │   ├── CameraCapture.jsx
    │   ├── EvidenceViewer.jsx
    │   ├── QualityScoreGauge.jsx
    │   ├── QualityBadge.jsx
    │   ├── DeductionCard.jsx
    │   └── DemoBanner.jsx
    ├── pages/
    │   ├── Dashboard.jsx
    │   ├── NewInspection.jsx
    │   ├── InspectionResult.jsx
    │   ├── CertificateView.jsx
    │   ├── History.jsx
    │   └── PublicVerify.jsx
    └── utils/
        └── helpers.js
```

---

# Complete Frontend Implementation

FILE: frontend/package.json
```json
{
  "name": "grainguard-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^0.344.0",
    "qrcode.react": "^3.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.3"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "vite": "^5.1.6"
  }
}
```

FILE: frontend/vite.config.js
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

FILE: frontend/postcss.config.js
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

FILE: frontend/tailwind.config.js
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0fdf4',
          100: '#dcfce7',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        }
      }
    },
  },
  plugins: [],
}
```

FILE: frontend/index.html
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2315803d'><path d='M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'/></svg>" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>GrainGuard — AI Grain Quality Inspection</title>
  </head>
  <body class="bg-slate-50 text-slate-900 antialiased min-h-screen">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

FILE: frontend/src/index.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-50 text-slate-800 selection:bg-emerald-100 selection:text-emerald-900;
  }
}

@media print {
  body {
    background: white !important;
    color: black !important;
  }
  .no-print {
    display: none !important;
  }
}
```

FILE: frontend/src/utils/helpers.js
```javascript
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
```

FILE: frontend/src/services/api.js
```javascript
const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend health check failed');
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
    throw new Error(err.detail || 'Failed to initialize inspection');
  }
  return res.json();
}

export async function analyzeInspection(inspectionId, imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);

  const res = await fetch(`${API_BASE}/inspections/${inspectionId}/analyze`, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Image analysis failed');
  }
  return res.json();
}

export async function getInspection(inspectionId) {
  const res = await fetch(`${API_BASE}/inspections/${inspectionId}`);
  if (!res.ok) throw new Error('Failed to retrieve inspection');
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
  if (!res.ok) throw new Error('Failed to list inspections');
  return res.json();
}

export async function verifyCertificateToken(token) {
  const res = await fetch(`${API_BASE}/verify/${token}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Invalid or expired certificate');
  }
  return res.json();
}
```

FILE: frontend/src/context/AppContext.jsx
```javascript
import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchHealth } from '../services/api';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [systemHealth, setSystemHealth] = useState({
    status: 'checking',
    ai_mode: 'demo',
    model_loaded: false
  });
  const [activeSession, setActiveSession] = useState(null);

  const checkHealth = async () => {
    try {
      const data = await fetchHealth();
      setSystemHealth(data);
    } catch (err) {
      setSystemHealth({
        status: 'offline',
        ai_mode: 'demo',
        model_loaded: false,
        error: err.message
      });
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <AppContext.Provider value={{ systemHealth, checkHealth, activeSession, setActiveSession }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
```

FILE: frontend/src/components/DemoBanner.jsx
```javascript
import React from 'react';
import { Info, Cpu, CheckCircle2 } from 'lucide-react';
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
```

FILE: frontend/src/components/Navbar.jsx
```javascript
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShieldCheck, PlusCircle, History, LayoutDashboard, Sparkles } from 'lucide-react';
import { useApp } from '../context/AppContext';

export default function Navbar() {
  const location = useLocation();
  const { systemHealth } = useApp();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="bg-slate-900 text-white sticky top-0 z-40 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Brand */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="bg-emerald-600 p-2 rounded-lg text-white shadow-sm group-hover:bg-emerald-500 transition-colors">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg tracking-tight">GrainGuard</span>
                <span className="bg-emerald-950 border border-emerald-600 text-emerald-300 text-[10px] font-semibold px-1.5 py-0.5 rounded">
                  MVP
                </span>
              </div>
              <p className="text-xs text-slate-400 -mt-0.5 hidden sm:block">AI Mandi Grain Quality & Certification</p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="flex items-center gap-1 sm:gap-2">
            <Link
              to="/"
              className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/')
                  ? 'bg-slate-800 text-emerald-400'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span className="hidden sm:inline">Dashboard</span>
            </Link>

            <Link
              to="/inspect/new"
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/inspect/new')
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-emerald-700 hover:bg-emerald-600 text-white'
              }`}
            >
              <PlusCircle className="w-4 h-4" />
              <span>New Inspection</span>
            </Link>

            <Link
              to="/history"
              className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/history')
                  ? 'bg-slate-800 text-emerald-400'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <History className="w-4 h-4" />
              <span className="hidden sm:inline">History</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}
```

FILE: frontend/src/components/QualityBadge.jsx
```javascript
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
```

FILE: frontend/src/components/QualityScoreGauge.jsx
```javascript
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
```

FILE: frontend/src/components/DeductionCard.jsx
```javascript
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
```

FILE: frontend/src/components/EvidenceViewer.jsx
```javascript
import React, { useState, useRef } from 'react';
import { CLASS_METADATA } from '../utils/helpers';
import { Eye, Filter, AlertCircle, Info, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';

export default function EvidenceViewer({ imageUrl, annotatedImageUrl, detections = [] }) {
  const [selectedFilter, setSelectedFilter] = useState('ALL');
  const [selectedDetection, setSelectedDetection] = useState(null);
  const [showAnnotated, setShowAnnotated] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(1);

  const filteredDetections = detections.filter(d => {
    if (selectedFilter === 'ALL') return true;
    return d.class_name === selectedFilter;
  });

  const activeImage = showAnnotated && annotatedImageUrl ? annotatedImageUrl : imageUrl;

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
```

FILE: frontend/src/components/CameraCapture.jsx
```javascript
import React, { useState, useRef, useEffect } from 'react';
import { Camera, RefreshCw, Upload, AlertTriangle, Check, FlipHorizontal } from 'lucide-react';

export default function CameraCapture({ onCapture, onSamplePick }) {
  const [stream, setStream] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // Default to rear camera
  const [capturedPreview, setCapturedPreview] = useState(null);
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);

  // Initialize camera stream
  const startCamera = async () => {
    setCameraError(null);
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }

    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.warn('Camera access error:', err);
      setCameraError('Camera stream unavailable. Please use file upload or demo samples.');
    }
  };

  useEffect(() => {
    startCamera();
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [facingMode]);

  const toggleCamera = () => {
    setFacingMode(prev => (prev === 'environment' ? 'user' : 'environment'));
  };

  const handleCaptureFrame = () => {
    if (!videoRef.current) return;

    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      if (!blob) return;
      const previewUrl = URL.createObjectURL(blob);
      setCapturedPreview(previewUrl);
      onCapture(blob);
    }, 'image/jpeg', 0.92);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const previewUrl = URL.createObjectURL(file);
      setCapturedPreview(previewUrl);
      onCapture(file);
    }
  };

  // Generate synthetic sample photo for rapid testing if no real photo is handy
  const handleGenerateSample = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 1000;
    canvas.height = 1000;
    const ctx = canvas.getContext('2d');

    // Dark contrasting background tray
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, 1000, 1000);

    // Physical tray border
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 14;
    ctx.strokeRect(40, 40, 920, 920);

    // Draw realistic grain cluster
    const rows = 12;
    const cols = 14;
    for (let r = 1; r <= rows; r++) {
      for (let c = 1; c <= cols; c++) {
        const x = c * 62 + (Math.sin(r * c) * 12);
        const y = r * 68 + (Math.cos(r + c) * 10);
        
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate((r * 37 + c * 19) * Math.PI / 180);

        const isDiscolored = (r * c) % 17 === 0;
        const isBroken = (r + c) % 11 === 0;
        const isInsect = (r * c) % 29 === 0;
        const isForeign = (r * c) % 43 === 0;

        if (isForeign) {
          ctx.fillStyle = '#7c3aed'; // Purple foreign stone
          ctx.beginPath();
          ctx.arc(0, 0, 8, 0, Math.PI * 2);
          ctx.fill();
        } else if (isInsect) {
          ctx.fillStyle = '#dc2626'; // Red insect damaged grain
          ctx.beginPath();
          ctx.ellipse(0, 0, 16, 6, 0, 0, Math.PI * 2);
          ctx.fill();
        } else if (isDiscolored) {
          ctx.fillStyle = '#d97706'; // Amber discolored
          ctx.beginPath();
          ctx.ellipse(0, 0, 18, 7, 0, 0, Math.PI * 2);
          ctx.fill();
        } else if (isBroken) {
          ctx.fillStyle = '#f8fafc'; // White broken half
          ctx.beginPath();
          ctx.ellipse(0, 0, 9, 6, 0, 0, Math.PI * 2);
          ctx.fill();
        } else {
          ctx.fillStyle = '#ffffff'; // Pristine whole grain
          ctx.beginPath();
          ctx.ellipse(0, 0, 20, 7, 0, 0, Math.PI * 2);
          ctx.fill();
        }

        ctx.restore();
      }
    }

    canvas.toBlob(blob => {
      if (!blob) return;
      const previewUrl = URL.createObjectURL(blob);
      setCapturedPreview(previewUrl);
      onCapture(blob);
    }, 'image/jpeg', 0.95);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
      <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div>
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <Camera className="w-4 h-4 text-emerald-600" />
            Smartphone Sample Capture
          </h3>
          <p className="text-xs text-slate-500">
            Position smartphone directly top-down over contrasting sample tray
          </p>
        </div>

        {stream && (
          <button
            onClick={toggleCamera}
            className="flex items-center gap-1.5 text-xs text-slate-600 bg-white border border-slate-200 px-2.5 py-1.5 rounded-lg hover:bg-slate-100"
          >
            <FlipHorizontal className="w-3.5 h-3.5" />
            <span>Flip Cam</span>
          </button>
        )}
      </div>

      <div className="p-4">
        {capturedPreview ? (
          /* Captured Preview Confirmation */
          <div className="flex flex-col items-center">
            <div className="relative max-w-md w-full rounded-xl overflow-hidden border-2 border-emerald-500 shadow-md">
              <img src={capturedPreview} alt="Captured Sample" className="w-full h-auto object-cover" />
              <div className="absolute top-2 left-2 bg-emerald-600 text-white text-[11px] font-semibold px-2.5 py-1 rounded-full flex items-center gap-1 shadow">
                <Check className="w-3.5 h-3.5" /> Sample Photo Ready
              </div>
            </div>
            <div className="mt-4 flex gap-3">
              <button
                type="button"
                onClick={() => {
                  setCapturedPreview(null);
                  onCapture(null);
                }}
                className="px-4 py-2 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100 flex items-center gap-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Retake Photo
              </button>
            </div>
          </div>
        ) : (
          /* Camera Viewport or Fallback */
          <div className="flex flex-col items-center">
            <div className="relative w-full max-w-md aspect-[4/3] bg-slate-950 rounded-xl overflow-hidden flex items-center justify-center border border-slate-800">
              {stream ? (
                <>
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover"
                  />
                  {/* Tray Alignment Overlay */}
                  <div className="absolute inset-6 border-2 border-dashed border-emerald-400/80 rounded-lg pointer-events-none flex flex-col justify-between p-3">
                    <span className="text-[10px] bg-slate-900/80 text-emerald-300 px-2 py-0.5 rounded self-start font-mono">
                      ALIGN TRAY BOUNDARY HERE
                    </span>
                    <span className="text-[10px] bg-slate-900/80 text-slate-300 px-2 py-0.5 rounded self-end">
                      Keep Camera Level
                    </span>
                  </div>
                </>
              ) : (
                <div className="text-center p-6 text-slate-400">
                  <Camera className="w-10 h-10 mx-auto mb-2 text-slate-600" />
                  <p className="text-xs">{cameraError || 'Loading camera stream...'}</p>
                </div>
              )}
            </div>

            {/* Shutter Button & Fallbacks */}
            <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
              {stream && (
                <button
                  type="button"
                  onClick={handleCaptureFrame}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2.5 rounded-xl shadow-md flex items-center gap-2 text-sm transition-all transform active:scale-95"
                >
                  <Camera className="w-4 h-4" /> Capture Tray Photo
                </button>
              )}

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleFileUpload}
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 shadow-sm"
              >
                <Upload className="w-3.5 h-3.5 text-slate-500" /> Upload Image File
              </button>

              <button
                type="button"
                onClick={handleGenerateSample}
                className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3.5 py-2.5 rounded-xl text-xs flex items-center gap-1.5"
                title="Generates high-contrast sample with mixed defects"
              >
                Use Sample Rice Tray
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

FILE: frontend/src/pages/Dashboard.jsx
```javascript
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlusCircle, 
  CheckCircle2, 
  AlertOctagon, 
  TrendingUp, 
  Clock, 
  ArrowRight, 
  FileCheck,
  Wheat,
  ShieldCheck,
  Search
} from 'lucide-react';
import { listInspections } from '../services/api';
import QualityBadge from '../components/QualityBadge';
import { formatDate } from '../utils/helpers';
import { useApp } from '../context/AppContext';

export default function Dashboard() {
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const { systemHealth } = useApp();

  const loadData = async () => {
    try {
      setLoading(true);
      const data = await listInspections({ limit: 8 });
      setInspections(data.items || []);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Compute summary stats
  const total = inspections.length;
  const avgScore = total > 0 
    ? (inspections.reduce((acc, i) => acc + (i.quality_score || 0), 0) / total).toFixed(1)
    : '0.0';
  const flaggedCount = inspections.filter(i => (i.quality_score || 0) < 75).length;

  return (
    <div className="space-y-6">
      
      {/* Top Welcome & Fast Action Banner */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white rounded-2xl p-6 shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
              Rural Intake Station #01
            </span>
            <span className="text-xs text-slate-400">Node Active</span>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight">Grain Quality Intake Hub</h1>
          <p className="text-slate-300 text-sm mt-1 max-w-xl">
            Objective, explainable smartphone-based grain defect inspection and auditable digital certification.
          </p>
        </div>

        <Link
          to="/inspect/new"
          className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-6 py-3 rounded-xl shadow-lg flex items-center gap-2 text-sm transition-all transform hover:-translate-y-0.5"
        >
          <PlusCircle className="w-5 h-5" /> Start New Inspection
        </Link>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Recent Intake Batches</span>
            <FileCheck className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{total}</span>
            <span className="text-xs text-slate-500">inspected</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Average Quality Score</span>
            <TrendingUp className="w-4 h-4 text-blue-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{avgScore}</span>
            <span className="text-xs text-slate-400 font-mono">/ 100</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Flagged / Review</span>
            <AlertOctagon className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-amber-600">{flaggedCount}</span>
            <span className="text-xs text-slate-500">require re-check</span>
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">AI Pipeline Mode</span>
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-sm font-bold text-slate-800 uppercase font-mono">
              {systemHealth.ai_mode === 'model' ? 'ONNX Neural Net' : 'Morphological CV'}
            </span>
          </div>
        </div>
      </div>

      {/* Recent Inspections Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-5 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h2 className="font-bold text-slate-900 text-base">Recent Grain Inspections</h2>
            <p className="text-xs text-slate-500">Live feed of verified Mandi intake assessments</p>
          </div>
          <Link
            to="/history"
            className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center gap-1"
          >
            View All History <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading inspection records...</div>
        ) : inspections.length === 0 ? (
          <div className="p-12 text-center">
            <Wheat className="w-12 h-12 mx-auto text-slate-300 mb-3" />
            <h3 className="font-semibold text-slate-800 text-sm">No inspections recorded yet</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              Place a grain sample on the tray and start your first smartphone AI inspection.
            </p>
            <Link
              to="/inspect/new"
              className="mt-4 inline-flex items-center gap-1.5 bg-emerald-600 text-white text-xs font-bold px-4 py-2 rounded-lg"
            >
              <PlusCircle className="w-4 h-4" /> Start Inspection
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 uppercase text-[11px] font-semibold border-b border-slate-200">
                <tr>
                  <th className="px-5 py-3">Inspection ID & Time</th>
                  <th className="px-4 py-3">Grain</th>
                  <th className="px-4 py-3">Farmer / Batch Reference</th>
                  <th className="px-4 py-3">Grains Analyzed</th>
                  <th className="px-4 py-3">Quality Score</th>
                  <th className="px-4 py-3">Grade Category</th>
                  <th className="px-5 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {inspections.map((insp) => (
                  <tr key={insp.inspection_id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-5 py-3.5">
                      <div className="font-mono font-medium text-slate-900">
                        {insp.inspection_id.substring(0, 8)}...
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
                        View Results <ArrowRight className="w-3 h-3" />
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
```

FILE: frontend/src/pages/NewInspection.jsx
```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createInspection, analyzeInspection } from '../services/api';
import CameraCapture from '../components/CameraCapture';
import { Wheat, ArrowRight, ShieldCheck, AlertCircle, Loader2 } from 'lucide-react';

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
```

FILE: frontend/src/pages/InspectionResult.jsx
```javascript
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getInspection } from '../services/api';
import QualityScoreGauge from '../components/QualityScoreGauge';
import QualityBadge from '../components/QualityBadge';
import DeductionCard from '../components/DeductionCard';
import EvidenceViewer from '../components/EvidenceViewer';
import { CLASS_METADATA, formatDate } from '../utils/helpers';
import { 
  FileCheck, 
  Clock, 
  Wheat, 
  ArrowLeft, 
  Award, 
  ShieldCheck, 
  Share2, 
  Printer, 
  Cpu,
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
```

FILE: frontend/src/pages/CertificateView.jsx
```javascript
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getInspection } from '../services/api';
import { QRCodeSVG } from 'qrcode.react';
import { formatDate } from '../utils/helpers';
import QualityBadge from '../components/QualityBadge';
import { ShieldCheck, Award, Printer, ArrowLeft, CheckCircle2, Lock } from 'lucide-react';

export default function CertificateView() {
  const { id } = useParams();
  const [inspection, setInspection] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCert = async () => {
      try {
        const data = await getInspection(id);
        setInspection(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCert();
  }, [id]);

  if (loading || !inspection) {
    return <div className="py-20 text-center text-xs text-slate-400">Loading Certificate...</div>;
  }

  const cert = inspection.certificate || {};
  const qr = inspection.quality_result || {};
  const verifyUrl = `${window.location.origin}/verify/${cert.verification_token}`;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* Action Bar */}
      <div className="flex items-center justify-between no-print">
        <Link
          to={`/inspect/${inspection.inspection_id}`}
          className="text-xs font-semibold text-slate-600 hover:text-slate-900 flex items-center gap-1"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Results
        </Link>
        <button
          onClick={() => window.print()}
          className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-sm"
        >
          <Printer className="w-4 h-4" /> Print / Save PDF
        </button>
      </div>

      {/* Official Certificate Paper Container */}
      <div className="bg-white rounded-2xl border-4 border-slate-900 p-8 sm:p-10 shadow-xl relative overflow-hidden">
        
        {/* Watermark Emblem */}
        <div className="absolute right-4 bottom-4 opacity-5 pointer-events-none">
          <ShieldCheck className="w-96 h-96 text-slate-900" />
        </div>

        {/* Certificate Header */}
        <div className="border-b-2 border-slate-900 pb-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <div className="bg-emerald-700 text-white p-2 rounded-lg">
              <ShieldCheck className="w-7 h-7" />
            </div>
            <span className="text-2xl font-black tracking-wider uppercase text-slate-900">
              GrainGuard
            </span>
          </div>
          <h1 className="text-lg font-bold uppercase tracking-widest text-slate-800">
            Digital Grain Quality Intake Certificate
          </h1>
          <p className="text-xs text-slate-500 font-mono mt-0.5">
            Cryptographically Tamper-Evident Mandi Audit Record
          </p>
        </div>

        {/* Certificate Metadata Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-6 border-b border-slate-200 text-xs">
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Certificate Number</span>
            <div className="font-bold font-mono text-slate-900 mt-0.5">
              {cert.certificate_number || 'GG-2025-001'}
            </div>
          </div>
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Date & Time</span>
            <div className="font-medium text-slate-800 mt-0.5">
              {formatDate(inspection.created_at)}
            </div>
          </div>
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Commodity</span>
            <div className="font-bold text-slate-900 capitalize mt-0.5">
              {inspection.grain_type}
            </div>
          </div>
          <div>
            <span className="text-slate-400 uppercase text-[10px] font-semibold">Batch / Farmer Ref</span>
            <div className="font-medium text-slate-800 mt-0.5">
              {inspection.farmer_reference || 'N/A'}
            </div>
          </div>
        </div>

        {/* Quality Score & Grade Hero */}
        <div className="py-6 border-b border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-6 bg-slate-50 rounded-xl px-6 my-6">
          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-slate-500">
              Assigned Intake Grade
            </span>
            <div className="mt-1 flex items-center gap-3">
              <QualityBadge category={qr.category} size="large" />
              <span className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-1 rounded">
                STATUS: {qr.decision || 'ACCEPTABLE'}
              </span>
            </div>
          </div>

          <div className="text-center sm:text-right">
            <span className="text-xs uppercase tracking-wider font-semibold text-slate-500">
              Verified Quality Score
            </span>
            <div className="text-3xl font-extrabold text-slate-900 font-mono">
              {inspection.quality_score.toFixed(1)} <span className="text-sm font-normal text-slate-400">/ 100</span>
            </div>
          </div>
        </div>

        {/* Defect Statistics Table */}
        <div className="mb-6">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2.5">
            Defect Composition (Sample Count: {inspection.total_objects} items)
          </h3>
          <table className="w-full text-xs text-left border border-slate-200">
            <thead className="bg-slate-100 text-slate-700 font-semibold text-[11px]">
              <tr>
                <th className="p-2.5 border-b border-slate-200">Visual Quality Class</th>
                <th className="p-2.5 border-b border-slate-200 text-right">Composition %</th>
                <th className="p-2.5 border-b border-slate-200 text-right">Assigned Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              <tr>
                <td className="p-2.5 font-medium">Whole Sound Grain</td>
                <td className="p-2.5 text-right font-mono font-bold text-emerald-700">{qr.whole_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-emerald-700 font-semibold">PASS</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Broken Grain Fragment (&lt; 3/4)</td>
                <td className="p-2.5 text-right font-mono">{qr.broken_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-slate-600">AUDITED</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Discolored / Chalky Grain</td>
                <td className="p-2.5 text-right font-mono">{qr.discolored_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-slate-600">AUDITED</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Insect Damaged Kernels</td>
                <td className="p-2.5 text-right font-mono text-rose-600">{qr.insect_damage_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-rose-600 font-semibold">FLAGGED</td>
              </tr>
              <tr>
                <td className="p-2.5 font-medium">Foreign Matter / Non-Grain</td>
                <td className="p-2.5 text-right font-mono text-purple-700">{qr.foreign_matter_percentage?.toFixed(2)}%</td>
                <td className="p-2.5 text-right text-purple-700 font-semibold">FLAGGED</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Verification QR & Legal Footer */}
        <div className="pt-6 border-t-2 border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="p-2 bg-white border border-slate-300 rounded-lg shadow-sm">
              <QRCodeSVG value={verifyUrl} size={84} level="M" />
            </div>
            <div className="text-xs">
              <div className="font-bold text-slate-900 flex items-center gap-1">
                <Lock className="w-3.5 h-3.5 text-emerald-600" /> Scan QR to Verify Authenticity
              </div>
              <p className="text-[11px] text-slate-500 max-w-xs mt-0.5">
                Token: <span className="font-mono">{cert.verification_token}</span>
              </p>
            </div>
          </div>

          <div className="text-center sm:text-right text-[11px] text-slate-400">
            <div>Authorized Procurement Officer Node</div>
            <div className="font-mono text-slate-700 font-bold mt-0.5">DIGITALLY SIGNED & SEALED</div>
          </div>
        </div>

      </div>
    </div>
  );
}
```

FILE: frontend/src/pages/PublicVerify.jsx
```javascript
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { verifyCertificateToken } from '../services/api';
import QualityBadge from '../components/QualityBadge';
import { formatDate } from '../utils/helpers';
import { ShieldCheck, CheckCircle2, AlertTriangle, Lock, Wheat, ArrowRight } from 'lucide-react';

export default function PublicVerify() {
  const { token } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const runVerification = async () => {
      try {
        setLoading(true);
        const res = await verifyCertificateToken(token);
        setData(res);
      } catch (err) {
        setError(err.message || 'Verification failed');
      } finally {
        setLoading(false);
      }
    };
    runVerification();
  }, [token]);

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      {loading ? (
        <div className="p-16 text-center text-xs text-slate-400">
          Cryptographically verifying certificate token...
        </div>
      ) : error || !data?.verified ? (
        <div className="bg-white rounded-2xl border border-rose-200 p-8 shadow-sm text-center">
          <AlertTriangle className="w-12 h-12 text-rose-600 mx-auto mb-3" />
          <h1 className="text-lg font-bold text-slate-900">Certificate Verification Failed</h1>
          <p className="text-xs text-slate-600 mt-2 max-w-md mx-auto">
            The verification token <code className="bg-slate-100 p-1 rounded font-mono text-rose-700">{token}</code> is either invalid, revoked, or has been tampered with.
          </p>
          <Link
            to="/"
            className="mt-6 inline-flex items-center gap-1.5 bg-slate-900 text-white text-xs font-semibold px-4 py-2 rounded-lg"
          >
            Go to GrainGuard Home
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border-2 border-emerald-600 p-8 shadow-lg">
          
          {/* Verified Seal Header */}
          <div className="text-center pb-6 border-b border-slate-200">
            <div className="w-14 h-14 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mx-auto mb-3 shadow-inner">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <span className="bg-emerald-100 text-emerald-800 text-[11px] font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              Official Tamper-Proof Audit
            </span>
            <h1 className="text-xl font-black text-slate-900 mt-2 uppercase tracking-wide">
              Certificate Verified Authentic
            </h1>
            <p className="text-xs text-slate-500 font-mono mt-0.5">
              Cert ID: {data.certificate_number}
            </p>
          </div>

          {/* Core Verified Details */}
          <div className="py-5 grid grid-cols-2 gap-4 text-xs border-b border-slate-200">
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Inspection Date</span>
              <div className="font-semibold text-slate-800 mt-0.5">{formatDate(data.inspection_date)}</div>
            </div>
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Commodity Type</span>
              <div className="font-bold text-slate-900 capitalize mt-0.5">{data.grain_type}</div>
            </div>
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Batch / Farmer Reference</span>
              <div className="font-medium text-slate-800 mt-0.5">{data.farmer_reference || 'N/A'}</div>
            </div>
            <div>
              <span className="text-slate-400 uppercase text-[10px] font-semibold">Sample Analyzed</span>
              <div className="font-bold font-mono text-slate-900 mt-0.5">{data.total_objects} Grains</div>
            </div>
          </div>

          {/* Grade & Score */}
          <div className="py-4 my-4 bg-slate-50 rounded-xl px-5 flex items-center justify-between border border-slate-100">
            <div>
              <span className="text-[10px] uppercase font-bold text-slate-400">Intake Grade Category</span>
              <div className="mt-1">
                <QualityBadge category={data.category} size="large" />
              </div>
            </div>
            <div className="text-right">
              <span className="text-[10px] uppercase font-bold text-slate-400">Quality Score</span>
              <div className="text-2xl font-extrabold font-mono text-slate-900">
                {data.quality_score?.toFixed(1)} <span className="text-xs text-slate-400 font-normal">/ 100</span>
              </div>
            </div>
          </div>

          {/* Defect Metrics */}
          <div className="space-y-2 text-xs">
            <h4 className="font-bold text-slate-800 text-[11px] uppercase tracking-wider">Defect Breakdown</h4>
            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Whole Grain:</span>
                <span className="font-bold text-emerald-700">{data.statistics?.whole_percentage?.toFixed(1)}%</span>
              </div>
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Broken Grain:</span>
                <span className="font-mono font-semibold text-slate-800">{data.statistics?.broken_percentage?.toFixed(1)}%</span>
              </div>
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Discolored:</span>
                <span className="font-mono font-semibold text-slate-800">{data.statistics?.discolored_percentage?.toFixed(1)}%</span>
              </div>
              <div className="p-2 bg-slate-50 rounded border border-slate-100 flex justify-between">
                <span className="text-slate-600">Insect Damaged:</span>
                <span className="font-mono font-bold text-rose-600">{data.statistics?.insect_damage_percentage?.toFixed(1)}%</span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-200 text-center text-[11px] text-slate-400 flex items-center justify-center gap-1">
            <Lock className="w-3.5 h-3.5 text-emerald-600" />
            Verified via GrainGuard Decentralized Mandi Node
          </div>

        </div>
      )}
    </div>
  );
}
```

FILE: frontend/src/pages/History.jsx
```javascript
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listInspections } from '../services/api';
import QualityBadge from '../components/QualityBadge';
import { formatDate } from '../utils/helpers';
import { Search, Filter, Clock, ArrowRight, Wheat } from 'lucide-react';

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
```

FILE: frontend/src/App.jsx
```javascript
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import DemoBanner from './components/DemoBanner';
import Dashboard from './pages/Dashboard';
import NewInspection from './pages/NewInspection';
import InspectionResult from './pages/InspectionResult';
import CertificateView from './pages/CertificateView';
import History from './pages/History';
import PublicVerify from './pages/PublicVerify';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <DemoBanner />
      <Navbar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inspect/new" element={<NewInspection />} />
          <Route path="/inspect/:id" element={<InspectionResult />} />
          <Route path="/inspect/:id/certificate" element={<CertificateView />} />
          <Route path="/history" element={<History />} />
          <Route path="/verify/:token" element={<PublicVerify />} />
        </Routes>
      </main>
      
      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-400 no-print">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>GrainGuard — AI Smartphone Grain Quality Assessment & Certification</span>
          <span>Targeting Visually Observable Grain Characteristics</span>
        </div>
      </footer>
    </div>
  );
}
```

FILE: frontend/src/main.jsx
```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import { AppProvider } from './context/AppContext.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AppProvider>
        <App />
      </AppProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
```

---

## FRONTEND SETUP COMMANDS

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install all dependencies
npm install
```

---

## FRONTEND RUN COMMANDS

```bash
# Start Vite development server (port 5173 with API proxy to backend on port 8000)
npm run dev
```

*Frontend will be immediately available at `http://localhost:5173`.*

---

## Complete End-to-End Workflow Verification

```bash
1. Open http://localhost:5173
2. Click "New Inspection"
3. Select Commodity: Rice, Enter Farmer Reference: "BATCH-891"
4. Click "Use Sample Rice Tray" (or snap camera photograph)
5. Click "Run AI Analysis"
6. Review the resulting Quality Score Gauge, Defect Distribution %, and interactive AI Evidence Viewer
7. Click "Generate Certificate" to view the digital certificate with verifiable QR code
8. Click/Scan the QR code to open the public verification screen at /verify/:token
9. Return to Dashboard / History to observe the saved record
```