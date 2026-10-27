import os
import sys
import argparse
import cv2
import numpy as np
import tensorflow as tf
from model import psnr_metric, ssim_metric

# Ensure utf-8 output where supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def calculate_metrics(clean_img, test_img):
    """
    Calculates PSNR and SSIM between two [0, 1] normalized float32 images.
    """
    clean_tensor = tf.convert_to_tensor(clean_img[np.newaxis, ...], dtype=tf.float32)
    test_tensor = tf.convert_to_tensor(test_img[np.newaxis, ...], dtype=tf.float32)

    psnr_val = float(tf.image.psnr(clean_tensor, test_tensor, max_val=1.0).numpy()[0])
    ssim_val = float(tf.image.ssim(clean_tensor, test_tensor, max_val=1.0).numpy()[0])
    return psnr_val, ssim_val


def get_default_model_path():
    """Finds available trained model."""
    candidates = ["models/image_denoising_model.keras", "image_denoising_model.keras"]
    for path in candidates:
        if os.path.exists(path):
            return path
    return "image_denoising_model.keras"


def denoise_image(image_path, model_path=None, clean_path=None, output_path=None):
    if model_path is None:
        model_path = get_default_model_path()

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at '{model_path}'. Run train.py first.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found at '{image_path}'")

    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(
        model_path,
        custom_objects={"psnr_metric": psnr_metric, "ssim_metric": ssim_metric},
        compile=False
    )

    # Read and resize noisy image
    noisy_bgr = cv2.imread(image_path)
    if noisy_bgr is None:
        raise ValueError(f"Failed to read image at '{image_path}'")

    resized_noisy = cv2.resize(noisy_bgr, (128, 128))
    input_tensor = resized_noisy.astype(np.float32) / 255.0
    input_batch = np.expand_dims(input_tensor, axis=0)

    # Predict denoised image
    print(f"Denoising '{image_path}'...")
    prediction = model.predict(input_batch, verbose=0)
    denoised_tensor = np.clip(prediction[0], 0.0, 1.0)
    denoised_bgr = (denoised_tensor * 255.0).astype(np.uint8)

    # Prepare output directories
    os.makedirs("outputs", exist_ok=True)
    if output_path is None:
        output_path = os.path.join("outputs", "denoised_output.png")

    # Save output images to destination and root for compatibility
    cv2.imwrite(output_path, denoised_bgr)
    cv2.imwrite("denoised_output.png", denoised_bgr)

    # Side-by-side comparison
    comparison = np.hstack((resized_noisy, denoised_bgr))
    comparison_path = os.path.join(os.path.dirname(output_path) or "outputs", "noisy_vs_denoised.png")
    cv2.imwrite(comparison_path, comparison)
    cv2.imwrite("noisy_vs_denoised.png", comparison)

    print("\nPrediction Completed Successfully!")
    print(f"  -> Denoised image saved to: {output_path} (and denoised_output.png)")
    print(f"  -> Side-by-side saved to:   {comparison_path} (and noisy_vs_denoised.png)")

    # Check for ground truth clean image
    if clean_path is None:
        # Check automatic correspondence (e.g. dataset/noisy/0001.png -> dataset/clean/0001.png)
        base_name = os.path.basename(image_path)
        auto_clean = os.path.join("dataset", "clean", base_name)
        if os.path.exists(auto_clean):
            clean_path = auto_clean

    if clean_path and os.path.exists(clean_path):
        clean_bgr = cv2.imread(clean_path)
        if clean_bgr is not None:
            clean_resized = cv2.resize(clean_bgr, (128, 128)).astype(np.float32) / 255.0
            noisy_psnr, noisy_ssim = calculate_metrics(clean_resized, input_tensor)
            den_psnr, den_ssim = calculate_metrics(clean_resized, denoised_tensor)

            print("\nQuantitative Evaluation against Clean Reference:")
            print(f"  Clean Reference Image: {clean_path}")
            print(f"  Noisy Input:   PSNR = {noisy_psnr:.2f} dB  |  SSIM = {noisy_ssim:.4f}")
            print(f"  Denoised:      PSNR = {den_psnr:.2f} dB  |  SSIM = {den_ssim:.4f}")
            print(f"  Improvement:   PSNR Gain = {den_psnr - noisy_psnr:+.2f} dB  |  SSIM Gain = {den_ssim - noisy_ssim:+.4f}")

    return denoised_bgr


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Denoising Inference Script")
    parser.add_argument("--image", type=str, default="dataset/noisy/0001.png", help="Path to input noisy image")
    parser.add_argument("--model", type=str, default=None, help="Path to trained .keras model")
    parser.add_argument("--clean", type=str, default=None, help="Path to reference clean image (optional)")
    parser.add_argument("--output", type=str, default="outputs/denoised_output.png", help="Output path for denoised image")

    args = parser.parse_args()
    denoise_image(
        image_path=args.image,
        model_path=args.model,
        clean_path=args.clean,
        output_path=args.output
    )
