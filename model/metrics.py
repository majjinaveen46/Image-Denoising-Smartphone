import numpy as np
import tensorflow as tf


@tf.keras.utils.register_keras_serializable(package="ImageDenoising")
def psnr_metric(y_true, y_pred):
    """
    Computes Peak Signal-to-Noise Ratio (PSNR) in dB between target and prediction.
    Assumes inputs are normalized to the [0, 1] range.
    """
    y_pred_clipped = tf.clip_by_value(y_pred, 0.0, 1.0)
    return tf.image.psnr(y_true, y_pred_clipped, max_val=1.0)


@tf.keras.utils.register_keras_serializable(package="ImageDenoising")
def ssim_metric(y_true, y_pred):
    """
    Computes Structural Similarity Index (SSIM) between target and prediction.
    Assumes inputs are normalized to the [0, 1] range.
    """
    y_pred_clipped = tf.clip_by_value(y_pred, 0.0, 1.0)
    return tf.image.ssim(y_true, y_pred_clipped, max_val=1.0)


def compute_psnr_np(clean: np.ndarray, test: np.ndarray) -> float:
    """
    Computes PSNR between two float32 images in [0, 1] using NumPy.
    """
    clean_f = clean.astype(np.float64)
    test_f = test.astype(np.float64)
    mse = np.mean((clean_f - test_f) ** 2)
    if mse <= 1e-12:
        return 100.0
    return float(20.0 * np.log10(1.0 / np.sqrt(mse)))


def compute_ssim_np(clean: np.ndarray, test: np.ndarray) -> float:
    """
    Computes SSIM between two images using TensorFlow backend.
    """
    c_t = tf.convert_to_tensor(clean[np.newaxis, ...], dtype=tf.float32)
    t_t = tf.convert_to_tensor(test[np.newaxis, ...], dtype=tf.float32)
    return float(tf.image.ssim(c_t, t_t, max_val=1.0).numpy()[0])


def estimate_noise_sigma(image_np: np.ndarray) -> float:
    """
    Blind noise standard deviation estimator using high-pass Laplacian filter.
    Useful for reporting estimated noise level on unlabelled user smartphone uploads.
    Returns estimated noise sigma on a [0, 255] scale.
    """
    if image_np.ndim == 3:
        # Convert RGB to grayscale luminance
        gray = 0.2989 * image_np[:, :, 0] + 0.5870 * image_np[:, :, 1] + 0.1140 * image_np[:, :, 2]
    else:
        gray = image_np.copy()

    # If normalized to [0, 1], scale to [0, 255]
    if gray.max() <= 1.0:
        gray = gray * 255.0

    H, W = gray.shape
    # 3x3 Laplacian operator kernel
    laplacian = np.array([[1, -2, 1],
                          [-2, 4, -2],
                          [1, -2, 1]], dtype=np.float64)

    # Convolve with valid padding using vectorized numpy operations
    sub = (
        gray[0:H-2, 0:W-2] - 2 * gray[0:H-2, 1:W-1] + gray[0:H-2, 2:W]
        - 2 * gray[1:H-1, 0:W-2] + 4 * gray[1:H-1, 1:W-1] - 2 * gray[1:H-1, 2:W]
        + gray[2:H, 0:W-2] - 2 * gray[2:H, 1:W-1] + gray[2:H, 2:W]
    )
    # Estimate standard deviation of noise: sigma = sqrt(pi/2) * (1 / (6 * (W-2)*(H-2))) * sum(|sub|)
    sigma = np.sum(np.abs(sub)) * np.sqrt(0.5 * np.pi) / (6.0 * (W - 2) * (H - 2))
    return float(np.round(sigma, 2))
