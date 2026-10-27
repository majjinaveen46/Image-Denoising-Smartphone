import os
import sys
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Ensure utf-8 output where supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def calculate_metrics(clean_img, test_img):
    clean_tensor = tf.convert_to_tensor(clean_img[np.newaxis, ...], dtype=tf.float32)
    test_tensor = tf.convert_to_tensor(test_img[np.newaxis, ...], dtype=tf.float32)

    psnr_val = float(tf.image.psnr(clean_tensor, test_tensor, max_val=1.0).numpy()[0])
    ssim_val = float(tf.image.ssim(clean_tensor, test_tensor, max_val=1.0).numpy()[0])
    return psnr_val, ssim_val


def compare_images(clean_path, noisy_path, denoised_path, output_plot_path="outputs/comparison_plot.png", show=False):
    # Verify file paths
    for p, name in [(clean_path, "Clean"), (noisy_path, "Noisy"), (denoised_path, "Denoised")]:
        if not os.path.exists(p):
            raise FileNotFoundError(f"{name} image not found at '{p}'")

    # Read images (OpenCV reads in BGR)
    clean_bgr = cv2.imread(clean_path)
    noisy_bgr = cv2.imread(noisy_path)
    denoised_bgr = cv2.imread(denoised_path)

    # Use denoised image resolution (e.g., 128x128) as standard comparison size
    target_size = (denoised_bgr.shape[1], denoised_bgr.shape[0])

    # Resize clean and noisy to match denoised dimensions for fair comparison
    clean_matched = cv2.resize(clean_bgr, target_size)
    noisy_matched = cv2.resize(noisy_bgr, target_size)

    # Convert to RGB for matplotlib display
    clean_rgb = cv2.cvtColor(clean_matched, cv2.COLOR_BGR2RGB)
    noisy_rgb = cv2.cvtColor(noisy_matched, cv2.COLOR_BGR2RGB)
    denoised_rgb = cv2.cvtColor(denoised_bgr, cv2.COLOR_BGR2RGB)

    # Compute metrics normalized to [0, 1]
    clean_norm = clean_matched.astype(np.float32) / 255.0
    noisy_norm = noisy_matched.astype(np.float32) / 255.0
    denoised_norm = denoised_bgr.astype(np.float32) / 255.0

    noisy_psnr, noisy_ssim = calculate_metrics(clean_norm, noisy_norm)
    den_psnr, den_ssim = calculate_metrics(clean_norm, denoised_norm)

    # Plot comparison
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(clean_rgb)
    axes[0].set_title("Original Clean (Reference)\nDimensions: {}x{}".format(*target_size), fontsize=11, fontweight="bold")
    axes[0].axis("off")

    axes[1].imshow(noisy_rgb)
    axes[1].set_title(f"Noisy Input\nPSNR: {noisy_psnr:.2f} dB | SSIM: {noisy_ssim:.4f}", fontsize=11, fontweight="bold", color="darkred")
    axes[1].axis("off")

    axes[2].imshow(denoised_rgb)
    axes[2].set_title(f"Denoised Model Output\nPSNR: {den_psnr:.2f} dB | SSIM: {den_ssim:.4f}", fontsize=11, fontweight="bold", color="darkgreen")
    axes[2].axis("off")

    plt.tight_layout()

    # Save plot to outputs directory
    os.makedirs(os.path.dirname(output_plot_path) or "outputs", exist_ok=True)
    plt.savefig(output_plot_path, dpi=200, bbox_inches="tight")
    print(f"Comparison plot successfully saved to: {output_plot_path}")

    if show:
        try:
            plt.show()
        except Exception as e:
            print(f"Could not open GUI window ({e}). Plot is saved at {output_plot_path}")

    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Side-by-Side Denoising Visualizer")
    parser.add_argument("--clean", type=str, default="dataset/clean/0001.png", help="Path to clean reference image")
    parser.add_argument("--noisy", type=str, default="dataset/noisy/0001.png", help="Path to noisy input image")
    parser.add_argument("--denoised", type=str, default="outputs/denoised_output.png", help="Path to denoised output image")
    parser.add_argument("--output", type=str, default="outputs/comparison_plot.png", help="Path to save comparison figure")
    parser.add_argument("--show", action="store_true", help="Display interactive plot window")

    args = parser.parse_args()

    compare_images(
        clean_path=args.clean,
        noisy_path=args.noisy,
        denoised_path=args.denoised,
        output_plot_path=args.output,
        show=args.show
    )
