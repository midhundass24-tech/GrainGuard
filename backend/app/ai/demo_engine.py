import time
import cv2
import numpy as np
from app.ai.base import BaseGrainEngine, InferenceResult, RawDetection
from app.ai.preprocessor import ImagePreprocessor

class DemoGrainEngine(BaseGrainEngine):
    """
    Deterministic morphological computer-vision engine for demonstration mode.
    Accurately locates real grain contours on contrasting backgrounds, analyzes
    area & aspect ratio for whole vs. broken, and analyzes HSV color histograms
    to classify discolored, insect-damaged, and foreign matter objects.
    """

    def analyze_grain_image(self, image_path: str, grain_type: str = "rice") -> InferenceResult:
        start_time = time.time()
        
        # Load and validate image
        img, diagnostics = ImagePreprocessor.validate_and_preprocess(image_path)
        h, w = img.shape[:2]

        # Convert to Grayscale & Adaptive Threshold to isolate grains from tray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Otsu thresholding + Morphological opening to separate touching grains
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # If background is bright tray instead of dark, invert
        white_pixels = cv2.countNonZero(thresh)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        if white_pixels > total_pixels * 0.6:
            thresh = cv2.bitwise_not(thresh)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        # Find grain contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Collect areas of reasonable size and filter outer tray frame
        grain_candidates = []
        img_area = w * h
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, bw, bh = cv2.boundingRect(cnt)
            # Skip outer tray borders (covering > 20% of image or touching all outer edges)
            if area > img_area * 0.20 or bw > w * 0.85 or bh > h * 0.85:
                continue
            # Filter noise (<35px) and non-grain artifacts (>30000px)
            if 35 <= area <= 30000:
                grain_candidates.append((cnt, area))

        if not grain_candidates:
            # Fallback synthetic grid if sample image is plain or edge-case
            return self._generate_synthetic_fallback(w, h, grain_type, start_time)

        # Compute median area to distinguish whole vs broken grains
        areas = [a for _, a in grain_candidates]
        median_area = np.median(areas) if len(areas) > 0 else 500.0

        for idx, (cnt, area) in enumerate(grain_candidates):
            x, y, bw, bh = cv2.boundingRect(cnt)
            x1, y1, x2, y2 = x, y, x + bw, y + bh

            # Extract ROI for color and defect inspection
            roi_hsv = hsv[y1:y2, x1:x2]
            if roi_hsv.size == 0:
                continue

            mean_sat = np.mean(roi_hsv[:, :, 1])
            mean_val = np.mean(roi_hsv[:, :, 2])
            mean_hue = np.mean(roi_hsv[:, :, 0])

            # Deterministic grain classification logic:
            aspect_ratio = max(bw, bh) / (min(bw, bh) + 1e-5)

            # 1. Foreign Matter: purple artifacts or extreme size (e.g. stone/chaff)
            if (mean_hue > 130 and mean_sat > 110) or area > median_area * 3.5:
                class_name = "foreign_matter"
                confidence = float(np.clip(0.91 + (idx % 8) * 0.01, 0.85, 0.98))
            # 2. Insect Damaged: dark boreholes or distinct dark-red specks
            elif (mean_hue < 10 and mean_sat > 140) or (mean_val < 45 and area > median_area * 0.4):
                class_name = "insect_damaged"
                confidence = float(np.clip(0.89 + (idx % 7) * 0.01, 0.84, 0.97))
            # 3. Discolored Grain: amber / deep yellow deviation
            elif (15 <= mean_hue <= 35 and mean_sat > 115):
                class_name = "discolored_grain"
                confidence = float(np.clip(0.90 + (idx % 9) * 0.01, 0.86, 0.98))
            # 4. Broken Grain: area significantly smaller than median or rounded aspect ratio
            elif area < median_area * 0.45 or aspect_ratio < 1.10:
                class_name = "broken_grain"
                confidence = float(np.clip(0.92 + (idx % 6) * 0.01, 0.88, 0.99))
            # 5. Whole Grain
            else:
                class_name = "whole_grain"
                confidence = float(np.clip(0.94 + (idx % 5) * 0.01, 0.90, 0.99))

            detections.append(
                RawDetection(
                    class_name=class_name,
                    confidence=round(confidence, 3),
                    bbox=[int(x1), int(y1), int(x2), int(y2)],
                    area=round(float(area), 2)
                )
            )

        elapsed_ms = int((time.time() - start_time) * 1000)
        return InferenceResult(
            detections=detections,
            model_version="demo-morphological-cv-v1",
            is_mock=True,
            inference_time_ms=elapsed_ms,
            metadata={
                "total_contours": len(contours),
                "processed_grains": len(detections),
                "median_area": float(median_area)
            }
        )

    def _generate_synthetic_fallback(self, w: int, h: int, grain_type: str, start_time: float) -> InferenceResult:
        """Fallback to guarantee deterministic demonstration results if an empty test image is provided."""
        detections = []
        rows, cols = 8, 12
        step_x, step_y = w // (cols + 2), h // (rows + 2)

        idx = 0
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                idx += 1
                cx = c * step_x + (idx % 7)
                cy = r * step_y + (idx % 5)
                bw, bh = 24 + (idx % 6), 55 + (idx % 10)
                
                # Distribution: ~85% whole, ~8% broken, ~3% discolored, ~2% insect, ~2% foreign
                if idx % 29 == 0:
                    cls = "foreign_matter"
                    conf = 0.91
                elif idx % 23 == 0:
                    cls = "insect_damaged"
                    conf = 0.89
                elif idx % 17 == 0:
                    cls = "discolored_grain"
                    conf = 0.93
                elif idx % 7 == 0:
                    cls = "broken_grain"
                    conf = 0.95
                    bh = int(bh * 0.5)
                else:
                    cls = "whole_grain"
                    conf = 0.97

                detections.append(
                    RawDetection(
                        class_name=cls,
                        confidence=conf,
                        bbox=[cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2],
                        area=float(bw * bh)
                    )
                )

        elapsed_ms = int((time.time() - start_time) * 1000)
        return InferenceResult(
            detections=detections,
            model_version="demo-synthetic-grid-v1",
            is_mock=True,
            inference_time_ms=elapsed_ms,
            metadata={"synthetic": True}
        )
