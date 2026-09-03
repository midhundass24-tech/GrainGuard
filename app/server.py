import os
import uuid
import secrets
import json
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import qrcode
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import init_db, get_db, Inspection, Detection, QualityResult, Certificate
from app.engine import GrainAnalysisEngine
from app.gemini_engine import analyze_with_gemini, map_gemini_counts_to_contours

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
STATIC_DIR = APP_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
CERT_DIR = STATIC_DIR / "certificates"
TEMPLATES_DIR = APP_DIR / "templates"
SAMPLE_DIR = PROJECT_ROOT / "demo" / "sample_images"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CERT_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

# Initialize database
init_db()

app = FastAPI(title="GrainGuard Live Camera System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = TEMPLATES_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return "<h1>GrainGuard Live App — index.html not found</h1>"

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "GrainGuard Live Mandi Terminal",
        "version": "1.0.0",
        "ai_provider": "Google Gemini Vision API",
        "models": ["gemini-3.6-flash", "gemini-3.7-flash"]
    }

@app.get("/api/samples")
def list_samples():
    samples = []
    if SAMPLE_DIR.exists():
        for f in SAMPLE_DIR.glob("*.jpg"):
            samples.append({
                "filename": f.name,
                "url": f"/api/samples/{f.name}"
            })
    return {"samples": samples}

@app.get("/api/samples/{sample_name}")
def get_sample_image(sample_name: str):
    file_path = SAMPLE_DIR / sample_name
    if not file_path.exists():
        # Auto-generate if missing
        try:
            gen_script = PROJECT_ROOT / "demo" / "generate_samples.py"
            if gen_script.exists():
                import subprocess, sys
                subprocess.run([sys.executable, str(gen_script)], check=False)
        except Exception:
            pass
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Sample image not found")
    return FileResponse(file_path, media_type="image/jpeg")

