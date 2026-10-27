import tensorflow as tf
from tensorflow.keras.layers import (
    Input,
    Conv2D,
    MaxPooling2D,
    UpSampling2D,
    Concatenate,
    BatchNormalization,
    Activation,
    Subtract,
    Multiply,
    add,
)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from .metrics import psnr_metric, ssim_metric


def build_hybrid_unet_dncnn(
    input_shape=(None, None, 3),
    unet_base_filters: int = 32,
    dncnn_depth: int = 6,
    learning_rate: float = 1e-3,
) -> Model:
    """
    Hybrid U-Net-DnCNN Architecture for Smartphone Image Denoising.

    Synergizes:
    1. Multi-scale U-Net Branch: Captures broad contextual representations,
       luminance uniformity, and semantic scene structure via contracting/expansive paths.
    2. Deep Residual DnCNN Branch: Isolates localized high-frequency sensor noise
       patterns and fine textural edges without spatial pooling degradation.
    3. Cross-Feature Fusion Unit: Combines U-Net and DnCNN feature maps via 1x1 convolutions
       and channel-wise gated modulation to produce the final noise residual estimation.
    4. Residual Subtraction: x_hat = clip(y - R_hybrid(y), 0, 1).
    """
    inputs = Input(shape=input_shape, name="noisy_input")

    # ==========================================
    # BRANCH 1: Multi-scale Contextual U-Net
    # ==========================================
    # Encoder Level 1
    u_c1 = Conv2D(unet_base_filters, (3, 3), padding="same", name="u_enc1_conv1")(inputs)
    u_c1 = BatchNormalization(name="u_enc1_bn1")(u_c1)
    u_c1 = Activation("relu", name="u_enc1_relu1")(u_c1)
    u_c1 = Conv2D(unet_base_filters, (3, 3), padding="same", name="u_enc1_conv2")(u_c1)
    u_c1 = BatchNormalization(name="u_enc1_bn2")(u_c1)
    u_c1 = Activation("relu", name="u_enc1_relu2")(u_c1)

    u_p1 = MaxPooling2D((2, 2), name="u_pool1")(u_c1)

    # Encoder Level 2
    u_c2 = Conv2D(unet_base_filters * 2, (3, 3), padding="same", name="u_enc2_conv1")(u_p1)
    u_c2 = BatchNormalization(name="u_enc2_bn1")(u_c2)
    u_c2 = Activation("relu", name="u_enc2_relu1")(u_c2)
    u_c2 = Conv2D(unet_base_filters * 2, (3, 3), padding="same", name="u_enc2_conv2")(u_c2)
    u_c2 = BatchNormalization(name="u_enc2_bn2")(u_c2)
    u_c2 = Activation("relu", name="u_enc2_relu2")(u_c2)

    # Bottleneck
    u_p2 = MaxPooling2D((2, 2), name="u_pool2")(u_c2)
    u_b = Conv2D(unet_base_filters * 4, (3, 3), padding="same", name="u_bottleneck_conv")(u_p2)
    u_b = BatchNormalization(name="u_bottleneck_bn")(u_b)
    u_b = Activation("relu", name="u_bottleneck_relu")(u_b)

    # Decoder Level 2
    u_up2 = UpSampling2D((2, 2), name="u_up2")(u_b)
    u_cat2 = Concatenate(name="u_concat2")([u_up2, u_c2])
    u_d2 = Conv2D(unet_base_filters * 2, (3, 3), padding="same", name="u_dec2_conv")(u_cat2)
    u_d2 = BatchNormalization(name="u_dec2_bn")(u_d2)
    u_d2 = Activation("relu", name="u_dec2_relu")(u_d2)

    # Decoder Level 1
    u_up1 = UpSampling2D((2, 2), name="u_up1")(u_d2)
    u_cat1 = Concatenate(name="u_concat1")([u_up1, u_c1])
    u_d1 = Conv2D(unet_base_filters, (3, 3), padding="same", name="u_dec1_conv")(u_cat1)
    u_d1 = BatchNormalization(name="u_dec1_bn")(u_d1)
    u_unet_features = Activation("relu", name="u_unet_feature_out")(u_d1)

    # ==========================================
    # BRANCH 2: High-Frequency Residual DnCNN
    # ==========================================
    d_x = Conv2D(32, (3, 3), padding="same", name="dn_conv1")(inputs)
    d_x = Activation("relu", name="dn_relu1")(d_x)

    for i in range(2, dncnn_depth + 1):
        d_x = Conv2D(32, (3, 3), padding="same", name=f"dn_conv{i}")(d_x)
        d_x = BatchNormalization(name=f"dn_bn{i}")(d_x)
        d_x = Activation("relu", name=f"dn_relu{i}")(d_x)

    d_dncnn_features = d_x

    # ==========================================
    # CROSS-FEATURE FUSION & RESIDUAL OUTPUT
    # ==========================================
    # Concatenate representations from both branches at full resolution
    fusion_cat = Concatenate(name="hybrid_fusion_concat")([u_unet_features, d_dncnn_features])

    # 1x1 Convolution to fuse cross-branch feature representations
    fused = Conv2D(64, (1, 1), padding="same", name="fusion_1x1")(fusion_cat)
    fused = BatchNormalization(name="fusion_bn")(fused)
    fused = Activation("relu", name="fusion_relu")(fused)

    # Refinement block
    refined = Conv2D(32, (3, 3), padding="same", name="refine_conv")(fused)
    refined = Activation("relu", name="refine_relu")(refined)

    # Predict residual noise field R(y)
    estimated_noise = Conv2D(3, (3, 3), padding="same", name="hybrid_estimated_noise")(refined)

    # Residual subtraction: Clean = Input - EstimatedNoise
    denoised = Subtract(name="hybrid_residual_sub")([inputs, estimated_noise])
    outputs = Activation("sigmoid", name="denoised_output")(denoised)

    model = Model(inputs=inputs, outputs=outputs, name="hybrid_unet_dncnn_denoiser")
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="mean_squared_error",
        metrics=[psnr_metric, ssim_metric, "mae"],
    )
    return model
