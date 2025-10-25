"""Core PDF417 barcode decoding functionality."""

import cv2
import os
import numpy as np
from typing import List, Dict, Optional
import time

try:
    import pyzbar.pyzbar as pyzbar
    PYZBAR_AVAILABLE = True
except (ImportError, FileNotFoundError):
    PYZBAR_AVAILABLE = False

from .preprocessing import preprocess_image
from .logger import get_logger

logger = get_logger(__name__)


def decode_pdf417_from_image(
    image_path: str, 
    show_preview: bool = False
) -> List[Dict]:
    """
    Decode all PDF417 barcodes in an image with robust preprocessing.
    
    Args:
        image_path: Path to the image file
        show_preview: Whether to display a preview window with detected barcodes
        
    Returns:
        List of decoded barcode data with metadata
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image cannot be loaded
        RuntimeError: If pyzbar is not available
    """
    if not PYZBAR_AVAILABLE:
        raise RuntimeError(
            "pyzbar library is not available. "
            "Please install it with: pip install pyzbar"
        )
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Load image with OpenCV
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")

    original = image.copy()
    results = []

    # Try multiple preprocessing versions
    processed_images = preprocess_image(image)

    for idx, proc in enumerate(processed_images):
        # Ensure 8-bit for pyzbar
        if proc.ndim == 3:
            proc_gray = cv2.cvtColor(proc, cv2.COLOR_BGR2GRAY)
        else:
            proc_gray = proc

        # Decode barcodes
        decoded_objects = pyzbar.decode(proc_gray, symbols=[pyzbar.ZBarSymbol.PDF417])

        for obj in decoded_objects:
            data = obj.data.decode('utf-8', errors='ignore')
            result = {
                'data': data,
                'type': obj.type,
                'rect': obj.rect,
                'polygon': obj.polygon,
                'quality': obj.quality,
                'preprocess_method': f"method_{idx}"
            }
            results.append(result)

            # Draw bounding box on original image
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(
                    np.array([point for point in points], dtype=np.float32)
                )
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = [(p.x, p.y) for p in points]

            cv2.polylines(original, [np.array(hull, np.int32)], True, (0, 255, 0), 3)
            cv2.putText(
                original, 
                f"PDF417 ({len(data)} chars)", 
                (obj.rect.left, obj.rect.top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, 
                (0, 255, 0), 
                2
            )

    # Remove duplicates (same data + similar position)
    unique_results = _remove_duplicates(results)

    # Show preview if requested
    if show_preview and unique_results:
        _show_preview(original)

    return unique_results


def _remove_duplicates(results: List[Dict]) -> List[Dict]:
    """Remove duplicate barcode detections based on data and position."""
    unique_results = []
    for res in results:
        is_duplicate = False
        for seen in unique_results:
            if (res['data'] == seen['data'] and
                abs(res['rect'].left - seen['rect'].left) < 20 and
                abs(res['rect'].top - seen['rect'].top) < 20):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_results.append(res)
    return unique_results


def _show_preview(image: np.ndarray) -> None:
    """Display preview window with detected barcodes."""
    display = cv2.resize(image, (800, 600))
    cv2.imshow('PDF417 Detected', display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
