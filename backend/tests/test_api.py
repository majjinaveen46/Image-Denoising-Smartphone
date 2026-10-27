import io
import os
import sys
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.main import app

client = TestClient(app)


def test_health_check():
    print("[API Test 1/5] Testing GET /api/health...")
    with client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True
        print(f"      [PASS] Health check OK. Model loaded: {data['model_name']}")


def test_model_info():
    print("[API Test 2/5] Testing GET /api/model-info...")
    with client:
        response = client.get("/api/model-info")
        assert response.status_code == 200
        data = response.json()
        assert "Image Denoising" in data["project_title"]
        assert "architecture_summary" in data
        assert data["architecture_summary"]["total_parameters"] > 0
        print(f"      [PASS] Model Info OK. Parameters: {data['architecture_summary']['total_parameters']:,}")


def test_upload_and_denoise_valid_image():
    print("[API Test 3/5] Testing POST /api/denoise with valid synthetic image...")
    # Create a synthetic noisy RGB image in memory
    img = Image.fromarray(np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8), mode="RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    with client:
        response = client.post(
            "/api/denoise",
            files={"file": ("test_noisy.png", buf.getvalue(), "image/png")},
            data={"mode": "resize"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["original_image"].startswith("data:image/png;base64,")
        assert data["denoised_image"].startswith("data:image/png;base64,")
        assert data["metadata"]["width"] == 128
        assert data["metadata"]["height"] == 128
        assert data["metadata"]["processing_time_ms"] > 0
        print(f"      [PASS] Denoising completed in {data['metadata']['processing_time_ms']} ms")


def test_invalid_file_rejection():
    print("[API Test 4/5] Testing rejection of corrupted / invalid files...")
    corrupted_bytes = b"This is a text file payload pretending to be an image."
    with client:
        response = client.post(
            "/api/denoise",
            files={"file": ("malicious.png", corrupted_bytes, "image/png")},
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        print(f"      [PASS] Invalid file correctly rejected with HTTP 400: '{data['detail']}'")


def test_sample_denoise():
    print("[API Test 5/5] Testing GET /api/samples and POST /api/denoise-sample...")
    with client:
        samples_res = client.get("/api/samples")
        assert samples_res.status_code == 200
        samples_data = samples_res.json()
        assert "samples" in samples_data

        if len(samples_data["samples"]) > 0:
            sample_id = samples_data["samples"][0]["id"]
            denoise_res = client.post("/api/denoise-sample", data={"sample_id": sample_id, "mode": "resize"})
            assert denoise_res.status_code == 200
            res_data = denoise_res.json()
            assert res_data["success"] is True
            assert res_data["metrics"]["psnr_db"] is not None
            print(f"      [PASS] Sample '{sample_id}' successfully evaluated: PSNR={res_data['metrics']['psnr_db']} dB")
        else:
            print("      [WARN] No samples directory found, skipping sample denoise.")


if __name__ == "__main__":
    print("=" * 60)
    print(" Running Backend API Test Suite")
    print("=" * 60)
    test_health_check()
    test_model_info()
    test_upload_and_denoise_valid_image()
    test_invalid_file_rejection()
    test_sample_denoise()
    print("=" * 60)
    print(" All Backend API Tests Passed!")
    print("=" * 60)
