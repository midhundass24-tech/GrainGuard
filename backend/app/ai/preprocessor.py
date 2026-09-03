import cv2
import numpy as np
from typing import Tuple, Dict, Any
from app.core.config import settings

class ImageQualityError(Exception):
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

class ImagePreprocessor:
    @staticmethod
    def decode_and_validate(
        image_bytes: bytes,
        min_blur: float = settings.MIN_BLUR_LAPLACIAN,
        min_luminance: float = settings.MIN_LUMINANCE,
        max_luminance: float = settings.MAX_LUMINANCE
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Decodes in-memory image bytes and validates clarity and illumination.
        Returns the BGR numpy image matrix and diagnostic metrics.
        """
        if not image_bytes:
            raise ImageQualityError("Uploaded image file is empty.")

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None or img.size == 0:
            raise ImageQualityError("Unable to decode image. Please ensure a valid JPEG or PNG file is uploaded.")

        # Standardize max working resolution for consistent inference
        height, width = img.shape[:2]
        max_dimension = 1600
        if max(height, width) > max_dimension:
            scale = max_dimension / float(max(height, width))
            img = cv2.resize(img, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)

        # Check blur via Laplacian variance
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        # Check illumination via mean luminance
        mean_luminance = float(np.mean(gray))

        diagnostics = {
            "width": int(img.shape[1]),
            "height": int(img.shape[0]),
            "blur_score": round(laplacian_var, 2),
            "luminance": round(mean_luminance, 2)
        }

        if laplacian_var < min_blur:
            raise ImageQualityError(
                f"Image is too blurry (Sharpness: {laplacian_var:.1f} < threshold {min_blur}). Please steady the camera and tap to focus.",
                diagnostics
            )

        if mean_luminance < min_luminance:
            raise ImageQualityError(
                f"Image is too dark (Luminance: {mean_luminance:.1f} < threshold {min_luminance}). Ensure adequate lighting on the sample tray.",
                diagnostics
            )

        if mean_luminance > max_luminance:
            raise ImageQualityError(
                f"Image is overexposed (Luminance: {mean_luminance:.1f} > threshold {max_luminance}). Reduce harsh reflections or direct glare.",
                diagnostics
            )

        return img, diagnostics

    @staticmethod
    def validate_and_preprocess(
        image_path: str,
        min_blur: float = settings.MIN_BLUR_LAPLACIAN,
        min_luminance: float = settings.MIN_LUMINANCE,
        max_luminance: float = settings.MAX_LUMINANCE
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        with open(image_path, "rb") as f:
            data = f.read()
        return ImagePreprocessor.decode_and_validate(data, min_blur, min_luminance, max_luminance)
