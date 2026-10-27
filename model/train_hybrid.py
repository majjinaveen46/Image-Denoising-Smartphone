import os
import sys
import argparse
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

from .hybrid_unet_dncnn import build_hybrid_unet_dncnn
from .metrics import psnr_metric, ssim_metric


def extract_patches(clean_folder="dataset/clean", noisy_folder="dataset/noisy", patch_size=128, patches_per_image=10):
    """
    Extracts random non-distorted patches from full-resolution smartphone images.
    Preserves fine high-frequency noise textures and sharp ground-truth edges.
    """
    clean_patches = []
    noisy_patches = []

    files = sorted(os.listdir(clean_folder))
    print(f"[Dataset] Extracting {patches_per_image} patches of {patch_size}x{patch_size} from {len(files)} image pairs...")

    for fname in files:
        c_path = os.path.join(clean_folder, fname)
        n_path = os.path.join(noisy_folder, fname)
        if not os.path.exists(n_path):
            continue

        c_img = cv2.imread(c_path)
        n_img = cv2.imread(n_path)
        if c_img is None or n_img is None:
            continue

        # Convert to RGB and normalize to [0, 1]
        c_img = cv2.cvtColor(c_img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        n_img = cv2.cvtColor(n_img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

        H, W, _ = c_img.shape
        if H < patch_size or W < patch_size:
            continue

        for _ in range(patches_per_image):
            y = random.randint(0, H - patch_size)
            x = random.randint(0, W - patch_size)

            c_patch = c_img[y : y + patch_size, x : x + patch_size, :]
            n_patch = n_img[y : y + patch_size, x : x + patch_size, :]

            # Random horizontal/vertical flip augmentation
            if random.random() > 0.5:
                c_patch = np.fliplr(c_patch)
                n_patch = np.fliplr(n_patch)
            if random.random() > 0.5:
                c_patch = np.flipud(c_patch)
                n_patch = np.flipud(n_patch)

            clean_patches.append(c_patch)
            noisy_patches.append(n_patch)

    X_train = np.array(noisy_patches, dtype=np.float32)
    Y_train = np.array(clean_patches, dtype=np.float32)
    print(f"[Dataset] Generated {len(X_train)} training patches: shape {X_train.shape}")
    return X_train, Y_train


def train_hybrid(
    epochs: int = 50,
    batch_size: int = 16,
    patches_per_image: int = 10,
    learning_rate: float = 1e-3,
    output_model_path: str = "models/hybrid_unet_dncnn.keras",
):
    os.makedirs("models", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    X_train, Y_train = extract_patches(
        clean_folder="dataset/clean",
        noisy_folder="dataset/noisy",
        patch_size=128,
        patches_per_image=patches_per_image,
    )

    print("\n[Hybrid U-Net-DnCNN] Compiling model...")
    model = build_hybrid_unet_dncnn(
        input_shape=(128, 128, 3),
        learning_rate=learning_rate,
    )
    model.summary()

    callbacks = [
        ModelCheckpoint(
            filepath=output_model_path,
            monitor="val_psnr_metric",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),
        EarlyStopping(
            monitor="val_psnr_metric",
            mode="max",
            patience=15,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=5,
            min_lr=1e-5,
            verbose=1,
        ),
    ]

    print("\n[Hybrid U-Net-DnCNN] Commencing training...")
    history = model.fit(
        X_train,
        Y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.15,
        callbacks=callbacks,
        shuffle=True,
    )

    # Plot results
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history.history["loss"], label="Train Loss (MSE)")
    if "val_loss" in history.history:
        plt.plot(history.history["val_loss"], label="Val Loss (MSE)")
    plt.title("Hybrid Model Loss")
    plt.xlabel("Epoch")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    if "psnr_metric" in history.history:
        plt.plot(history.history["psnr_metric"], label="Train PSNR (dB)")
        if "val_psnr_metric" in history.history:
            plt.plot(history.history["val_psnr_metric"], label="Val PSNR (dB)")
        plt.title("Hybrid Model PSNR")
        plt.xlabel("Epoch")
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.savefig("outputs/hybrid_training_history.png", dpi=200)
    plt.close()
    print(f"[Hybrid U-Net-DnCNN] Training complete! Saved to {output_model_path}")
    return model, history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Hybrid U-Net-DnCNN on Smartphone Image Dataset")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--patches-per-image", type=int, default=8)
    parser.add_argument("--lr", type=float, default=0.001)

    args = parser.parse_args()
    train_hybrid(
        epochs=args.epochs,
        batch_size=args.batch_size,
        patches_per_image=args.patches_per_image,
        learning_rate=args.lr,
    )
