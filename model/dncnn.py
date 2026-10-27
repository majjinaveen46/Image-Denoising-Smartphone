import tensorflow as tf
from tensorflow.keras.layers import (
    Input,
    Conv2D,
    BatchNormalization,
    Activation,
    Subtract,
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from .metrics import psnr_metric, ssim_metric


def build_dncnn(depth=10, num_filters=64, input_shape=(None, None, 3), learning_rate=1e-3) -> Model:
    """
    Builds a DnCNN (Denoising Convolutional Neural Network) model.
    The network predicts the residual noise map R(y), and the denoised
    image is computed via residual subtraction: x_hat = y - R(y).
    """
    inputs = Input(shape=input_shape, name="noisy_input")

    # Layer 1: Conv + ReLU (no BN)
    x = Conv2D(num_filters, (3, 3), padding="same", name="dncnn_conv1")(inputs)
    x = Activation("relu", name="dncnn_relu1")(x)

    # Intermediate Layers: Conv + BN + ReLU
    for i in range(2, depth):
        x = Conv2D(num_filters, (3, 3), padding="same", name=f"dncnn_conv{i}")(x)
        x = BatchNormalization(name=f"dncnn_bn{i}")(x)
        x = Activation("relu", name=f"dncnn_relu{i}")(x)

    # Final Layer: Conv to reconstruct residual noise map (3 channels)
    residual_noise = Conv2D(3, (3, 3), padding="same", name="predicted_noise")(x)

    # Residual Subtraction: Denoised = Input - ResidualNoise
    denoised = Subtract(name="residual_subtract")([inputs, residual_noise])
    outputs = Activation("sigmoid", name="denoised_output")(denoised)

    model = Model(inputs=inputs, outputs=outputs, name="dncnn_denoiser")
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="mean_squared_error",
        metrics=[psnr_metric, ssim_metric, "mae"],
    )
    return model
