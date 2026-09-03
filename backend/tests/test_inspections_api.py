import io
import cv2
import numpy as np

def create_synthetic_test_image_bytes():
    img = np.full((600, 600, 3), (30, 41, 59), dtype=np.uint8)
    for i in range(8):
        for j in range(8):
            cv2.ellipse(img, (70 + i * 60, 70 + j * 60), (14, 7), 30, 0, 360, (230, 230, 230), -1)
    
    _, buffer = cv2.imencode(".jpg", img)
    return io.BytesIO(buffer.tobytes())

def test_create_and_analyze_inspection(client):
    # 1. Create inspection session
    create_res = client.post("/api/inspections", json={"grain_type": "rice", "farmer_reference": "FARMER-TEST-01"})
    assert create_res.status_code == 201
    insp_id = create_res.json()["inspection_id"]
    assert insp_id is not None

    # 2. Upload image and execute analysis
    img_bytes = create_synthetic_test_image_bytes()
    files = {"file": ("test_sample.jpg", img_bytes, "image/jpeg")}
    analyze_res = client.post(f"/api/inspections/{insp_id}/analyze", files=files)
    assert analyze_res.status_code == 200
    data = analyze_res.json()

    assert data["status"] == "COMPLETED"
    assert data["total_objects"] > 0
    assert data["quality_result"] is not None
    assert data["certificate"] is not None
    assert len(data["detections"]) > 0

    # 3. Verify public certificate endpoint
    token = data["certificate"]["verification_token"]
    verify_res = client.get(f"/api/verify/{token}")
    assert verify_res.status_code == 200
    v_data = verify_res.json()
    assert v_data["verified"] is True
    assert v_data["certificate_number"] == data["certificate"]["certificate_number"]

def test_blurry_image_rejection(client):
    create_res = client.post("/api/inspections", json={"grain_type": "rice"})
    insp_id = create_res.json()["inspection_id"]

    # Flat image with 0 laplacian variance (pure blur)
    img = np.full((300, 300, 3), 128, dtype=np.uint8)
    _, buffer = cv2.imencode(".jpg", img)
    files = {"file": ("blurry.jpg", io.BytesIO(buffer.tobytes()), "image/jpeg")}

    res = client.post(f"/api/inspections/{insp_id}/analyze", files=files)
    assert res.status_code == 422
    assert "blurry" in res.json()["detail"].lower()
