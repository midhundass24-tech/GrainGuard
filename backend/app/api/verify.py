from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Certificate, Inspection, QualityResult
from app.schemas.certificate import CertificateVerifyResponse

router = APIRouter()

@router.get("/verify/{verification_token}", response_model=CertificateVerifyResponse)
def verify_certificate(verification_token: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.verification_token == verification_token).first()
    if not cert:
        raise HTTPException(
            status_code=404,
            detail="Invalid certificate token. This inspection certificate does not exist or has been revoked."
        )

    inspection = cert.inspection
    qr = inspection.quality_result

    stats = {
        "whole_percentage": qr.whole_percentage if qr else 0.0,
        "broken_percentage": qr.broken_percentage if qr else 0.0,
        "discolored_percentage": qr.discolored_percentage if qr else 0.0,
        "insect_damage_percentage": qr.insect_damage_percentage if qr else 0.0,
        "foreign_matter_percentage": qr.foreign_matter_percentage if qr else 0.0,
    }

    ann_url = f"/static/uploads/annotated/{inspection.inspection_id}_annotated.jpg" if inspection.annotated_image_path else None

    return CertificateVerifyResponse(
        verified=True,
        status_message="OFFICIALLY VERIFIED INSPECTION CERTIFICATE",
        certificate_number=cert.certificate_number,
        verification_token=cert.verification_token,
        inspection_date=cert.created_at,
        grain_type=inspection.grain_type,
        farmer_reference=inspection.farmer_reference,
        quality_score=inspection.quality_score,
        category=qr.category if qr else "Unknown",
        decision=qr.decision if qr else "UNKNOWN",
        total_objects=inspection.total_objects,
        statistics=stats,
        annotated_image_url=ann_url
    )