@app.post("/api/analyze")
async def analyze_captured_sample(
    file: UploadFile = File(...),
    grain_type: str = Form("rice"),
    farmer_reference: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="No image received from camera.")

    try:
        # 1. Decode & Pre-flight Validate Image (sharpness & illumination)
        img, diagnostics = GrainAnalysisEngine.decode_and_validate(contents)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))

    # 2. Save Raw Normalized Image
    insp_uuid = str(uuid.uuid4())
    raw_path = UPLOAD_DIR / f"{insp_uuid}_raw.jpg"
    cv2.imwrite(str(raw_path), img, [cv2.IMWRITE_JPEG_QUALITY, 92])

    # 3. AI Execution: Strictly use Gemini Vision API with configured keys
    ai_mode_used = "gemini"
    ai_notes = ""
    detections = []
    
    try:
        gemini_result = analyze_with_gemini(contents)
        if gemini_result is not None:
            ai_mode_used = f"gemini ({gemini_result.get('ai_model', 'gemini-3.6-flash')})"
            ai_notes = gemini_result.get("notes", "")
            # Spatial mapping to real image contours
            contours_info, _ = GrainAnalysisEngine.extract_contours_info(img)
            detections = map_gemini_counts_to_contours(gemini_result, contours_info)
        else:
            # Fallback only if all Gemini keys temporarily exhausted
            ai_mode_used = "cv_fallback"
            detections = GrainAnalysisEngine.analyze(img, grain_type)
    except Exception as e:
        print(f"[Analyze] Error in AI pipeline: {e}, falling back to CV...")
        ai_mode_used = "cv_fallback"
        detections = GrainAnalysisEngine.analyze(img, grain_type)

    # 4. Compute Quality Scores & Deductions
    quality_metrics = GrainAnalysisEngine.compute_quality(detections, grain_type)

    # 5. Generate High-Contrast Bounding Box Annotated Image
    annotated_img = GrainAnalysisEngine.annotate(img, detections)
    ann_path = UPLOAD_DIR / f"{insp_uuid}_annotated.jpg"
    cv2.imwrite(str(ann_path), annotated_img, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # 6. Generate Verifiable Certificate & QR Code
    verification_token = secrets.token_hex(16)
    cert_number = f"GG-{time.strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"
    qr_filename = f"{verification_token}.png"
    qr_path = CERT_DIR / qr_filename

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(f"/verify/{verification_token}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(str(qr_path))

    # 7. Persist to Database
    elapsed_ms = int((time.time() - start_time) * 1000)
    insp_row = Inspection(
        inspection_id=insp_uuid,
        grain_type=grain_type.lower(),
        farmer_reference=farmer_reference.strip() if farmer_reference else "Unassigned Batch",
        image_path=f"/static/uploads/{insp_uuid}_raw.jpg",
        annotated_image_path=f"/static/uploads/{insp_uuid}_annotated.jpg",
        total_objects=len(detections),
        quality_score=quality_metrics["score"],
        status="COMPLETED",
        processing_time_ms=elapsed_ms
    )
    db.add(insp_row)
    db.flush()

    # Add detections
    for d in detections:
        d_row = Detection(
            inspection_id=insp_row.id,
            class_name=d.class_name,
            confidence=d.confidence,
            x1=float(d.bbox[0]),
            y1=float(d.bbox[1]),
            x2=float(d.bbox[2]),
            y2=float(d.bbox[3]),
            area=d.area
        )
        db.add(d_row)

    # Add quality results
    qr_row = QualityResult(
        inspection_id=insp_row.id,
        whole_percentage=quality_metrics["whole_pct"],
        broken_percentage=quality_metrics["broken_pct"],
        discolored_percentage=quality_metrics["discolor_pct"],
        insect_damage_percentage=quality_metrics["insect_pct"],
        foreign_matter_percentage=quality_metrics["foreign_pct"],
        quality_score=quality_metrics["score"],
        category=quality_metrics["category"],
        decision=quality_metrics["decision"],
        penalty_details=json.dumps(quality_metrics["penalties"])
    )
    db.add(qr_row)

    # Add certificate
    cert_row = Certificate(
        inspection_id=insp_row.id,
        certificate_number=cert_number,
        verification_token=verification_token,
        qr_code_path=f"/static/certificates/{qr_filename}"
    )
    db.add(cert_row)
    db.commit()

    return {
        "inspection_id": insp_uuid,
        "status": "COMPLETED",
        "grain_type": grain_type,
        "farmer_reference": insp_row.farmer_reference,
        "ai_engine_used": ai_mode_used,
        "ai_notes": ai_notes,
        "image_url": f"/static/uploads/{insp_uuid}_raw.jpg",
        "annotated_image_url": f"/static/uploads/{insp_uuid}_annotated.jpg",
        "total_objects": len(detections),
        "quality_score": quality_metrics["score"],
        "processing_time_ms": elapsed_ms,
        "quality_result": quality_metrics,
        "certificate": {
            "certificate_number": cert_number,
            "verification_token": verification_token,
            "qr_code_url": f"/static/certificates/{qr_filename}",
            "verification_url": f"/verify/{verification_token}"
        },
        "detections": [
            {
                "id": idx + 1,
                "class_name": d.class_name,
                "confidence": d.confidence,
                "bbox": d.bbox,
                "area": d.area
            }
            for idx, d in enumerate(detections)
        ]
    }

@app.get("/api/inspections")
def list_inspections(db: Session = Depends(get_db)):
    items = db.query(Inspection).order_by(Inspection.created_at.desc()).limit(50).all()
    results = []
    for i in items:
        qr = i.quality_result
        cert = i.certificate
        results.append({
            "inspection_id": i.inspection_id,
            "grain_type": i.grain_type,
            "farmer_reference": i.farmer_reference,
            "quality_score": i.quality_score,
            "total_objects": i.total_objects,
            "created_at": i.created_at.strftime("%Y-%m-%d %H:%M"),
            "category": qr.category if qr else "Unknown",
            "decision": qr.decision if qr else "UNKNOWN",
            "certificate_number": cert.certificate_number if cert else "N/A"
        })
    return {"items": results}

@app.get("/api/verify/{token}")
def verify_certificate(token: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.verification_token == token).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Invalid certificate token.")

    insp = cert.inspection
    qr = insp.quality_result

    return {
        "verified": True,
        "certificate_number": cert.certificate_number,
        "verification_token": cert.verification_token,
        "inspection_date": cert.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "grain_type": insp.grain_type,
        "farmer_reference": insp.farmer_reference,
        "quality_score": insp.quality_score,
        "category": qr.category if qr else "Unknown",
        "decision": qr.decision if qr else "UNKNOWN",
        "total_objects": insp.total_objects,
        "whole_percentage": qr.whole_percentage if qr else 0.0,
        "broken_percentage": qr.broken_percentage if qr else 0.0,
        "discolored_percentage": qr.discolored_percentage if qr else 0.0,
        "insect_damage_percentage": qr.insect_damage_percentage if qr else 0.0,
        "foreign_matter_percentage": qr.foreign_matter_percentage if qr else 0.0,
        "annotated_image_url": insp.annotated_image_path
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
