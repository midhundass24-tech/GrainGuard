import json
from typing import List, Dict, Any, Tuple
from app.ai.base import RawDetection
from app.core.config import settings

class QualityEngine:
    """
    Transparent, configurable grain quality calculation engine.
    Calculates class distribution percentages, applies penalty formulas, and assigns quality grades.
    """

    @staticmethod
    def calculate_metrics(detections: List[RawDetection], grain_type: str = "rice") -> Dict[str, Any]:
        total_count = len(detections)
        if total_count == 0:
            return {
                "whole_percentage": 0.0,
                "broken_percentage": 0.0,
                "discolored_percentage": 0.0,
                "insect_damage_percentage": 0.0,
                "foreign_matter_percentage": 0.0,
                "quality_score": 0.0,
                "category": "Poor",
                "decision": "REJECTED",
                "penalties": {}
            }

        # Count occurrences per class
        counts = {
            "whole_grain": 0,
            "broken_grain": 0,
            "discolored_grain": 0,
            "insect_damaged": 0,
            "foreign_matter": 0
        }

        for d in detections:
            if d.class_name in counts:
                counts[d.class_name] += 1
            else:
                counts["foreign_matter"] += 1

        # Calculate exact percentages
        whole_pct = round((counts["whole_grain"] / total_count) * 100.0, 2)
        broken_pct = round((counts["broken_grain"] / total_count) * 100.0, 2)
        discolor_pct = round((counts["discolored_grain"] / total_count) * 100.0, 2)
        insect_pct = round((counts["insect_damaged"] / total_count) * 100.0, 2)
        foreign_pct = round((counts["foreign_matter"] / total_count) * 100.0, 2)

        # Get configurable grain-specific penalty weights
        grain_cfg = settings.QUALITY_THRESHOLDS.get(grain_type, settings.QUALITY_THRESHOLDS["rice"])
        penalties_cfg = grain_cfg["penalties"]
        limits_cfg = grain_cfg["limits"]

        # Deductions
        broken_deduction = broken_pct * penalties_cfg["broken_penalty_per_pct"]
        discolor_deduction = discolor_pct * penalties_cfg["discoloration_penalty_per_pct"]
        insect_deduction = insect_pct * penalties_cfg["insect_penalty_per_pct"]
        foreign_deduction = foreign_pct * penalties_cfg["foreign_matter_penalty_per_pct"]

        total_penalty = broken_deduction + discolor_deduction + insect_deduction + foreign_deduction
        raw_score = 100.0 - total_penalty
        final_score = round(max(0.0, min(100.0, raw_score)), 2)

        # Tier Categorization
        if final_score >= 90.0:
            category = "Excellent"
            decision = "ACCEPTABLE"
        elif final_score >= 75.0:
            category = "Good"
            decision = "ACCEPTABLE"
        elif final_score >= 60.0:
            category = "Needs Review"
            decision = "CONDITIONAL"
        else:
            category = "Poor"
            decision = "REJECTED"

        # Check hard reject limits
        if (
            broken_pct > limits_cfg["broken_reject"] or
            foreign_pct > limits_cfg["foreign_matter_reject"] or
            insect_pct > limits_cfg["insect_damage_reject"]
        ):
            decision = "REJECTED"
            if category in ["Excellent", "Good"]:
                category = "Needs Review"

        penalty_details = {
            "broken_penalty": round(broken_deduction, 2),
            "discoloration_penalty": round(discolor_deduction, 2),
            "insect_penalty": round(insect_deduction, 2),
            "foreign_matter_penalty": round(foreign_deduction, 2),
            "total_penalty": round(total_penalty, 2)
        }

        return {
            "whole_percentage": whole_pct,
            "broken_percentage": broken_pct,
            "discolored_percentage": discolor_pct,
            "insect_damage_percentage": insect_pct,
            "foreign_matter_percentage": foreign_pct,
            "quality_score": final_score,
            "category": category,
            "decision": decision,
            "penalties": penalty_details
        }
