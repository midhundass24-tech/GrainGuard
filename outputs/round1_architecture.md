# GrainGuard — System Architecture Specification (MVP)

---

## 1. Project Overview
**GrainGuard** is an AI-powered, smartphone-based visual grain quality inspection and digital certification system designed for rural grain procurement centers, primary agricultural cooperatives, and aggregation gates. 

The core value proposition follows the **SEE → MEASURE → VERIFY** workflow:
- **SEE**: Operators capture a high-contrast top-down photograph of a representative grain sample using a standard smartphone camera and a physical tray.
- **MEASURE**: An edge-ready/lightweight computer vision pipeline segments individual grains, classifies visible defects (whole, broken, discolored, insect-damaged, foreign matter), and applies an explainable, configurable scoring model.
- **VERIFY**: The system issues a cryptographically tamper-evident digital certificate with a verifiable QR code, making intake inspection results transparent, traceable, and auditable.

*Disclaimer & Scope*: GrainGuard is designed strictly for **visible physical grain quality characteristics** and serves as an auditable digital intake assessment. It does not replace laboratory chemical/NIR assays (e.g., moisture, protein content, mycotoxin presence) nor does it dictate statutory government price fixes.

---

## 2. Target Users
1. **Procurement Gate Agents / Field Operators**: Non-technical personnel operating in rural warehouses and intake points requiring a fast, one-handed mobile capture workflow with minimal typing and clear pass/review indicators.
2. **Farmers / Grain Suppliers**: Require clear, explainable, visual proof (bounding boxes, defect percentages) of why a sample received a specific grade, eliminating arbitrary grading disputes.
3. **Auditors / Warehouse Managers / Off-Takers**: Need instant verification of inspection certificates via public QR lookup to validate batch quality before dispatching payments or loading silos.

---

## 3. User Workflow

```
[ 1. Select Grain Type (Rice) & Batch Ref ]
                     │
                     ▼
[ 2. Capture / Upload Top-Down Sample Photo ]
                     │
                     ▼
[ 3. Pre-Flight Validation (Blur, Lighting, Tray Boundary) ]
        │                                  │
      (Pass)                             (Fail) ──► [ Request Recapture with Guidance ]
        ▼
[ 4. Inference (Model or Deterministic Demo) ]
                     │
                     ▼
[ 5. Quality Score & Defect Engine Computation ]
                     │
                     ▼
[ 6. Interactive Review Screen (AI Bounding Box Evidence + Deductions) ]
                     │
                     ▼
[ 7. Generate Signed Digital Certificate + QR Code ]
                     │
                     ▼
[ 8. Public Verification via QR Scan (/verify/{token}) ]
```

---

## 4. System Architecture

The MVP uses a monolithic client-server architecture designed for local execution or containerized single-host deployment.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER (Mobile/Browser)                   │
│                                                                        │
│   React (Vite) + Tailwind CSS + Lucide Icons + HTML5 Camera Stream     │
│   ├── Capture Interface (Guided Overlay & Exposure Check)              │
│   ├── Interactive AI Evidence Viewer (SVG/Canvas Bounding Boxes)       │
│   ├── Dashboard & Inspection History (Filterable)                      │
│   └── Public Certificate Verification Page (/verify/:token)            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS / REST (JSON + multipart/form-data)
┌───────────────────────────────────▼────────────────────────────────────┐
│                        API & BACKEND LAYER (FastAPI)                   │
│                                                                        │
│   FastAPI App (Async Uvicorn Server)                                   │
│   ├── Core Middleware (CORS, Request Tracing, Error Handlers)          │
│   ├── Routers (/api/inspections, /api/verify, /api/health)             │
│   ├── Validation & Pydantic Schemas                                    │
│   │                                                                    │
│   ├── Image Preprocessing Engine (OpenCV / PIL)                        │
│   │   ├── Lighting & Laplacian Blur Detection                          │
│   │   └── Contrast Enhancement & Normalization                         │
│   │                                                                    │
│   ├── AI Inference Subsystem (Pluggable Abstraction)                   │
│   │   ├── Model Adapter Interface (`analyze_grain_image`)              │
│   │   ├── PyTorch/YOLO Inference Engine (Real weights if present)       │
│   │   └── Deterministic Synthetic Demo Engine (Fallback)               │
│   │                                                                    │
│   ├── Explainable Quality Engine                                       │
│   │   ├── Weighted Penalties, Configurable Thresholds, Categorization   │
│   │                                                                    │
│   └── Certificate Generation Engine (Pillow/ReportLab + QRCode)        │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
                   ▼                                 ▼
