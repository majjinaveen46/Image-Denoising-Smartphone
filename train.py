import os
import sys
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from model import build_model, psnr_metric, ssim_metric

# Ensure utf-8 output where supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_dataset(clean_folder="dataset/clean", noisy_folder="dataset/noisy", image_size=(128, 128)):
    """
    Loads matched pairs of clean and noisy images.
    """
    if not os.path.exists(clean_folder):
        raise FileNotFoundError(f"Clean folder '{clean_folder}' does not exist.")
    if not os.path.exists(noisy_folder):
        raise FileNotFoundError(f"Noisy folder '{noisy_folder}' does not exist.")

    clean_images = []
    noisy_images = []

    filenames = sorted(os.listdir(clean_folder))
    print(f"Loading {len(filenames)} images from dataset...")

    for filename in filenames:
        clean_path = os.path.join(clean_folder, filename)
        noisy_path = os.path.join(noisy_folder, filename)

        if os.path.exists(noisy_path):
            clean = cv2.imread(clean_path)
            noisy = cv2.imread(noisy_path)

            if clean is None or noisy is None:
                continue

            clean = cv2.resize(clean, image_size).astype(np.float32) / 255.0
            noisy = cv2.resize(noisy, image_size).astype(np.float32) / 255.0

            clean_images.append(clean)
            noisy_images.append(noisy)

    clean_arr = np.array(clean_images, dtype=np.float32)
    noisy_arr = np.array(noisy_images, dtype=np.float32)

    print("\nDataset Loaded Successfully!")
    print(f"  Clean Images: {clean_arr.shape}")
    print(f"  Noisy Images: {noisy_arr.shape}")

    return clean_arr, noisy_arr


def plot_and_save_history(history, output_path="outputs/training_history.png"):
    """
    Plots training and validation loss and PSNR curves.
    """
    os.makedirs(os.path.dirname(output_path) or "outputs", exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Loss curve
    axes[0].plot(history.history["loss"], label="Train Loss (MSE)", color="royalblue", linewidth=2)
    if "val_loss" in history.history:
        axes[0].plot(history.history["val_loss"], label="Val Loss (MSE)", color="darkorange", linewidth=2)
    axes[0].set_title("Training & Validation Loss", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Mean Squared Error")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    # PSNR curve
    if "psnr_metric" in history.history:
        axes[1].plot(history.history["psnr_metric"], label="Train PSNR (dB)", color="forestgreen", linewidth=2)
        if "val_psnr_metric" in history.history:
            axes[1].plot(history.history["val_psnr_metric"], label="Val PSNR (dB)", color="crimson", linewidth=2)
        axes[1].set_title("Training & Validation PSNR", fontsize=12, fontweight="bold")
        axes[1].set_xlabel("Epoch")
        axes[1].set_ylabel("PSNR (dB)")
        axes[1].grid(True, linestyle="--", alpha=0.6)
        axes[1].legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Training history plot saved to: {output_path}")


def train(epochs=100, batch_size=8, validation_split=0.2, model_type="standard", learning_rate=0.001):
    os.makedirs("models", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    clean_images, noisy_images = load_dataset()

    print(f"\nBuilding model architecture ('{model_type}')...")
    model = build_model(
        input_shape=(128, 128, 3),
        learning_rate=learning_rate,
        model_type=model_type
    )
    model.summary()

    model_dest_path = "models/image_denoising_model.keras"

    callbacks = [
        ModelCheckpoint(
            filepath=model_dest_path,
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor="val_loss",
            patience=20,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=6,
            min_lr=1e-5,
            verbose=1
        )
    ]

    print("\nTraining Started...")
    history = model.fit(
        noisy_images,
        clean_images,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=callbacks,
        shuffle=True
    )

    print("\nTraining Complete!")
    print(f"Model saved to: {model_dest_path}")

    # Plot history
    plot_and_save_history(history, "outputs/training_history.png")

    return model, history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CNN Image Denoising Model")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size")
    parser.add_argument("--val-split", type=float, default=0.2, help="Validation data fraction")
    parser.add_argument("--model-type", type=str, choices=["standard", "residual"], default="standard", help="Model architecture")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")

    args = parser.parse_args()

    train(
        epochs=args.epochs,
        batch_size=args.batch_size,
        validation_split=args.val_split,
        model_type=args.model_type,
        learning_rate=args.lr
    )
