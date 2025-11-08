"""Command-line interface for PDF417 decoder."""

import argparse
import sys
from typing import Optional
from pathlib import Path

from .decoder import decode_pdf417_from_image, decode_batch
from .exporters import export_results
from .logger import setup_logger, get_logger
from .cache import get_cache
from .config import load_config
from .quality_analyzer import analyze_image_quality
from .generator import generate_barcode, generate_barcode_from_file


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Powerful PDF417 Barcode Decoder & Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Decode
  %(prog)s decode image.jpg
  %(prog)s decode image.jpg --show
  %(prog)s decode photos/ --batch
  
  # Generate
  %(prog)s generate "Hello World" -o barcode.png
  %(prog)s generate --input data.txt -o barcode.svg --format svg
  
  # API Server
  %(prog)s --serve
        """
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Decode subcommand (default behavior)
    decode_parser = subparsers.add_parser('decode', help='Decode PDF417 barcodes')
    decode_parser.add_argument(
        "image", 
        help="Path to image file or directory (JPG, PNG, etc.)"
    )
    decode_parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all images in directory (if image path is a directory)"
    )
    decode_parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively process subdirectories in batch mode"
    )
    decode_parser.add_argument(
        "-o", "--output", 
        help="Save decoded data to file"
    )
    decode_parser.add_argument(
        "-f", "--format",
        choices=['txt', 'json', 'csv', 'xml'],
        default='txt',
        help="Output format (default: txt)"
    )
    decode_parser.add_argument(
        "--show", 
        action="store_true", 
        help="Show preview window with detected barcodes"
    )
    decode_parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Print detailed information"
    )
    decode_parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze image quality and provide recommendations"
    )
    
    # Generate subcommand
    gen_parser = subparsers.add_parser('generate', help='Generate PDF417 barcodes')
    gen_parser.add_argument(
        "data",
        nargs='?',
        help="Data to encode in barcode"
    )
    gen_parser.add_argument(
        "-i", "--input",
        help="Read data from text file"
    )
    gen_parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output file path"
    )
    gen_parser.add_argument(
        "-f", "--format",
        choices=['png', 'jpg', 'bmp', 'svg'],
        default='png',
        help="Output format (default: png)"
    )
    gen_parser.add_argument(
        "--error-correction",
        choices=['low', 'medium', 'high', 'very_high'],
        default='medium',
        help="Error correction level (default: medium)"
    )
    gen_parser.add_argument(
        "--scale",
        type=int,
        default=3,
        help="Scale factor for barcode size (default: 3)"
    )
    gen_parser.add_argument(
        "--ratio",
        type=int,
        default=3,
        help="Aspect ratio (default: 3)"
    )
    gen_parser.add_argument(
        "--columns",
        type=int,
        help="Number of data columns (1-30, default: auto)"
    )
    
    # For backward compatibility, also accept image as first positional arg
    parser.add_argument(
        "image",
        nargs='?',
        help="Path to image file or directory (for decode mode)"
    )
    parser.add_argument(
        "image", 
        help="Path to image file or directory (JPG, PNG, etc.)"
    )
    # Global arguments (for backward compatibility)
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all images in directory"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively process subdirectories"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output file path"
    )
    parser.add_argument(
        "-f", "--format",
        help="Output format"
    )
    parser.add_argument(
        "--show", 
        action="store_true", 
        help="Show preview window"
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
    parser.add_argument(
        "--config",
        help="Path to configuration file (YAML or JSON)"
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze image quality and provide recommendations"
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start REST API server"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API server port (default: 8000)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="API server host (default: 0.0.0.0)"
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
    
    # Load configuration
    config = load_config(parsed_args.config)
    
    # Apply config defaults if not specified in CLI
    log_level = parsed_args.log_level or config.get('logging.level', 'INFO')
    log_file = parsed_args.log_file or config.get('logging.file')
    
    # Setup logging
    logger = setup_logger(
        level=log_level,
        log_file=log_file,
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
    
    # Handle API server
    if parsed_args.serve:
        try:
            from src.api.server import start_server
            print(f"🚀 Starting PDF417 Decoder API server...")
            print(f"   Host: {parsed_args.host}")
            print(f"   Port: {parsed_args.port}")
            print(f"   Docs: http://{parsed_args.host}:{parsed_args.port}/docs")
            print(f"   Health: http://{parsed_args.host}:{parsed_args.port}/health")
            print()
            start_server(host=parsed_args.host, port=parsed_args.port, reload=False)
            return 0
        except ImportError as e:
            logger.error(f"API dependencies not installed: {e}")
            print("❌ Error: API dependencies not installed")
            print("Install with: pip install fastapi uvicorn[standard] python-multipart")
            return 1
        except Exception as e:
            logger.error(f"Error starting API server: {e}")
            print(f"❌ Error: {e}", file=sys.stderr)
            return 1
    
    # Handle quality analysis
    if parsed_args.analyze:
        try:
            print("🔍 Analyzing image quality...\n")
            analysis = analyze_image_quality(parsed_args.image)
            
            print(f"Overall Quality: {analysis['overall_quality'].upper()} ({analysis['overall_score']:.2f}/1.0)\n")
            
            print("Detailed Analysis:")
            print(f"  • {analysis['resolution']['message']}")
            print(f"  • {analysis['contrast']['message']}")
            print(f"  • {analysis['sharpness']['message']}")
            print(f"  • {analysis['noise']['message']}")
            print(f"  • {analysis['brightness']['message']}")
            
            if analysis['issues']:
                print(f"\n⚠️  Issues Detected:")
                for issue in analysis['issues']:
                    print(f"  • {issue}")
            
            print(f"\n💡 Recommendations:")
            for rec in analysis['recommendations']:
                print(f"  • {rec}")
            
            return 0
        except Exception as e:
            logger.error(f"Error analyzing image quality: {e}")
            print(f"❌ Error: {e}", file=sys.stderr)
            return 1

    try:
        # Handle generate command
        if parsed_args.command == 'generate':
            logger.info("Starting barcode generation")
            
            # Get data from argument or file
            if parsed_args.input:
                logger.debug(f"Reading data from file: {parsed_args.input}")
                output_path = generate_barcode_from_file(
                    input_path=parsed_args.input,
                    output_path=parsed_args.output,
                    format=parsed_args.format,
                    error_correction=parsed_args.error_correction,
                    scale=parsed_args.scale,
                    ratio=parsed_args.ratio
                )
            elif parsed_args.data:
                logger.debug(f"Generating barcode from string: {len(parsed_args.data)} chars")
                output_path = generate_barcode(
                    data=parsed_args.data,
                    output_path=parsed_args.output,
                    format=parsed_args.format,
                    error_correction=parsed_args.error_correction,
                    scale=parsed_args.scale,
                    ratio=parsed_args.ratio,
                    columns=parsed_args.columns
                )
            else:
                logger.error("No data provided for generation")
                print("❌ Error: Provide data via argument or --input file")
                return 1
            
            logger.info(f"Barcode generated successfully: {output_path}")
            print(f"✅ Barcode generated successfully!")
            print(f"   Output: {output_path}")
            print(f"   Format: {parsed_args.format.upper()}")
            print(f"   Error Correction: {parsed_args.error_correction}")
            print(f"   Data Length: {len(parsed_args.data or 'file')} characters")
            return 0
        
        # Handle decode command (default)
        # For backward compatibility, use image arg if no command specified
        image_path = parsed_args.image if parsed_args.command != 'decode' else getattr(parsed_args, 'image', None)
        if parsed_args.command == 'decode':
            image_path = parsed_args.image
        
        if not image_path:
            logger.error("No image path provided")
            print("❌ Error: Provide image path or use 'generate' command")
            print("Run with --help for usage information")
            return 1
        
        # Check if batch mode
        input_path = Path(image_path)
        
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
