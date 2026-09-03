import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Inspection, QualityResult
from app.schemas.inspection import (
    InspectionCreate,
    InspectionResponse,
    InspectionListResponse,
    DetectionSchema,
    QualityResultSchema,
    CertificateSummarySchema
)
from app.services.inspection_service import InspectionService
from app.ai.preprocessor import ImageQualityError

router = APIRouter(prefix="/inspections")

def _build_inspection_response(insp: Inspection) -> InspectionResponse:
    raw_url = f"/static/uploads/raw/{insp.inspection_id}_raw.jpg" if insp.image_path else None
    ann_url = f"/static/uploads/annotated/{insp.inspection_id}_annotated.jpg" if insp.annotated_image_path else None

    qr_schema = None
    if insp.quality_result:
        qr = insp.quality_result
        penalties = None
        if qr.penalty_details:
            try:
                penalties = json.loads(qr.penalty_details)
            except Exception:
                penalties = None

        qr_schema = QualityResultSchema(
            whole_percentage=qr.whole_percentage,
            broken_percentage=qr.broken_percentage,
            discolored_percentage=qr.discolored_percentage,
            insect_damage_percentage=qr.insect_damage_percentage,
            foreign_matter_percentage=qr.foreign_matter_percentage,
            quality_score=qr.quality_score,
            category=qr.category,
            decision=qr.decision,
            penalties=penalties
        )

    det_schemas = [
        DetectionSchema(
            id=d.id,
            class_name=d.class_name,
            confidence=d.confidence,
            bbox=[d.x1, d.y1, d.x2, d.y2],
            area=d.area
        )
        for d in (insp.detections or [])
    ]

    cert_schema = None
    if insp.certificate:
        cert_schema = CertificateSummarySchema(
            certificate_number=insp.certificate.certificate_number,
            verification_token=insp.certificate.verification_token,
            verification_url=f"/verify/{insp.certificate.verification_token}",
            qr_code_url=f"/static/certificates/{insp.certificate.verification_token}.png",
            created_at=insp.certificate.created_at
        )

    return InspectionResponse(
        inspection_id=insp.inspection_id,
        status=insp.status,
        grain_type=insp.grain_type,
        farmer_reference=insp.farmer_reference,
        image_url=raw_url,
        annotated_image_url=ann_url,
        total_objects=insp.total_objects or 0,
        quality_score=insp.quality_score or 0.0,
        processing_time_ms=insp.processing_time_ms or 0,
        ai_mode=insp.ai_mode or "demo",
        created_at=insp.created_at,
        quality_result=qr_schema,
        detections=det_schemas,
        certificate=cert_schema
    )

@router.post("", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(payload: InspectionCreate, db: Session = Depends(get_db)):
    service = InspectionService(db)
    insp = service.create_inspection(
        grain_type=payload.grain_type,
        farmer_reference=payload.farmer_reference
    )
    return _build_inspection_response(insp)

@router.post("/{inspection_id}/analyze", response_model=InspectionResponse)
async def analyze_inspection_image(
    inspection_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    if len(contents) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the maximum allowed limit of 15MB."
        )

    service = InspectionService(db)
    try:
        insp = service.process_and_analyze(
            inspection_id=inspection_id,
            image_bytes=contents,
            filename=file.filename or "upload.jpg"
        )
        return _build_inspection_response(insp)
    except ImageQualityError as iqe:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=iqe.message
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis engine failure: {str(e)}"
        )

@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(inspection_id: str, db: Session = Depends(get_db)):
    insp = db.query(Inspection).filter(Inspection.inspection_id == inspection_id).first()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection record not found")
    return _build_inspection_response(insp)

@router.get("", response_model=InspectionListResponse)
def list_inspections(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    grain_type: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Inspection)

    if grain_type:
        query = query.filter(Inspection.grain_type == grain_type.lower())

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Inspection.farmer_reference.ilike(search_pattern)) |
            (Inspection.inspection_id.ilike(search_pattern))
        )

    if category:
        query = query.join(QualityResult).filter(QualityResult.category == category)

    total = query.count()
    items = query.order_by(Inspection.created_at.desc()).offset(skip).limit(limit).all()

    return InspectionListResponse(
        total=total,
        items=[_build_inspection_response(i) for i in items]
    )

@router.get("/{inspection_id}/certificate")
def get_certificate(inspection_id: str, db: Session = Depends(get_db)):
    insp = db.query(Inspection).filter(Inspection.inspection_id == inspection_id).first()
    if not insp or not insp.certificate:
        raise HTTPException(status_code=404, detail="Certificate not found for this inspection")

    cert = insp.certificate
    qr = insp.quality_result

    return {
        "certificate_number": cert.certificate_number,
        "verification_token": cert.verification_token,
        "verification_url": f"/verify/{cert.verification_token}",
        "qr_code_url": f"/static/certificates/{cert.verification_token}.png",
        "created_at": cert.created_at,
        "grain_type": insp.grain_type,
        "farmer_reference": insp.farmer_reference,
        "quality_score": insp.quality_score,
        "category": qr.category if qr else "Unknown",
        "decision": qr.decision if qr else "Unknown"
    }
