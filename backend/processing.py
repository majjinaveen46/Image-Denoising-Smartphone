import io
import os
import uuid
import base64
from typing import Tuple, Optional
from PIL import Image, ImageOps
import numpy as np

# Configurable security constraints
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 Megabytes
ALLOWED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}


class ImageValidationError(Exception):
    """Custom exception for image validation failures."""
    pass


def validate_and_decode_upload(file_bytes: bytes, filename: str) -> Image.Image:
    """
    Validates uploaded file payload securely:
    - Verifies byte length doesn't exceed MAX_FILE_SIZE_BYTES.
    - Inspects image headers via PIL rather than trusting client MIME or extension.
    - Ensures format is supported.
    - Transposes smartphone EXIF orientation.
    - Converts to standard 3-channel RGB.
    """
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ImageValidationError(
            f"File exceeds maximum allowed size of {MAX_FILE_SIZE_BYTES / (1024*1024):.1f} MB."
        )

    if len(file_bytes) == 0:
        raise ImageValidationError("Uploaded file is empty.")

    try:
        pil_img = Image.open(io.BytesIO(file_bytes))
        pil_img.verify()  # Verifies file integrity and format headers
    except Exception as e:
        raise ImageValidationError(f"Invalid or corrupted image format: {str(e)}")

    # Re-open after verify() (PIL requires re-opening after verify)
    pil_img = Image.open(io.BytesIO(file_bytes))

    format_upper = (pil_img.format or "").upper()
    if format_upper not in ALLOWED_FORMATS:
        raise ImageValidationError(
            f"Unsupported format '{format_upper}'. Allowed formats: {', '.join(sorted(ALLOWED_FORMATS))}."
        )

    # Smartphone EXIF orientation normalization
    try:
        pil_img = ImageOps.exif_transpose(pil_img)
    except Exception:
        pass

    # Convert to standard RGB (strips any alpha/palette channels safely)
    return pil_img.convert("RGB")


def image_to_base64_data_uri(pil_img: Image.Image, format: str = "PNG") -> str:
    """
    Converts a PIL Image to a Base64 Data URI for instant browser rendering.
    """
    buffered = io.BytesIO()
    fmt = "PNG" if format.upper() == "PNG" else "JPEG"
    if fmt == "JPEG":
        pil_img.save(buffered, format=fmt, quality=95)
        mime = "image/jpeg"
    else:
        pil_img.save(buffered, format=fmt, optimize=True)
        mime = "image/png"

    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:{mime};base64,{img_b64}"


def image_to_bytes(pil_img: Image.Image, format: str = "PNG") -> bytes:
    """
    Converts a PIL Image to raw bytes for direct binary file downloads.
    """
    buffered = io.BytesIO()
    fmt = "PNG" if format.upper() == "PNG" else "JPEG"
    if fmt == "JPEG":
        pil_img.save(buffered, format=fmt, quality=95)
    else:
        pil_img.save(buffered, format=fmt)
    return buffered.getvalue()