┌───────────────────────────────────────┐ ┌──────────────────────────────┐
│       SQLITE DATABASE (WAL Mode)      │ │   LOCAL PERSISTENCE / STORAGE│
│  ├── inspections    ├── detections    │ │  ├── uploads/ (Raw images)   │
│  ├── quality_results├── certificates  │ │  └── certificates/ (Artifacts│
└───────────────────────────────────────┘ └──────────────────────────────┘
```

---

## 5. Frontend Architecture
- **Framework**: React 18 + Vite (fast HMR, lean bundle).
- **Styling**: Tailwind CSS with custom high-contrast tokens suitable for sunlight outdoor readability (`emerald-800`, `amber-600`, `slate-900`).
- **State Management**: React Context (`InspectionContext`) for wizard flow and active capture states; React Query / native hooks for REST caching.
- **Camera/Media**: Standard HTML5 `navigator.mediaDevices.getUserMedia` with video-to-canvas frame capture and fallback file uploader for testing.
- **Evidence Rendering**: Lightweight `<canvas>` / SVG overlay for interactive bounding-box tooltips (click object $\to$ view class, confidence, pixel area).
- **Routing**: Client-side lightweight hash or browser router (`react-router-dom`).
  - `/` — Operator Dashboard
  - `/inspect/new` — Wizard (Setup $\to$ Camera $\to$ Analysis)
  - `/inspect/:id` — Full Inspection Results & AI Evidence Explainer
  - `/inspect/:id/certificate` — Official Certificate View
  - `/history` — Audit Log & Inspection History
  - `/verify/:token` — Public Verification Screen (Accessible without login)

---

## 6. Backend Architecture
- **Framework**: FastAPI (Python 3.10+) for native async support, automated OpenAPI docs, and clean Pydantic integration.
- **ORM & Database**: SQLAlchemy 2.0 with SQLite (WAL mode enabled for concurrent reads).
- **Image Pipeline**: OpenCV (`cv2`) and NumPy for:
  - Blur check (Variance of Laplacian $> \text{threshold}$).
  - Brightness/Exposure validation (Luminance histogram checks).
  - High-res annotated image rendering with color-coded bounding boxes.
- **AI Core Abstraction**:
  - `GrainModelInterface` defining `predict(image_bytes, grain_type) -> List[GrainDetection]`.
  - Implementation selector dynamically toggling between `YOLOV8GrainModel` and `DeterministicDemoModel` based on `AI_MODE` and model file existence.
- **Execution Strategy**: CPU-optimized inference (TorchScript/ONNX/PyTorch CPU) so no discrete GPU is required for hackathon judges.

---

## 7. Database Architecture

```
                       ┌───────────────────────┐
                       │         users         │
                       ├───────────────────────┤
                       │ PK id                 │
                       │    name               │
                       │    role               │
                       │    created_at         │
                       └───────────┬───────────┘
                                   │ 1
                                   │
                                   │ N
                       ┌───────────▼───────────┐
                       │      inspections      │
                       ├───────────────────────┤
                       │ PK id (UUID)          │
                       │ FK user_id            │
                       │    grain_type         │
                       │    farmer_reference   │
                       │    raw_image_path     │
                       │    annotated_img_path │
                       │    total_objects      │
                       │    processing_time_ms │
                       │    status             │
                       │    ai_mode            │
                       │    created_at         │
                       └─────┬───────────┬─────┘
                             │ 1         │ 1
                 ┌───────────┘           └───────────┐
                 │ 1                                 │ 1
                 ▼ N                                 ▼ 1
┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│           detections            │   │         quality_results         │
├─────────────────────────────────┤   ├─────────────────────────────────┤
│ PK id                           │   │ PK id                           │
│ FK inspection_id                │   │ FK inspection_id                │
│    class_name                   │   │    whole_pct                    │
│    confidence                   │   │    broken_pct                   │
│    x1, y1, x2, y2               │   │    discolored_pct               │
│    area_px                      │   │    insect_damaged_pct           │
│    is_low_confidence            │   │    foreign_matter_pct           │
└─────────────────────────────────┘   │    quality_score (0-100)        │
                                      │    grade_category               │
                                      │    deduction_breakdown (JSON)   │
                                      └─────────────────────────────────┘
                                                     │ 1
                                                     │ 1
                                      ┌──────────────▼──────────────────┐
                                      │           certificates          │
                                      ├─────────────────────────────────┤
                                      │ PK id                           │
                                      │ FK inspection_id                │
                                      │    certificate_number           │
                                      │    verification_token (UUID)    │
                                      │    qr_code_path                 │
                                      │    created_at                   │
                                      └─────────────────────────────────┘
```

---

## 8. AI Architecture & Inference Abstraction

### Object Classes
1. `whole_grain` (Sound grain)
2. `broken_grain` (Fragmented/split grain $< \frac{3}{4}$ original length)
3. `discolored_grain` (Chalky, yellowed, black-tipped, or pecked)
4. `insect_damaged` (Grain with boreholes or weevil damage)
5. `foreign_matter` (Chaff, husk, stones, non-grain particles)

### Model Interface Pattern
```python
class GrainDetection(BaseModel):
    class_name: Literal["whole_grain", "broken_grain", "discolored_grain", "insect_damaged", "foreign_matter"]
    confidence: float
    bbox: Tuple[int, int, int, int]  # [x1, y1, x2, y2]
    area: float

class GrainModelInterface(ABC):
    @abstractmethod
    def analyze_grain_image(self, image_path: str, grain_type: str) -> List[GrainDetection]:
        pass
```

- **Production / Model Mode (`AI_MODE=model`)**:
  - Checks for weights in `backend/models/grain_model.pt` or `.onnx`.
  - Executes inference with NMS (Non-Maximum Suppression) and returns calibrated detections.
- **Deterministic Demo Mode (`AI_MODE=demo`)**:
  - Computes an image perceptual hash (or seed) from input image pixels.
  - Generates realistic, reproducible spatial clusters of bounding boxes mimicking real rice distributions.
  - Flags explicit header/payload `"ai_mode": "demo"` so the UI prominently displays `DEMO INFERENCE MODE`.

---

## 9. API Endpoints

| Method | Endpoint | Description | Payload / Params | Response |
|---|---|---|---|---|
| `GET` | `/api/health` | Healthcheck & system status | None | `{"status": "healthy", "ai_mode": "demo"\|"model", "version": "1.0.0"}` |
| `GET` | `/api/inspections` | List inspection history | `?limit=50&offset=0&grain_type=rice` | Paginated list of inspection summaries |
| `POST` | `/api/inspections` | Initialize new inspection session | `{"grain_type": "rice", "farmer_reference": "BATCH-809"}` | `{"inspection_id": "...", "status": "draft"}` |
| `POST` | `/api/inspections/{id}/analyze` | Upload image & run analysis | `multipart/form-data (file: image/jpeg)` | Complete inspection results, score, detections |
| `GET` | `/api/inspections/{id}` | Retrieve single inspection details | `id` (path) | Full inspection object with detections & score breakdown |
| `GET` | `/api/inspections/{id}/certificate` | Get/Generate certificate data | `id` (path) | Certificate metadata, verification token, QR image path |
| `GET` | `/api/verify/{token}` | Public tamper verification | `token` (path) | Sanitized public audit data (Grade, counts, timestamp) |

---

## 10. External Services
* **Zero Mandatory Cloud Dependencies**: To satisfy hackathon reliability requirements and rural offline scenarios, the entire stack (FastAPI, SQLite, OpenCV, PyTorch, React) runs locally without third-party cloud APIs (AWS, Firebase, or OpenAI).
* **QR Code Generation**: Self-contained using Python `qrcode[pil]` library locally.

---

## 11. Authentication Requirements
* **MVP Strategy**: Simplified single-tenant / role-tagged session model.
* No passwords/OAuth required for the hackathon MVP to eliminate login friction for judges.
* Default identity is assigned as `"Lead Procurement Officer (Gate #1)"`.
* Verification endpoints (`/api/verify/{token}`) are completely open and public by design.

---

## 12. Project Folder Structure

```
grain-guard/
├── .env.example
├── docker-compose.yml
├── README.md
├── demo/
│   └── sample_images/
│       ├── rice_sample_good.jpg
│       ├── rice_sample_broken.jpg
│       └── rice_sample_discolored.jpg
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── models/
│   │   └── README.md
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── quality_config.py
│   │   ├── database/
│   │   │   ├── session.py
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   └── inspection.py
│   │   ├── services/
│   │   │   ├── image_processor.py
│   │   │   ├── quality_engine.py
│   │   │   └── certificate_service.py
│   │   ├── ai/
│   │   │   ├── base.py
│   │   │   ├── demo_engine.py
│   │   │   └── yolo_engine.py
│   │   └── api/
│   │       ├── health.py
│   │       ├── inspections.py
│   │       └── verify.py
│   └── tests/
│       ├── test_quality_engine.py
│       └── test_api.py
└── frontend/
    ├── Dockerfile
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── components/
        │   ├── Navbar.jsx
        │   ├── EvidenceViewer.jsx
        │   ├── CameraCapture.jsx
        │   ├── QualityBadge.jsx
        │   └── DeductionBreakdown.jsx
        ├── pages/
        │   ├── Dashboard.jsx
        │   ├── NewInspection.jsx
        │   ├── InspectionResult.jsx
        │   ├── CertificateView.jsx
        │   ├── History.jsx
        │   └── PublicVerify.jsx
        ├── services/
        │   └── api.js
        └── utils/
            └── formatters.js
```

---

## 13. Data Flow

```
1. Operator inputs batch reference & selects grain type on React UI.
2. React UI triggers POST /api/inspections -> Backend generates Inspection ID.
3. Operator snaps photo -> React transmits Blob via POST /api/inspections/{id}/analyze.
4. image_processor.py receives image:
   a. Validates image resolution & aspect ratio.
   b. Computes blur index (Laplacian) & brightness histograms.
   c. If checks fail -> Returns HTTP 422 with actionable guidance ("Image too dark", "Camera blurry").
5. AI Subsystem executes:
   a. Feeds preprocessed matrix to active engine (DemoEngine or YoloEngine).
   b. Extracts list of detections [bbox, class, confidence, area].
6. OpenCV annotates original frame with color-coded bounding boxes and defect labels.
7. quality_engine.py runs:
   a. Aggregates object counts & calculates defect percentages.
   b. Computes weighted deductions:
      Score = 100 - (broken% * W1) - (discolored% * W2) - (insect% * W3) - (foreign% * W4)
   c. Assigns Grade: Excellent (90+), Good (75-89.9), Review (60-74.9), Poor (<60).
8. SQLite stores:
   a. Inspection record + Quality breakdown + Individual detections.
9. certificate_service.py generates verification token + QR Code.
10. Backend responds with full JSON payload and annotated image URL (< 2.5 seconds).
11. UI renders Interactive AI Evidence & allows immediate digital certificate generation.
```

---

## 14. Security & Data Integrity Considerations
1. **File Upload Hardening**: Maximum upload size capped at 12MB. File magic bytes inspected to ensure only `image/jpeg` and `image/png` are parsed. Filenames sanitized with UUIDs to avoid directory traversal.
2. **Path Traversal Protection**: Static storage mounts (`/uploads`, `/certificates`) serve strictly through controlled endpoints with sanitized identifiers.
3. **Audit Immutability**: Quality results and detections are tied to a unique `verification_token`. Updating completed inspection records is prohibited by API logic.
4. **Public Surface Sanitization**: `/api/verify/{token}` exposes only necessary inspection proof (grade, aggregate defect counts, timestamp, masked batch ID). Internal paths, database IDs, and server metadata are omitted.

---

## 15. Error Handling Strategy

| Error Scenario | Detection Layer | User-Facing Actionable Response |
|---|---|---|
| Image too blurry | Preprocessing (`cv2.Laplacian` variance $< 100$) | ⚠️ *"Image is blurry. Please steady your smartphone and tap to focus."* |
| Image too dark / overexposed | Preprocessing (Mean pixel intensity $< 40$ or $> 230$) | ⚠️ *"Lighting is inadequate. Ensure even lighting without harsh shadows."* |
| No grains detected | Detection Engine (Object count $= 0$) | ⚠️ *"No grains detected. Ensure sample is spread across the tray surface."* |
| Model weights missing | AI Loader | Clean fallback to Demo Mode with prominent UI banner *"Demo Inference Mode Active"*. |
| Unhandled backend exception | FastAPI Global Exception Handler | Generic HTTP 500 with friendly UI notice *"Analysis could not be completed. Please try again."* (Zero raw Python tracebacks leaked). |

---

## 16. Deployment Approach
* **Local Developer / Hackathon Judge Mode**:
  - Dual process: `uvicorn backend.app.main:app --reload --port 8000` & `npm run dev --prefix frontend` (Vite port 5173).
* **Containerized Deployment**:
  - `docker-compose up --build` spins up both services with an internal bridge network and volume mounting for sample images.

---

## 17. MVP Feature Scope
- ✅ Single-tap sample camera capture + desktop sample image file uploader.
- ✅ Pre-flight image quality validation (blur and darkness rejection).
- ✅ Object detection pipeline for 5 classes (`whole`, `broken`, `discolored`, `insect`, `foreign`).
- ✅ Dynamic fallback between trained model and deterministic demo inference.
- ✅ Explainable Quality Scoring engine with transparent configurable mathematical formulas.
- ✅ AI Evidence Explorer: Interactive bounding-box inspector on annotated images.
- ✅ Digital Certificate generator with unique verification token and local QR code generator.
- ✅ Public Verification lookup page (`/verify/:token`).
- ✅ Searchable and filterable Inspection Audit History table.

---

## 18. Features Explicitly Excluded (Out of Scope for MVP)
- ❌ Blockchain ledgers and smart contracts (unnecessary complexity; UUID tokens suffice).
- ❌ Payment gateways / automated farmer payout calculations.
- ❌ Multi-tenant OAuth / SSO integrations.
- ❌ Physical IoT hardware scale/tray integration.
- ❌ Complex microservice topologies or message queues (RabbitMQ/Kafka).

---

## 19. Recommended Technology Stack Summary
* **Frontend**: React 18, Vite 5, Tailwind CSS 3, Lucide-React, HTML5 Canvas API.
* **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn.
* **Database**: SQLite 3 with SQLAlchemy 2.0.
* **Computer Vision / AI**: OpenCV-Python (`cv2`), NumPy, Pillow, PyTorch CPU / Ultralytics YOLOv8.
* **Utilities**: `qrcode[pil]`, `python-multipart`.

---

## 20. Technical Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Varying mobile camera resolutions & lighting** | False detections / poor segmentation | Standardize input image dimensions via resizing/normalization; provide visual on-screen framing overlay. |
| **Model initialization latency on judge laptop** | App hangs or times out | Lazy-load model once at server startup; fall back automatically to instant deterministic demo inference if weights are absent. |
| **Browser camera permission restrictions on localhost** | Camera capture fails | Provide an intuitive "Upload Image File" button alongside the live camera feed. |
| **Complex bounding box rendering performance on mobile** | Laggy UI | Render bounding boxes onto canvas statically on backend, with SVG hotspot overlays on frontend for crisp, low-overhead interactions. |

---

# IMPLEMENTATION PLAN

1. **Step 1 — Project Initialization & Environment Setup**:
   Create directory layout, set up `.env.example`, configure backend Python virtual environment (`requirements.txt`), and initialize Vite React frontend with Tailwind CSS.

2. **Step 2 — Database Schema & Session Configuration**:
   Implement SQLAlchemy declarative models (`Inspection`, `Detection`, `QualityResult`, `Certificate`) in SQLite and create initial migration/table generation logic.

3. **Step 3 — Backend API Skeleton & Health Endpoints**:
   Implement FastAPI entrypoint (`main.py`), CORS middleware, global error handling, and `/api/health`.

4. **Step 4 — Image Preprocessing & Validation Service**:
   Write OpenCV helper routines in `image_processor.py` for blur detection (Laplacian variance), illumination checking, and image normalization.

5. **Step 5 — AI Interface & Inference Subsystem**:
   Build `GrainModelInterface`, implement `DeterministicDemoEngine` (deterministic hashing based on sample image characteristics), and hook up `YoloEngine` loader with fallback logic.

6. **Step 6 — Explainable Quality Engine**:
   Implement `quality_engine.py` to calculate defect percentages, apply weighted deduction formulas, assign grade categories, and construct explainability metadata.

7. **Step 7 — Certificate & QR Verification Service**:
   Create `certificate_service.py` to generate unique verification tokens, format official certificate payloads, and synthesize QR codes pointing to `/verify/{token}`.

8. **Step 8 — Analysis Pipeline Integration**:
   Complete `POST /api/inspections` and `POST /api/inspections/{id}/analyze` endpoints connecting Preprocessing $\to$ AI Inference $\to$ Quality Engine $\to$ Certificate Generation $\to$ Database persistence.

9. **Step 9 — Frontend Wizard & Camera Interface**:
   Build `NewInspection.jsx` and `CameraCapture.jsx` with real-time video stream, tray alignment overlay, quality warning toasts, and fallback sample picker.

10. **Step 10 — Frontend Results & AI Evidence Viewer**:
    Build `InspectionResult.jsx` featuring the Quality Score dial, defect percentage meters, transparent deduction explanations, and interactive canvas bounding box inspector.

11. **Step 11 — Digital Certificate & Public Verification UI**:
    Build `CertificateView.jsx` (print/export ready certificate with QR code) and `PublicVerify.jsx` (tamper-evident audit lookup page).

12. **Step 12 — Dashboard & Inspection History**:
    Implement `Dashboard.jsx` (key metrics, today's summary) and `History.jsx` with instant search, filter by grain type/grade, and direct result linking.

13. **Step 13 — Automated Tests & Sample Data**:
    Add pytest test suite covering quality calculations, API endpoints, and verification tokens; supply sample grain images in `demo/sample_images/`.

14. **Step 14 — Dockerization & Final Polish**:
    Write clean `Dockerfile`s and `docker-compose.yml`, test the complete end-to-end flow from scratch, and verify documentation in `README.md`.