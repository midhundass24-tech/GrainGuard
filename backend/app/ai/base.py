from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class RawDetection(BaseModel):
    class_name: str
    confidence: float
    bbox: List[int]  # [x1, y1, x2, y2]
    area: float

class InferenceResult(BaseModel):
    detections: List[RawDetection]
    model_version: str
    is_mock: bool
    inference_time_ms: int
    metadata: Dict[str, Any] = {}

class BaseGrainEngine(ABC):
    @abstractmethod
    def analyze_grain_image(self, image_path: str, grain_type: str = "rice") -> InferenceResult:
        """
        Standardized AI inference interface.
        Accepts image path and grain type, returns detected objects and bounding boxes.
        """
        pass
