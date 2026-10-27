import os
import sys
import time
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image

# Ensure project root is in python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from model.inference import DenoisingInferenceEngine
from backend.processing import (
    validate_and_decode_upload,
    image_to_base64_data_uri,
    image_to_bytes,
    ImageValidationError,
)

SERVER_START_TIME = time.time()
inference_engine: Optional[DenoisingInferenceEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler. Loads the trained deep learning model
    once upon server initialization to prevent per-request reloading.
    """
    global inference_engine
    print("[Server Startup] Initializing Denoising Inference Engine...")
    inference_engine = DenoisingInferenceEngine.get_instance()
    print("[Server Startup] Model ready. Server accepting requests.")
    yield
    print("[Server Shutdown] Cleaning up resources...")


app = FastAPI(
    title="Smartphone Image Denoising API",
    description="Academic Deep Learning Service for 'Image Denoising Using Machine Learning for Smartphone Images'",
    version="2.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """
    Verifies backend service operational health and model loading state.
    """
    global inference_engine
    uptime = round(time.time() - SERVER_START_TIME, 1)
    is_loaded = inference_engine is not None and inference_engine.model is not None
    return {
        "status": "healthy" if is_loaded else "degraded",
        "service": "Smartphone Image Denoising API",
        "version": "2.0.0",
        "uptime_seconds": uptime,
        "model_loaded": is_loaded,
        "model_name": inference_engine.model_name if inference_engine else None,
        "backend_framework": "FastAPI + TensorFlow 2.16+",
    }


@app.get("/api/model-info")
async def get_model_info():
    """
    Returns verified architectural metadata, parameter counts, and research details.
    """
    global inference_engine
    if inference_engine is None:
        raise HTTPException(status_code=503, detail="Inference engine not initialized")

    info = inference_engine.get_info()
    return {
        "project_title": "Image Denoising Using Machine Learning for Smartphone Images",
        "academic_context": "Engineering / Computer Science Capstone Research Project",
        "architecture_summary": {
            "name": info["model_name"],
            "type": info["architecture_type"],
            "total_parameters": info["total_parameters"],
            "trainable_parameters": info["trainable_parameters"],
            "receptive_field": info["receptive_field"],
            "input_channels": info["input_channels"],
            "checkpoint_path": info["model_path"],
            "checkpoint_status": "ACTIVE_TRAINED_CHECKPOINT" if info["model_path"] else "IN_MEMORY_COMPILED",
        },
        "technologies": {
            "deep_learning": "TensorFlow / Keras",
            "computer_vision": "OpenCV / Pillow",
            "api_server": "FastAPI (Python 3.11)",
            "frontend_stack": "React 18 + Vite + TypeScript + Tailwind CSS",
        },
        "supported_features": {
            "arbitrary_dimensions": True,
            "full_resolution_tiling": True,
            "hann_window_blending": True,
            "exif_orientation_correction": True,
            "formats": info["supported_formats"],
        },
        "training_dataset_summary": {
            "description": "Paired high-resolution smartphone photographs (100 clean, 100 noisy pairs)",
            "native_resolution": "1404 x 2040 pixels",
            "noise_profile": "Additive sensor noise, digital amplification, low-light ISO grain",
        },
    }


@app.post("/api/denoise")
async def denoise_image_endpoint(
    file: UploadFile = File(...),
    mode: str = Form("tiled"),
):
    """
    Accepts a user-uploaded smartphone photograph, executes model inference,
    and returns the denoised result alongside quantitative metadata and metrics.
    """
    global inference_engine
    if inference_engine is None:
        raise HTTPException(status_code=503, detail="Inference engine not ready")

    # Read uploaded file bytes securely
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file payload: {str(e)}")

    # Validate image format and dimensions
    try:
        pil_image = validate_and_decode_upload(file_bytes, file.filename or "upload.png")
    except ImageValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    # Execute deep learning inference
    try:
        result = inference_engine.denoise_image(pil_image, mode=mode)
    except Exception as e:
        print(f"[Denoise Error] Inference failure: {e}")
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

    # Convert results to Base64 data URIs for immediate browser rendering
    orig_b64 = image_to_base64_data_uri(result["original_image"], format="PNG")
    denoised_b64 = image_to_base64_data_uri(result["denoised_image"], format="PNG")

    return {
        "success": True,
        "filename": file.filename,
        "original_image": orig_b64,
        "denoised_image": denoised_b64,
        "metadata": {
            "width": result["width"],
            "height": result["height"],
            "aspect_ratio": result["aspect_ratio"],
            "processing_time_ms": result["processing_time_ms"],
            "model_name": result["model_name"],
            "processing_mode": result["mode"],
        },
        "metrics": {
            "estimated_input_noise_sigma": result["estimated_input_noise_sigma"],
            "estimated_output_noise_sigma": result["estimated_output_noise_sigma"],
            "noise_reduction_percentage": result["noise_reduction_percentage"],
            "psnr_db": result["psnr_db"],
            "ssim": result["ssim"],
        },
    }


@app.get("/api/samples")
async def get_dataset_samples():
    """
    Returns curated demo pairs from the dataset for users who wish to test
    instantly with authentic smartphone test data.
    """
    samples = []
    clean_dir = os.path.join(ROOT_DIR, "dataset", "clean")
    noisy_dir = os.path.join(ROOT_DIR, "dataset", "noisy")

    if os.path.exists(noisy_dir) and os.path.exists(clean_dir):
        # Pick 3 representative samples
        target_ids = ["0001", "0002", "0005"]
        for tid in target_ids:
            fname = f"{tid}.png"
            c_path = os.path.join(clean_dir, fname)
            n_path = os.path.join(noisy_dir, fname)
            if os.path.exists(c_path) and os.path.exists(n_path):
                # Generate small thumbnail data URIs for quick client previews
                try:
                    c_thumb = Image.open(c_path).resize((256, 176))
                    n_thumb = Image.open(n_path).resize((256, 176))
                    samples.append({
                        "id": tid,
                        "title": f"Smartphone Sample #{tid}",
                        "noisy_thumbnail": image_to_base64_data_uri(n_thumb, format="JPEG"),
                        "clean_thumbnail": image_to_base64_data_uri(c_thumb, format="JPEG"),
                        "noisy_path": f"dataset/noisy/{fname}",
                        "clean_path": f"dataset/clean/{fname}",
                    })
                except Exception as e:
                    print(f"Error loading sample thumbnail {fname}: {e}")

    return {"samples": samples}


@app.post("/api/denoise-sample")
async def denoise_sample_endpoint(sample_id: str = Form(...), mode: str = Form("resize")):
    """
    Executes denoising on an authentic dataset sample, calculating exact ground-truth PSNR and SSIM.
    """
    global inference_engine
    if inference_engine is None:
        raise HTTPException(status_code=503, detail="Inference engine not ready")

    noisy_path = os.path.join(ROOT_DIR, "dataset", "noisy", f"{sample_id}.png")
    clean_path = os.path.join(ROOT_DIR, "dataset", "clean", f"{sample_id}.png")

    if not os.path.exists(noisy_path):
        raise HTTPException(status_code=404, detail=f"Sample '{sample_id}' not found")

    result = inference_engine.denoise_image(
        noisy_path,
        mode=mode,
        clean_reference=clean_path if os.path.exists(clean_path) else None,
    )

    orig_b64 = image_to_base64_data_uri(result["original_image"], format="PNG")
    denoised_b64 = image_to_base64_data_uri(result["denoised_image"], format="PNG")

    return {
        "success": True,
        "sample_id": sample_id,
        "original_image": orig_b64,
        "denoised_image": denoised_b64,
        "metadata": {
            "width": result["width"],
            "height": result["height"],
            "aspect_ratio": result["aspect_ratio"],
            "processing_time_ms": result["processing_time_ms"],
            "model_name": result["model_name"],
            "processing_mode": result["mode"],
        },
        "metrics": {
            "estimated_input_noise_sigma": result["estimated_input_noise_sigma"],
            "estimated_output_noise_sigma": result["estimated_output_noise_sigma"],
            "noise_reduction_percentage": result["noise_reduction_percentage"],
            "psnr_db": result["psnr_db"],
            "ssim": result["ssim"],
        },
    }


# Mount production frontend static files if built
from fastapi.staticfiles import StaticFiles

dist_dir = os.path.join(ROOT_DIR, "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static_frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
