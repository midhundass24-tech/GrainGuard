"""
Utility script to generate high-contrast demo tray sample images in demo/sample_images/
"""
import os
from pathlib import Path
import cv2
import numpy as np

SAMPLE_DIR = Path(__file__).resolve().parent / "sample_images"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

def create_demo_tray(filename: str, broken_ratio=0.08, discolored_ratio=0.04, insect_ratio=0.02, foreign_ratio=0.02):
    # 1000x1000 dark contrasting tray
    img = np.full((1000, 1000, 3), (30, 41, 59), dtype=np.uint8)
    # Physical tray border
    cv2.rectangle(img, (40, 40), (960, 960), (71, 85, 105), 14)

    rows, cols = 12, 14
    idx = 0
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            idx += 1
            cx = c * 62 + int(np.sin(r * c) * 10)
            cy = r * 68 + int(np.cos(r + c) * 10)
            angle = (r * 37 + c * 19) % 180

            # Assign defect based on ratios
            if foreign_ratio > 0 and idx % max(1, int(1 / foreign_ratio)) == 0:
                # Foreign stone / purple artifact
                cv2.circle(img, (cx, cy), 10, (182, 89, 155), -1)
            elif insect_ratio > 0 and idx % max(1, int(1 / insect_ratio)) == 0:
                # Insect damaged (dark specked red)
                cv2.ellipse(img, (cx, cy), (16, 7), angle, 0, 360, (0, 0, 220), -1)
                cv2.circle(img, (cx, cy), 3, (15, 15, 15), -1)
            elif discolored_ratio > 0 and idx % max(1, int(1 / discolored_ratio)) == 0:
                # Discolored / yellowed grain
                cv2.ellipse(img, (cx, cy), (18, 7), angle, 0, 360, (41, 128, 185), -1)
            elif broken_ratio > 0 and idx % max(1, int(1 / broken_ratio)) == 0:
                # Broken grain half
                cv2.ellipse(img, (cx, cy), (9, 6), angle, 0, 360, (240, 240, 240), -1)
            else:
                # Sound whole rice kernel
                cv2.ellipse(img, (cx, cy), (20, 7), angle, 0, 360, (255, 255, 255), -1)

    out_path = SAMPLE_DIR / filename
    cv2.imwrite(str(out_path), img)
    print(f"Generated sample tray: {out_path}")

if __name__ == "__main__":
    create_demo_tray("rice_sample_good.jpg", broken_ratio=0.04, discolored_ratio=0.02, insect_ratio=0.01, foreign_ratio=0.01)
    create_demo_tray("rice_sample_broken.jpg", broken_ratio=0.18, discolored_ratio=0.04, insect_ratio=0.01, foreign_ratio=0.02)
    create_demo_tray("rice_sample_discolored.jpg", broken_ratio=0.06, discolored_ratio=0.15, insect_ratio=0.05, foreign_ratio=0.03)
