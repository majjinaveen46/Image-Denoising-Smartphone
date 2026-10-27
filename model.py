import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Add, Activation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


@tf.keras.utils.register_keras_serializable()
def psnr_metric(y_true, y_pred):
    """Computes Peak Signal-to-Noise Ratio (PSNR) metric in dB."""
    return tf.image.psnr(y_true, y_pred, max_val=1.0)


@tf.keras.utils.register_keras_serializable()
def ssim_metric(y_true, y_pred):
    """Computes Structural Similarity Index Measure (SSIM) metric."""
    return tf.image.ssim(y_true, y_pred, max_val=1.0)


def build_model(input_shape=(128, 128, 3), learning_rate=0.001, model_type="standard"):
    """
    Builds and compiles an image denoising CNN model.

    Args:
        input_shape: Tuple representing image input shape (height, width, channels).
                     Use (128, 128, 3) for fixed size or (None, None, 3) for arbitrary sizes.
        learning_rate: Learning rate for the Adam optimizer.
        model_type: 'standard' (baseline 3-layer CNN) or 'residual' (residual skip connection).

    Returns:
        Compiled tf.keras.Model instance.
    """
    inputs = Input(shape=input_shape, name="noisy_input")

    if model_type == "residual":
        # Residual CNN architecture: learns the residual correction over the input
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv1")(inputs)
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv2")(x)
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv3")(x)
        residual = Conv2D(3, (3, 3), padding="same", name="residual_conv")(x)
        added = Add(name="residual_add")([inputs, residual])
        outputs = Activation("sigmoid", name="denoised_output")(added)
        model = Model(inputs=inputs, outputs=outputs, name="residual_denoiser")
    else:
        # Standard 3-layer convolutional autoencoder/denoiser
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv1")(inputs)
        x = Conv2D(64, (3, 3), activation="relu", padding="same", name="conv2")(x)
        outputs = Conv2D(3, (3, 3), activation="sigmoid", padding="same", name="denoised_output")(x)
        model = Model(inputs=inputs, outputs=outputs, name="standard_denoiser")

    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss="mean_squared_error",
        metrics=[psnr_metric, "mae"]
    )

    return model


if __name__ == "__main__":
    print("Building standard model:")
    std_model = build_model(model_type="standard")
    std_model.summary()

    print("\nBuilding residual model:")
    res_model = build_model(model_type="residual")
    res_model.summary()
