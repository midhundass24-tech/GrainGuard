# GrainGuard Live Camera Application

An edge-ready, real-time smartphone and webcam grain quality inspection terminal.

---

## 🚀 Quick Start (1-Click Run)

### Option 1: Double-Click
Double-click `run.bat` inside this folder.

### Option 2: Command Line
From project root:
```bash
py app/run.py
```
Or with uvicorn:
```bash
py -m uvicorn app.server:app --reload --host 127.0.0.1 --port 8000
```

Then open your browser at **`http://127.0.0.1:8000/`**.

---

## 📱 Live Features
1. **Real-time Camera Stream**: Uses your device's webcam or mobile rear camera with top-down alignment guides.
2. **Instant Capture & Analyze**: Snaps the live video frame and runs the optical defect segmentation pipeline in $< 400\text{ ms}$.
3. **Interactive AI Evidence Viewer**: Toggle between raw photo and AI-annotated frame with color-coded bounding boxes.
4. **Transparent Scoring Engine**: Shows exact mathematical deductions per visual defect class.
5. **Digital Certificate & QR Code**: Generates tamper-evident certificates with verifiable QR codes.
6. **Audit History**: All inspections are saved in local SQLite (`grainguard_live.db`).
