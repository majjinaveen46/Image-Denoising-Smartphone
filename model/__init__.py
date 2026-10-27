"""
Image Denoising Models Package
Contains modular implementations of:
- U-Net (Multi-scale Contextual Denoiser)
- DnCNN (Deep Convolutional Residual Noise Estimator)
- Hybrid U-Net-DnCNN (State-of-the-art smartphone image denoiser)
- Standard 3-Layer Baseline Denoiser
"""

import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Add, Activation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from .metrics import psnr_metric, ssim_metric, compute_psnr_np, compute_ssim_np
from .unet import build_unet
from .dncnn import build_dncnn
from .hybrid_unet_dncnn import build_hybrid_unet_dncnn
from .inference import DenoisingInferenceEngine


def build_model(input_shape=(128, 128, 3), learning_rate=0.001, model_type="standard"):
    """
    Unified model factory for image denoising.

    Args:
        input_shape: Image input shape (height, width, channels).
        learning_rate: Adam optimizer learning rate.
        model_type: 'hybrid' (Hybrid U-Net-DnCNN), 'unet', 'dncnn', 'residual', or 'standard'.
    """
    if model_type == "hybrid":
        return build_hybrid_unet_dncnn(input_shape=input_shape, learning_rate=learning_rate)
    elif model_type == "unet":
        return build_unet(input_shape=input_shape, learning_rate=learning_rate)
    elif model_type == "dncnn":
        return build_dncnn(input_shape=input_shape, learning_rate=learning_rate)
    elif model_type == "residual":
        inputs = Input(shape=input_shape, name="noisy_input")
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv1")(inputs)
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv2")(x)
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv3")(x)
        res = Conv2D(3, (3, 3), padding="same", name="residual_conv")(x)
        added = Add(name="residual_add")([inputs, res])
        outputs = Activation("sigmoid", name="denoised_output")(added)
        model = Model(inputs=inputs, outputs=outputs, name="residual_denoiser")
        model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss="mean_squared_error",
            metrics=[psnr_metric, "mae"],
        )
        return model
    else:
        # Standard 3-layer baseline CNN
        inputs = Input(shape=input_shape, name="noisy_input")
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv1")(inputs)
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv2")(x)
        outputs = Conv2D(3, (3, 3), activation="sigmoid", padding="same", name="denoised_output")(x)
        model = Model(inputs=inputs, outputs=outputs, name="standard_denoiser")
        model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss="mean_squared_error",
            metrics=[psnr_metric, "mae"],
        )
        return model


__all__ = [
    "build_model",
    "build_unet",
    "build_dncnn",
    "build_hybrid_unet_dncnn",
    "DenoisingInferenceEngine",
    "psnr_metric",
    "ssim_metric",
    "compute_psnr_np",
    "compute_ssim_np",
]
