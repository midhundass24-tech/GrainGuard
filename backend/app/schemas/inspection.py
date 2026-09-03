from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class DetectionSchema(BaseModel):
    id: Optional[int] = None
    class_name: str
    confidence: float
    bbox: List[float] = Field(description="[x1, y1, x2, y2]")
    area: float

    class Config:
        from_attributes = True

class QualityResultSchema(BaseModel):
    whole_percentage: float
    broken_percentage: float
    discolored_percentage: float
    insect_damage_percentage: float
    foreign_matter_percentage: float
    quality_score: float
    category: str
    decision: str
    penalties: Optional[Dict[str, float]] = None

    class Config:
        from_attributes = True

class CertificateSummarySchema(BaseModel):
    certificate_number: str
    verification_token: str
    verification_url: str
    qr_code_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class InspectionCreate(BaseModel):
    grain_type: str = Field(default="rice", description="Grain type: rice, wheat, pulses")
    farmer_reference: Optional[str] = Field(default=None, description="Optional batch or farmer ID")

class InspectionResponse(BaseModel):
    inspection_id: str
    status: str
    grain_type: str
    farmer_reference: Optional[str] = None
    image_url: Optional[str] = None
    annotated_image_url: Optional[str] = None
    total_objects: int = 0
    quality_score: float = 0.0
    processing_time_ms: int = 0
    ai_mode: str
    created_at: datetime
    quality_result: Optional[QualityResultSchema] = None
    detections: Optional[List[DetectionSchema]] = []
    certificate: Optional[CertificateSummarySchema] = None

    class Config:
        from_attributes = True

class InspectionListResponse(BaseModel):
    total: int
    items: List[InspectionResponse]
