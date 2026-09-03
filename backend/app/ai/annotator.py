import cv2
import numpy as np
from typing import List
from app.ai.base import RawDetection

# Color palette (BGR format for OpenCV)
CLASS_COLORS = {
    "whole_grain": (46, 204, 113),      # Emerald Green
    "broken_grain": (52, 152, 219),     # Blue
    "discolored_grain": (41, 128, 185), # Amber / Orange
    "insect_damaged": (0, 0, 220),       # Bright Red
    "foreign_matter": (155, 89, 182)    # Purple
}

class ImageAnnotator:
    @staticmethod
    def annotate(image_path: str, detections: List[RawDetection], output_path: str) -> str:
        """
        Draws high-contrast bounding boxes, classification badges, and confidence tags on the image.
        """
        img = cv2.imread(image_path)
        if img is None:
            return image_path

        h, w = img.shape[:2]
        thickness = max(2, int(min(w, h) / 400))
        font_scale = max(0.45, min(w, h) / 1400)

        for det in detections:
            x1, y1, x2, y2 = det.bbox
            color = CLASS_COLORS.get(det.class_name, (200, 200, 200))

            # Bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

            # Label banner
            short_name = det.class_name.replace("_grain", "").replace("_damaged", " dmg").upper()
            label = f"{short_name} {int(det.confidence * 100)}%"

            (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)
            
            # Put label on top if space allows, otherwise inside
            label_y1 = max(0, y1 - text_h - 6)
            label_y2 = y1
            if y1 - text_h - 6 < 0:
                label_y1 = y1
                label_y2 = y1 + text_h + 6

            cv2.rectangle(img, (x1, label_y1), (x1 + text_w + 6, label_y2), color, -1)
            cv2.putText(
                img,
                label,
                (x1 + 3, label_y2 - 3),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        return output_path
