from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class CertificateVerifyResponse(BaseModel):
    verified: bool
    status_message: str
    certificate_number: str
    verification_token: str
    inspection_date: datetime
    grain_type: str
    farmer_reference: Optional[str] = None
    quality_score: float
    category: str
    decision: str
    total_objects: int
    statistics: Dict[str, float]
    annotated_image_url: Optional[str] = None
    issuer: str = "GrainGuard Rural Mandi Certification Node"
