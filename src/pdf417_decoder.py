import cv2
import pyzbar.pyzbar as pyzbar
import argparse
import os
from PIL import Image
import numpy as np
from typing import List, Tuple, Optional


def preprocess_image(image: np.ndarray) -> List[np.ndarray]:
    """
    Apply multiple preprocessing techniques to improve detection.
    Returns a list of processed images to try.
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
    sharpened = cv2.filter2D(gray, -1, np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]))
    processed.append(sharpened)

    return processed


def decode_pdf417_from_image(image_path: str, show_preview: bool = False) -> List[dict]:
    """
    Decode all PDF417 barcodes in an image with robust preprocessing.
    Returns list of decoded data with metadata.
    """
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
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = [(p.x, p.y) for p in points]

            cv2.polylines(original, [np.array(hull, np.int32)], True, (0, 255, 0), 3)
            cv2.putText(original, f"PDF417 ({len(data)} chars)", 
                        (obj.rect.left, obj.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Remove duplicates (same data + similar position)
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

    # Show preview if requested
    if show_preview and unique_results:
        display = cv2.resize(original, (800, 600))
        cv2.imshow('PDF417 Detected', display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return unique_results


def main():
    parser = argparse.ArgumentParser(description="Powerful PDF417 Barcode Decoder")
    parser.add_argument("image", help="Path to image file (JPG, PNG, etc.)")
    parser.add_argument("-o", "--output", help="Save decoded data to file")
    parser.add_argument("--show", action="store_true", help="Show preview window")
    parser.add_argument("--verbose", action="store_true", help="Print detailed info")

    args = parser.parse_args()

    try:
        results = decode_pdf417_from_image(args.image, show_preview=args.show)

        if not results:
            print("❌ No PDF417 barcodes found.")
            return

        print(f"✅ Found {len(results)} PDF417 barcode(s):\n")

        output_lines = []
        for i, res in enumerate(results):
            print(f"--- Barcode {i+1} ---")
            print(f"Preprocess: {res['preprocess_method']}")
            print(f"Position: {res['rect']}")
            print(f"Data ({len(res['data'])} chars):")
            print(res['data'])
            print()

            output_lines.append(f"--- Barcode {i+1} ---")
            output_lines.append(res['data'])
            output_lines.append("")

        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write("\n".join(output_lines))
            print(f"💾 Saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()