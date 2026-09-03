# GrainGuard — AI Smartphone Grain Quality Inspection & Digital Certification

> **SEE $\rightarrow$ MEASURE $\rightarrow$ VERIFY**  
> An explainable, smartphone-based visual grain inspection and tamper-evident digital certification MVP for rural procurement centers.

---

## 1. Problem & Product Concept
Traditional visible grain quality assessment at rural aggregation gates relies on subjective visual checks, leading to grading disputes and lack of audit trails. 

**GrainGuard** turns any smartphone camera into an objective intake terminal:
- **SEE**: The operator snaps a top-down photo of a grain sample placed on a standardized contrasting tray.
- **MEASURE**: Computer vision detects, segments, and classifies individual kernels into 5 visual classes: Whole, Broken, Discolored, Insect-damaged, and Foreign Matter.
- **VERIFY**: The system computes a transparent score deduction, generates color-coded AI evidence bounding boxes, and issues a tamper-evident digital certificate with a verifiable QR code.

*Disclaimer*: This system is designed strictly for **visible physical grain quality characteristics** and does not replace laboratory NIR chemical testing (such as moisture or protein content). Quality deduction thresholds are configurable demonstration values.

---

## 2. Technology Stack
- **Frontend**: React 18, Vite 5, Tailwind CSS, Lucide Icons, QR Code SVG, HTML5 MediaDevices API.
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy 2.0, SQLite (WAL mode), Pydantic v2, Uvicorn.
- **Computer Vision & AI**: OpenCV, NumPy, Pillow, with pluggable support for PyTorch/ONNX models and a morphological CV fallback engine.

---

## 3. Quick Start (1-Click Run)

### Option A: Master 1-Click Launch
```bash
py run_app.py
```
This automatically verifies dependencies, generates sample datasets, opens the interactive browser dashboard, and starts the FastAPI server at `http://127.0.0.1:8000`.

### Option B: Local Dual-Terminal Run
**Terminal 1 (Backend API):**
```bash
cd backend
py -m pip install -r requirements.txt
pytest
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*API Documentation:* `http://127.0.0.1:8000/docs`

**Terminal 2 (Frontend React App):**
```bash
cd frontend
npm install
npm run dev
```
*Web App:* `http://localhost:5173`

---

## 4. Docker Deployment
```bash
docker compose up --build
```
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000/docs`

---

## 5. Live Hackathon Demo Walkthrough for Judges
1. Open `standalone_app.html` or `http://localhost:5173`.
2. Select **Rice / Paddy** and click **Generate Good Sample** (or **Broken/Defective Sample**).
3. Click **Run AI Quality Analysis**.
4. Observe the **Quality Score Gauge (0-100)** and **5-class Defect Breakdown** with transparent score deductions.
5. Click **Generate Certificate** to view the tamper-evident certificate with verified QR code.
