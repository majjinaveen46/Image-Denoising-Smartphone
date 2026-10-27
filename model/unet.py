import tensorflow as tf
from tensorflow.keras.layers import (
    Input,
    Conv2D,
    MaxPooling2D,
    UpSampling2D,
    Concatenate,
    BatchNormalization,
    Activation,
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from .metrics import psnr_metric, ssim_metric


def conv_block(x, filters: int, name: str):
    x = Conv2D(filters, (3, 3), padding="same", name=f"{name}_conv1")(x)
    x = BatchNormalization(name=f"{name}_bn1")(x)
    x = Activation("relu", name=f"{name}_relu1")(x)
    x = Conv2D(filters, (3, 3), padding="same", name=f"{name}_conv2")(x)
    x = BatchNormalization(name=f"{name}_bn2")(x)
    x = Activation("relu", name=f"{name}_relu2")(x)
    return x


def build_unet(input_shape=(None, None, 3), learning_rate=1e-3) -> Model:
    """
    Builds a U-Net model with multi-scale skip connections for image denoising.
    Input shape (None, None, 3) enables arbitrary height and width fully-convolutional inference.
    """
    inputs = Input(shape=input_shape, name="noisy_input")

    # Encoder (Contracting Path)
    c1 = conv_block(inputs, 32, "enc1")
    p1 = MaxPooling2D((2, 2), name="pool1")(c1)

    c2 = conv_block(p1, 64, "enc2")
    p2 = MaxPooling2D((2, 2), name="pool2")(c2)

    # Bottleneck
    b = conv_block(p2, 128, "bottleneck")

    # Decoder (Expansive Path with Skip Connections)
    u2 = UpSampling2D((2, 2), name="up2")(b)
    cat2 = Concatenate(name="concat2")([u2, c2])
    d2 = conv_block(cat2, 64, "dec2")

    u1 = UpSampling2D((2, 2), name="up1")(d2)
    cat1 = Concatenate(name="concat1")([u1, c1])
    d1 = conv_block(cat1, 32, "dec1")

    # Final Output Layer
    outputs = Conv2D(3, (1, 1), activation="sigmoid", name="denoised_output")(d1)

    model = Model(inputs=inputs, outputs=outputs, name="unet_denoiser")
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="mean_squared_error",
        metrics=[psnr_metric, ssim_metric, "mae"],
    )
    return model
