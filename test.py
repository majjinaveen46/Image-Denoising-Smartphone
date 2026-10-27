import os
import sys
import numpy as np
import tensorflow as tf
from model import build_model, psnr_metric, ssim_metric

# Ensure utf-8 output where supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def test_build_standard_model():
    print("[1/5] Testing Standard Model Architecture...")
    model = build_model(input_shape=(128, 128, 3), model_type="standard")
    assert model is not None, "Model failed to build"
    dummy_input = np.random.uniform(0.0, 1.0, size=(2, 128, 128, 3)).astype(np.float32)
    output = model.predict(dummy_input, verbose=0)
    assert output.shape == (2, 128, 128, 3), f"Expected shape (2, 128, 128, 3), got {output.shape}"
    assert np.all(output >= 0.0) and np.all(output <= 1.0), "Outputs out of [0, 1] range"
    print("      [PASS] Standard model successfully built and inferred.")


def test_build_residual_model():
    print("[2/5] Testing Residual Model Architecture...")
    model = build_model(input_shape=(128, 128, 3), model_type="residual")
    assert model is not None, "Residual model failed to build"
    dummy_input = np.random.uniform(0.0, 1.0, size=(2, 128, 128, 3)).astype(np.float32)
    output = model.predict(dummy_input, verbose=0)
    assert output.shape == (2, 128, 128, 3), f"Expected shape (2, 128, 128, 3), got {output.shape}"
    print("      [PASS] Residual model successfully built and inferred.")


def test_metrics():
    print("[3/5] Testing PSNR and SSIM metrics...")
    img = tf.random.uniform(shape=(1, 64, 64, 3), minval=0.0, maxval=1.0)
    ssim_val = float(ssim_metric(img, img))
    assert np.isclose(ssim_val, 1.0, atol=1e-3), f"SSIM for identical images expected ~1.0, got {ssim_val}"

    noisy_img = tf.clip_by_value(img + tf.random.normal(shape=img.shape, stddev=0.1), 0.0, 1.0)
    psnr_val = float(psnr_metric(img, noisy_img))
    assert psnr_val > 0.0, f"PSNR should be positive, got {psnr_val}"
    print(f"      [PASS] Metrics verified: SSIM={ssim_val:.4f}, Sample Noisy PSNR={psnr_val:.2f} dB")


def test_dataset_integrity():
    print("[4/5] Checking Dataset Integrity...")
    clean_dir = "dataset/clean"
    noisy_dir = "dataset/noisy"

    if not os.path.exists(clean_dir) or not os.path.exists(noisy_dir):
        print("      [WARN] Dataset directory not found (skipping dataset checks).")
        return

    clean_files = sorted(os.listdir(clean_dir))
    noisy_files = sorted(os.listdir(noisy_dir))
    assert len(clean_files) > 0, "Clean dataset folder is empty"
    assert len(clean_files) == len(noisy_files), f"Count mismatch: {len(clean_files)} clean vs {len(noisy_files)} noisy"
    print(f"      [PASS] Dataset verified: {len(clean_files)} matched image pairs found.")


def test_saved_model():
    print("[5/5] Checking Saved Model Loading...")
    model_paths = ["models/image_denoising_model.keras", "image_denoising_model.keras"]
    loaded = False
    for path in model_paths:
        if os.path.exists(path):
            model = tf.keras.models.load_model(
                path,
                custom_objects={"psnr_metric": psnr_metric, "ssim_metric": ssim_metric},
                compile=False
            )
            dummy_input = np.zeros((1, 128, 128, 3), dtype=np.float32)
            out = model.predict(dummy_input, verbose=0)
            assert out.shape == (1, 128, 128, 3)
            print(f"      [PASS] Saved model at '{path}' loaded and executed successfully.")
            loaded = True
            break
    if not loaded:
        print("      [WARN] No saved model found yet. Run train.py to generate one.")


if __name__ == "__main__":
    print("=" * 60)
    print(" Running Image Denoising Project Test Suite")
    print("=" * 60)
    test_build_standard_model()
    test_build_residual_model()
    test_metrics()
    test_dataset_integrity()
    test_saved_model()
    print("=" * 60)
    print(" All tests passed successfully!")
    print("=" * 60)
