from app.services.quality_engine import QualityEngine
from app.ai.base import RawDetection

def test_quality_engine_calculation():
    # 90 whole, 5 broken, 3 discolored, 1 insect, 1 foreign
    detections = []
    for _ in range(90):
        detections.append(RawDetection(class_name="whole_grain", confidence=0.95, bbox=[0,0,10,10], area=100))
    for _ in range(5):
        detections.append(RawDetection(class_name="broken_grain", confidence=0.91, bbox=[0,0,10,10], area=50))
    for _ in range(3):
        detections.append(RawDetection(class_name="discolored_grain", confidence=0.88, bbox=[0,0,10,10], area=95))
    for _ in range(1):
        detections.append(RawDetection(class_name="insect_damaged", confidence=0.92, bbox=[0,0,10,10], area=90))
    for _ in range(1):
        detections.append(RawDetection(class_name="foreign_matter", confidence=0.85, bbox=[0,0,10,10], area=200))

    metrics = QualityEngine.calculate_metrics(detections, grain_type="rice")

    assert metrics["whole_percentage"] == 90.0
    assert metrics["broken_percentage"] == 5.0
    assert metrics["discolored_percentage"] == 3.0
    assert metrics["insect_damage_percentage"] == 1.0
    assert metrics["foreign_matter_percentage"] == 1.0
    assert metrics["quality_score"] > 60.0
    assert metrics["category"] in ["Good", "Needs Review", "Excellent"]
