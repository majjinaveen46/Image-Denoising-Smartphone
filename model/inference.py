import os
import time
import math
from typing import Dict, Any, Tuple, Optional
import numpy as np
from PIL import Image, ImageOps
import cv2
import tensorflow as tf

from .metrics import psnr_metric, ssim_metric, compute_psnr_np, compute_ssim_np, estimate_noise_sigma
from .hybrid_unet_dncnn import build_hybrid_unet_dncnn


class DenoisingInferenceEngine:
    """
    Production-grade inference engine for Smartphone Image Denoising.
    Supports single model loading, full-resolution overlapping patch tiling,
    EXIF orientation correction, and metadata/metric extraction.
    """

    _instance = None

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_name = "Hybrid U-Net-DnCNN / CNN Denoising Engine"
        self.model_path = model_path
        self.params_count = 0
        self.trainable_params = 0
        self.is_hybrid = False
        self.load_model(model_path)

    @classmethod
    def get_instance(cls, model_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = cls(model_path)
        return cls._instance

    def _discover_model_path(self) -> Optional[str]:
        candidates = [
            "models/hybrid_unet_dncnn.keras",
            "models/image_denoising_model.keras",
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def load_model(self, model_path: Optional[str] = None):
        if model_path is None:
            model_path = self._discover_model_path()

        custom_objects = {
            "psnr_metric": psnr_metric,
            "ssim_metric": ssim_metric,
            "build_hybrid_unet_dncnn": build_hybrid_unet_dncnn,
        }

        if model_path and os.path.exists(model_path):
            print(f"[InferenceEngine] Loading existing model checkpoint from '{model_path}'...")
            try:
                self.model = tf.keras.models.load_model(
                    model_path,
                    custom_objects=custom_objects,
                    compile=False
                )
                self.model_path = model_path
                self.model_name = getattr(self.model, "name", "Trained Smartphone Denoising CNN")
                print(f"[InferenceEngine] Model loaded successfully: {self.model_name}")
            except Exception as e:
                print(f"[InferenceEngine] Error loading checkpoint: {e}. Instantiating fresh Hybrid U-Net-DnCNN architecture.")
                self.model = build_hybrid_unet_dncnn(input_shape=(None, None, 3))
                self.model_name = "Hybrid U-Net-DnCNN (Research Architecture)"
                self.model_path = "models/hybrid_unet_dncnn.keras"
        else:
            print("[InferenceEngine] Checkpoint not found. Instantiating fresh Hybrid U-Net-DnCNN architecture.")
            self.model = build_hybrid_unet_dncnn(input_shape=(None, None, 3))
            self.model_name = "Hybrid U-Net-DnCNN (Architecture Instantiated)"
            self.model_path = "models/hybrid_unet_dncnn.keras"

        # Check whether this model is Hybrid or Sequential
        if "hybrid" in str(getattr(self.model, "name", "")).lower():
            self.is_hybrid = True
        else:
            self.is_hybrid = False

        self.params_count = int(self.model.count_params())
        self.trainable_params = int(sum(tf.keras.backend.count_params(w) for w in self.model.trainable_weights))
        print(f"[InferenceEngine] Engine ready. Total Parameters: {self.params_count:,} (Trainable: {self.trainable_params:,})")

    def get_info(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "architecture_type": "Hybrid U-Net-DnCNN" if self.is_hybrid else "Deep Convolutional Denoiser",
            "model_path": self.model_path,
            "total_parameters": self.params_count,
            "trainable_parameters": self.trainable_params,
            "input_channels": 3,
            "receptive_field": "Multi-scale Contextual + High-frequency Residual",
            "supported_formats": ["JPEG", "JPG", "PNG", "WEBP"],
            "tiling_supported": True,
            "default_tile_size": 128,
            "status": "LOADED_AND_ACTIVE" if self.model is not None else "UNINITIALIZED",
        }

    def _tiled_inference(self, rgb_norm: np.ndarray, tile_size: int = 128, step: int = 64) -> np.ndarray:
        """
        Processes high-resolution smartphone photographs in overlapping tiles
        using 2D Hann window blending to completely eliminate boundary artifacts.
        Preserves 100% of original image dimensions and aspect ratio!
        """
        H, W, C = rgb_norm.shape

        # Create 2D Hann window for smooth seam blending
        hann_1d_h = np.hanning(tile_size)
        hann_1d_w = np.hanning(tile_size)
        hann_2d = np.outer(hann_1d_h, hann_1d_w).astype(np.float32)
        hann_2d = np.clip(hann_2d, 0.001, 1.0)[:, :, np.newaxis]

        # Calculate padding needed to cover entire image
        pad_h = (step - (H - tile_size) % step) % step if H > tile_size else (tile_size - H)
        pad_w = (step - (W - tile_size) % step) % step if W > tile_size else (tile_size - W)

        padded_img = np.pad(rgb_norm, ((0, pad_h), (0, pad_w), (0, 0)), mode="reflect")
        padded_H, padded_W, _ = padded_img.shape

        output_acc = np.zeros_like(padded_img, dtype=np.float32)
        weight_acc = np.zeros((padded_H, padded_W, 1), dtype=np.float32)

        tiles = []
        positions = []

        for y in range(0, padded_H - tile_size + 1, step):
            for x in range(0, padded_W - tile_size + 1, step):
                tile = padded_img[y : y + tile_size, x : x + tile_size, :]
                tiles.append(tile)
                positions.append((y, x))

        batch_size = 16
        tiles_arr = np.array(tiles, dtype=np.float32)
        preds = []

        for i in range(0, len(tiles_arr), batch_size):
            batch = tiles_arr[i : i + batch_size]
            batch_pred = self.model.predict(batch, verbose=0)
            preds.append(batch_pred)

        preds = np.concatenate(preds, axis=0)

        # Blend tiles back into full resolution output
        for (y, x), pred_tile in zip(positions, preds):
            output_acc[y : y + tile_size, x : x + tile_size, :] += pred_tile * hann_2d
            weight_acc[y : y + tile_size, x : x + tile_size, :] += hann_2d

        # Normalize by accumulated window weights
        weight_acc = np.maximum(weight_acc, 1e-6)
        denoised_padded = output_acc / weight_acc

        # Crop back to original dimensions
        denoised_rgb = denoised_padded[0:H, 0:W, :]
        return np.clip(denoised_rgb, 0.0, 1.0)

    def denoise_image(
        self,
        image_input,
        mode: str = "tiled",
        clean_reference=None,
    ) -> Dict[str, Any]:
        """
        Executes end-to-end denoising on a smartphone photograph.

        Args:
            image_input: PIL Image, filepath, or NumPy RGB array.
            mode: 'tiled' (high-fidelity full resolution) or 'resize' (fast 128x128).
            clean_reference: Optional clean ground-truth image for computing PSNR/SSIM.

        Returns:
            Dictionary with denoised PIL Image, original PIL Image, metrics, and runtime stats.
        """
        start_time = time.perf_counter()

        # Step 1: Safe image decoding and EXIF orientation normalization
        if isinstance(image_input, str):
            pil_img = Image.open(image_input)
        elif isinstance(image_input, Image.Image):
            pil_img = image_input
        elif isinstance(image_input, np.ndarray):
            pil_img = Image.fromarray(image_input)
        else:
            raise TypeError("Unsupported image input type")

        # Auto-transpose EXIF tag (critical for smartphone photos!)
        try:
            pil_img = ImageOps.exif_transpose(pil_img)
        except Exception:
            pass

        # Ensure RGB format (strip alpha channel if RGBA, or convert grayscale)
        pil_img = pil_img.convert("RGB")
        orig_w, orig_h = pil_img.size

        rgb_np = np.array(pil_img, dtype=np.float32) / 255.0

        # Step 2: Model Inference Execution
        if mode == "resize":
            # Fast preview mode
            resized = cv2.resize(rgb_np, (128, 128))
            input_batch = np.expand_dims(resized, axis=0)
            pred = self.model.predict(input_batch, verbose=0)[0]
            pred = np.clip(pred, 0.0, 1.0)
            denoised_rgb = cv2.resize(pred, (orig_w, orig_h))
        else:
            # Full-resolution Tiled Mode (Preserves aspect ratio, dimensions & sharpness)
            # If image is small enough (e.g. exactly 128x128), run direct:
            if orig_w == 128 and orig_h == 128:
                input_batch = np.expand_dims(rgb_np, axis=0)
                pred = self.model.predict(input_batch, verbose=0)[0]
                denoised_rgb = np.clip(pred, 0.0, 1.0)
            else:
                denoised_rgb = self._tiled_inference(rgb_np, tile_size=128, step=64)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

        # Step 3: Compute Real Metrics
        initial_noise_sigma = estimate_noise_sigma(rgb_np)
        final_noise_sigma = estimate_noise_sigma(denoised_rgb)
        noise_reduction_pct = max(0.0, round(((initial_noise_sigma - final_noise_sigma) / max(initial_noise_sigma, 1e-4)) * 100.0, 1))

        # Check clean reference if available
        psnr_val = None
        ssim_val = None
        if clean_reference is not None:
            if isinstance(clean_reference, str):
                ref_pil = ImageOps.exif_transpose(Image.open(clean_reference)).convert("RGB")
            else:
                ref_pil = clean_reference.convert("RGB")

            ref_rgb = np.array(ref_pil.resize((orig_w, orig_h)), dtype=np.float32) / 255.0
            psnr_val = round(compute_psnr_np(ref_rgb, denoised_rgb), 2)
            ssim_val = round(compute_ssim_np(ref_rgb, denoised_rgb), 4)

        # Convert back to uint8 PIL Image
        denoised_uint8 = (denoised_rgb * 255.0).round().astype(np.uint8)
        denoised_pil = Image.fromarray(denoised_uint8, mode="RGB")

        return {
            "denoised_image": denoised_pil,
            "original_image": pil_img,
            "width": orig_w,
            "height": orig_h,
            "aspect_ratio": f"{orig_w}:{orig_h} ({(orig_w / orig_h):.2f})",
            "processing_time_ms": elapsed_ms,
            "estimated_input_noise_sigma": initial_noise_sigma,
            "estimated_output_noise_sigma": final_noise_sigma,
            "noise_reduction_percentage": noise_reduction_pct,
            "psnr_db": psnr_val,
            "ssim": ssim_val,
            "model_name": self.model_name,
            "mode": mode,
        }
