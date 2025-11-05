"""Image preprocessing utilities for barcode detection."""

import cv2
import numpy as np
from typing import List


def preprocess_image(image: np.ndarray) -> List[np.ndarray]:
    """
    Apply multiple preprocessing techniques to improve detection.
    
    Args:
        image: Input image as numpy array
        
    Returns:
        List of processed images to try for barcode detection
    """
    processed = []

    # 1. Original
    processed.append(image)

    # 2. Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed.append(gray)

    # 3. Binary threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    processed.append(binary)

    # 4. Inverted binary
    inverted = cv2.bitwise_not(binary)
    processed.append(inverted)

    # 5. Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    processed.append(adaptive)

    # 6. Morphological operations (close gaps)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    processed.append(morph)

    # 7. Sharpened
    sharpened = cv2.filter2D(gray, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
    processed.append(sharpened)

    return processed
