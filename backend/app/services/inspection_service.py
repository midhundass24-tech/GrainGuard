import uuid
import secrets
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
import cv2
import qrcode
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.models import Inspection, Detection, QualityResult, Certificate, User
from app.ai.base import BaseGrainEngine
from app.ai.demo_engine import DemoGrainEngine
from app.ai.model_engine import ModelGrainEngine
from app.ai.gemini_engine import GeminiGrainEngine
from app.ai.annotator import ImageAnnotator
from app.ai.preprocessor import ImagePreprocessor
from app.services.quality_engine import QualityEngine

class InspectionService:
    def __init__(self, db: Session):
        self.db = db
        if settings.AI_MODE == "gemini" or (settings.AI_MODE == "auto" and settings.GEMINI_API_KEYS):
            self.ai_engine: BaseGrainEngine = GeminiGrainEngine()
        elif settings.AI_MODE == "model":
            self.ai_engine = ModelGrainEngine()
        else:
            self.ai_engine = DemoGrainEngine()

    def create_inspection(self, grain_type: str, farmer_reference: Optional[str] = None) -> Inspection:
        user = self.db.query(User).first()
        if not user:
            user = User(name="Lead Mandi Inspector", role="procurement_agent")
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        inspection_id = str(uuid.uuid4())
        inspection = Inspection(
            inspection_id=inspection_id,
            user_id=user.id,
            grain_type=grain_type.lower(),
            farmer_reference=farmer_reference.strip() if farmer_reference else None,
            status="PENDING",
            ai_mode=settings.AI_MODE
        )
        self.db.add(inspection)
        self.db.commit()
        self.db.refresh(inspection)
        return inspection

    def process_and_analyze(self, inspection_id: str, image_bytes: bytes, filename: str) -> Inspection:
        start_time = time.time()
        inspection = self.db.query(Inspection).filter(Inspection.inspection_id == inspection_id).first()
        if not inspection:
            raise ValueError(f"Inspection with ID '{inspection_id}' was not found.")

        # 1. Decode & Pre-flight Validate Image (Raises ImageQualityError if invalid)
        decoded_img, diagnostics = ImagePreprocessor.decode_and_validate(image_bytes)

        # 2. Save Raw Normalized Image
        raw_filename = f"{inspection.inspection_id}_raw.jpg"
        raw_file_path = settings.UPLOAD_RAW_DIR / raw_filename
        cv2.imwrite(str(raw_file_path), decoded_img, [cv2.IMWRITE_JPEG_QUALITY, 92])
        inspection.image_path = str(raw_file_path)

        # 3. Execute AI / Computer Vision Engine
        inference_result = self.ai_engine.analyze_grain_image(str(raw_file_path), inspection.grain_type)
        
        if len(inference_result.detections) < settings.MIN_DETECTED_OBJECTS:
            inspection.status = "FAILED"
            self.db.commit()
            raise ValueError(
                f"Insufficient grains detected ({len(inference_result.detections)} < {settings.MIN_DETECTED_OBJECTS} minimum). "
                "Ensure sample is spread evenly across the contrasting tray surface."
            )

        # 4. Calculate Quality Metrics
        quality_metrics = QualityEngine.calculate_metrics(inference_result.detections, inspection.grain_type)

        # 5. Generate Annotated Image
        annotated_filename = f"{inspection.inspection_id}_annotated.jpg"
        annotated_file_path = settings.UPLOAD_ANNOTATED_DIR / annotated_filename
        ImageAnnotator.annotate(str(raw_file_path), inference_result.detections, str(annotated_file_path))

        # 6. Save Detections
        self.db.query(Detection).filter(Detection.inspection_id == inspection.id).delete()
        for det in inference_result.detections:
            d_row = Detection(
                inspection_id=inspection.id,
                class_name=det.class_name,
                confidence=det.confidence,
                x1=float(det.bbox[0]),
                y1=float(det.bbox[1]),
                x2=float(det.bbox[2]),
                y2=float(det.bbox[3]),
                area=det.area
            )
            self.db.add(d_row)

        # 7. Save Quality Result
        existing_qr = self.db.query(QualityResult).filter(QualityResult.inspection_id == inspection.id).first()
        if existing_qr:
            self.db.delete(existing_qr)

        qr_row = QualityResult(
            inspection_id=inspection.id,
            whole_percentage=quality_metrics["whole_percentage"],
            broken_percentage=quality_metrics["broken_percentage"],
            discolored_percentage=quality_metrics["discolored_percentage"],
            insect_damage_percentage=quality_metrics["insect_damage_percentage"],
            foreign_matter_percentage=quality_metrics["foreign_matter_percentage"],
            quality_score=quality_metrics["quality_score"],
            category=quality_metrics["category"],
            decision=quality_metrics["decision"],
            penalty_details=json.dumps(quality_metrics["penalties"])
        )
        self.db.add(qr_row)

        # 8. Generate Certificate & QR Code
        verification_token = secrets.token_hex(16)
        cert_number = f"GG-{time.strftime('%Y%m%d')}-{inspection.id:05d}"
        qr_filename = f"{verification_token}.png"
        qr_file_path = settings.CERTIFICATE_DIR / qr_filename

        verify_url = f"/verify/{verification_token}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr.add_data(verify_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(str(qr_file_path))

        existing_cert = self.db.query(Certificate).filter(Certificate.inspection_id == inspection.id).first()
        if existing_cert:
            self.db.delete(existing_cert)

        cert_row = Certificate(
            inspection_id=inspection.id,
            certificate_number=cert_number,
            verification_token=verification_token,
            qr_code_path=str(qr_file_path)
        )
        self.db.add(cert_row)

        # 9. Update Inspection State
        elapsed_ms = int((time.time() - start_time) * 1000)
        inspection.status = "COMPLETED"
        inspection.annotated_image_path = str(annotated_file_path)
        inspection.total_objects = len(inference_result.detections)
        inspection.quality_score = quality_metrics["quality_score"]
        inspection.processing_time_ms = elapsed_ms
        inspection.ai_mode = "demo" if inference_result.is_mock else "model"

        self.db.commit()
        self.db.refresh(inspection)
        return inspection
