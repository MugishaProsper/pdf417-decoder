"""Command-line interface for PDF417 decoder."""

import argparse
import sys
from typing import Optional
from pathlib import Path

from .decoder import decode_pdf417_from_image, decode_batch
from .exporters import export_results
from .logger import setup_logger, get_logger
from .cache import get_cache


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Powerful PDF417 Barcode Decoder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.jpg
  %(prog)s image.jpg --show
  %(prog)s image.jpg -o output.txt --verbose
        """
    )
    parser.add_argument(
        "image", 
        help="Path to image file or directory (JPG, PNG, etc.)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all images in directory (if image path is a directory)"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively process subdirectories in batch mode"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Save decoded data to file"
    )
    parser.add_argument(
        "-f", "--format",
        choices=['txt', 'json', 'csv', 'xml'],
        default='txt',
        help="Output format (default: txt)"
    )
    parser.add_argument(
        "--show", 
        action="store_true", 
        help="Show preview window with detected barcodes"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Print detailed information"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    parser.add_argument(
        "--log-level",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help="Set logging level (default: INFO)"
    )
    parser.add_argument(
        "--log-file",
        help="Path to log file (optional)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable result caching"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear all cached results and exit"
    )
    parser.add_argument(
        "--cache-stats",
        action="store_true",
        help="Show cache statistics and exit"
    )
    
    return parser.parse_args(args)


def main(args: Optional[list] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        args: Command-line arguments (for testing)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parsed_args = parse_args(args)
    
    # Setup logging
    logger = setup_logger(
        level=parsed_args.log_level,
        log_file=parsed_args.log_file,
        console=True
    )
    
    logger.debug(f"Starting PDF417 decoder with args: {parsed_args}")
    
    # Handle cache commands
    cache = get_cache()
    
    if parsed_args.clear_cache:
        count = cache.clear()
        print(f"✅ Cleared {count} cache entries")
        return 0
    
    if parsed_args.cache_stats:
        stats = cache.get_stats()
        print("📊 Cache Statistics:")
        print(f"   Total entries: {stats['total_entries']}")
        print(f"   Valid entries: {stats['valid_entries']}")
        print(f"   Expired entries: {stats['expired_entries']}")
        print(f"   Total size: {stats['total_size_mb']} MB")
        return 0

    try:
        # Check if batch mode
        input_path = Path(parsed_args.image)
        
        if parsed_args.batch or input_path.is_dir():
            # Batch processing mode
            logger.info(f"Starting batch processing: {parsed_args.image}")
            batch_results = decode_batch(
                str(input_path),
                recursive=parsed_args.recursive,
                show_preview=False  # Disable preview in batch mode
            )
            
            if not batch_results:
                logger.warning("No barcodes found in any images")
                print("❌ No PDF417 barcodes found in any images.")
                return 1
            
            # Display summary
            total_images = len(batch_results)
            total_barcodes = sum(len(r['results']) for r in batch_results)
            successful = sum(1 for r in batch_results if r['results'])
            
            logger.info(f"Batch complete: {total_barcodes} barcodes from {successful}/{total_images} images")
            print(f"\n✅ Batch Processing Complete:")
            print(f"   Images processed: {total_images}")
            print(f"   Images with barcodes: {successful}")
            print(f"   Total barcodes found: {total_barcodes}\n")
            
            # Display individual results
            for batch_result in batch_results:
                if batch_result['results']:
                    print(f"📄 {batch_result['image']}: {len(batch_result['results'])} barcode(s)")
                    if parsed_args.verbose:
                        for i, res in enumerate(batch_result['results'], 1):
                            print(f"   {i}. {res['data'][:50]}...")
            
            # Save to file if requested
            if parsed_args.output:
                logger.debug(f"Exporting batch results to {parsed_args.output}")
                metadata = {
                    'source': parsed_args.image,
                    'batch_mode': True,
                    'total_images': total_images,
                    'successful_images': successful,
                    'total_barcodes': total_barcodes
                }
                
                # Flatten results for export
                all_results = []
                for batch_result in batch_results:
                    for result in batch_result['results']:
                        result['source_image'] = batch_result['image']
                        all_results.append(result)
                
                export_results(
                    all_results,
                    parsed_args.output,
                    format_type=parsed_args.format,
                    metadata=metadata
                )
                logger.info(f"Batch results exported to {parsed_args.output}")
                print(f"💾 Saved to {parsed_args.output} ({parsed_args.format.upper()} format)")
        
        else:
            # Single image processing mode
            logger.info(f"Processing image: {parsed_args.image}")
            
            # Check cache first (unless disabled)
            results = None
            if not parsed_args.no_cache:
                results = cache.get(parsed_args.image)
                if results:
                    print("💾 Loaded from cache")
            
            # Decode if not cached
            if results is None:
                results = decode_pdf417_from_image(
                    parsed_args.image, 
                    show_preview=parsed_args.show
                )
                
                # Cache results (unless disabled)
                if not parsed_args.no_cache and results:
                    cache.set(parsed_args.image, results)

            if not results:
                logger.warning("No PDF417 barcodes found in image")
                print("❌ No PDF417 barcodes found.")
                return 1

            logger.info(f"Successfully decoded {len(results)} barcode(s)")
            print(f"✅ Found {len(results)} PDF417 barcode(s):\n")

            # Display results to console
            for i, res in enumerate(results):
                print(f"--- Barcode {i+1} ---")
                
                if parsed_args.verbose:
                    print(f"Preprocess: {res['preprocess_method']}")
                    print(f"Position: {res['rect']}")
                    print(f"Quality: {res['quality']}")
                
                print(f"Data ({len(res['data'])} chars):")
                print(res['data'])
                print()

            # Save to file if requested
            if parsed_args.output:
                logger.debug(f"Exporting results to {parsed_args.output} as {parsed_args.format}")
                metadata = {
                    'source': parsed_args.image,
                    'verbose': parsed_args.verbose,
                    'format': parsed_args.format
                }
                
                export_results(
                    results, 
                    parsed_args.output, 
                    format_type=parsed_args.format,
                    metadata=metadata
                )
                logger.info(f"Results exported to {parsed_args.output}")
                print(f"💾 Saved to {parsed_args.output} ({parsed_args.format.upper()} format)")

        return 0

    except Exception as e:
        logger.error(f"Error processing image: {e}", exc_info=parsed_args.verbose)
        print(f"❌ Error: {e}", file=sys.stderr)
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
