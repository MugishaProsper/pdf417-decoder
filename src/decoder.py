"""Core PDF417 barcode decoding functionality."""

import cv2
import os
import numpy as np
from typing import List, Dict, Optional
import time
from pathlib import Path

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
    start_time = time.time()
    
    if not PYZBAR_AVAILABLE:
        logger.error("pyzbar library is not available")
        raise RuntimeError(
            "pyzbar library is not available. "
            "Please install it with: pip install pyzbar"
        )
    
    if not os.path.exists(image_path):
        logger.error(f"Image file not found: {image_path}")
        raise FileNotFoundError(f"Image not found: {image_path}")

    logger.debug(f"Loading image: {image_path}")
    # Load image with OpenCV
    image = cv2.imread(image_path)
    if image is None:
        logger.error(f"Failed to load image: {image_path}")
        raise ValueError(f"Could not load image: {image_path}")

    logger.debug(f"Image loaded successfully: {image.shape}")
    original = image.copy()
    results = []

    # Try multiple preprocessing versions
    logger.debug("Starting preprocessing")
    processed_images = preprocess_image(image)
    logger.debug(f"Generated {len(processed_images)} preprocessed versions")

    for idx, proc in enumerate(processed_images):
        logger.debug(f"Trying preprocessing method {idx}")
        # Ensure 8-bit for pyzbar
        if proc.ndim == 3:
            proc_gray = cv2.cvtColor(proc, cv2.COLOR_BGR2GRAY)
        else:
            proc_gray = proc

        # Decode barcodes
        decoded_objects = pyzbar.decode(proc_gray, symbols=[pyzbar.ZBarSymbol.PDF417])
        
        if decoded_objects:
            logger.debug(f"Method {idx} found {len(decoded_objects)} barcode(s)")

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
    logger.debug(f"Found {len(results)} total results before deduplication")
    unique_results = _remove_duplicates(results)
    logger.debug(f"After deduplication: {len(unique_results)} unique results")
    
    elapsed_time = time.time() - start_time
    logger.info(f"Decoding completed in {elapsed_time:.3f}s - found {len(unique_results)} barcode(s)")

    # Show preview if requested
    if show_preview and unique_results:
        logger.debug("Showing preview window")
        _show_preview(original)

    return unique_results


def decode_batch(
    directory_path: str,
    recursive: bool = False,
    show_preview: bool = False,
    image_extensions: tuple = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'),
    workers: Optional[int] = None,
    use_parallel: bool = False
) -> List[Dict]:
    """
    Decode PDF417 barcodes from multiple images in a directory.
    
    Args:
        directory_path: Path to directory containing images
        recursive: Whether to search subdirectories recursively
        show_preview: Whether to show preview (disabled in batch mode)
        image_extensions: Tuple of valid image file extensions
        workers: Number of parallel workers (None = CPU count)
        use_parallel: Whether to use parallel processing
        
    Returns:
        List of dictionaries containing image path and results
    """
    logger.info(f"Starting batch processing in: {directory_path} (parallel={use_parallel})")
    
    directory = Path(directory_path)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")
    
    # Find all image files
    if recursive:
        image_files = []
        for ext in image_extensions:
            image_files.extend(directory.rglob(f"*{ext}"))
            image_files.extend(directory.rglob(f"*{ext.upper()}"))
    else:
        image_files = []
        for ext in image_extensions:
            image_files.extend(directory.glob(f"*{ext}"))
            image_files.extend(directory.glob(f"*{ext.upper()}"))
    
    image_files = sorted(set(image_files))  # Remove duplicates and sort
    logger.info(f"Found {len(image_files)} image files to process")
    
    if not image_files:
        logger.warning("No image files found in directory")
        return []
    
    # Use parallel processing if requested and beneficial
    if use_parallel and len(image_files) > 1:
        return _decode_batch_parallel(image_files, workers)
    else:
        return _decode_batch_sequential(image_files)


def _decode_batch_sequential(image_files: List[Path]) -> List[Dict]:
    """Process images sequentially."""
    batch_results = []
    
    try:
        # Try to import tqdm for progress bar
        from tqdm import tqdm
        iterator = tqdm(image_files, desc="Processing images", unit="img")
    except ImportError:
        logger.debug("tqdm not available, using simple progress")
        iterator = image_files
    
    for i, image_file in enumerate(iterator, 1):
        try:
            logger.debug(f"Processing {image_file}")
            results = decode_pdf417_from_image(str(image_file), show_preview=False)
            
            batch_results.append({
                'image': str(image_file),
                'results': results,
                'success': len(results) > 0,
                'error': None
            })
            
            if not isinstance(iterator, list):  # If using tqdm
                iterator.set_postfix({'found': len(results)})
            else:
                # Simple progress without tqdm
                if i % 10 == 0 or i == len(image_files):
                    logger.info(f"Progress: {i}/{len(image_files)} images processed")
                    
        except Exception as e:
            logger.warning(f"Error processing {image_file}: {e}")
            batch_results.append({
                'image': str(image_file),
                'results': [],
                'success': False,
                'error': str(e)
            })
    
    successful = sum(1 for r in batch_results if r['success'])
    total_barcodes = sum(len(r['results']) for r in batch_results)
    logger.info(f"Batch complete: {total_barcodes} barcodes from {successful}/{len(image_files)} images")
    
    return batch_results


def _decode_batch_parallel(image_files: List[Path], workers: Optional[int] = None) -> List[Dict]:
    """Process images in parallel using multiprocessing."""
    import multiprocessing as mp
    from functools import partial
    
    if workers is None:
        workers = mp.cpu_count()
    
    logger.info(f"Using parallel processing with {workers} workers")
    
    # Create a pool of workers
    with mp.Pool(processes=workers) as pool:
        try:
            # Try to import tqdm for progress bar
            from tqdm import tqdm
            
            # Process images in parallel with progress bar
            batch_results = list(tqdm(
                pool.imap(_process_single_image, [str(f) for f in image_files]),
                total=len(image_files),
                desc="Processing images (parallel)",
                unit="img"
            ))
        except ImportError:
            # No tqdm, process without progress bar
            logger.debug("tqdm not available, processing without progress bar")
            batch_results = pool.map(_process_single_image, [str(f) for f in image_files])
    
    successful = sum(1 for r in batch_results if r['success'])
    total_barcodes = sum(len(r['results']) for r in batch_results)
    logger.info(f"Parallel batch complete: {total_barcodes} barcodes from {successful}/{len(image_files)} images")
    
    return batch_results


def _process_single_image(image_path: str) -> Dict:
    """
    Process a single image (for parallel processing).
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary with results
    """
    try:
        results = decode_pdf417_from_image(image_path, show_preview=False)
        return {
            'image': image_path,
            'results': results,
            'success': len(results) > 0,
            'error': None
        }
    except Exception as e:
        return {
            'image': image_path,
            'results': [],
            'success': False,
            'error': str(e)
        }


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
