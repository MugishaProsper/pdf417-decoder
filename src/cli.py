"""Command-line interface for PDF417 decoder."""

import argparse
import sys
from typing import Optional

from .decoder import decode_pdf417_from_image


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
        help="Path to image file (JPG, PNG, etc.)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Save decoded data to file"
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

    try:
        results = decode_pdf417_from_image(
            parsed_args.image, 
            show_preview=parsed_args.show
        )

        if not results:
            print("❌ No PDF417 barcodes found.")
            return 1

        print(f"✅ Found {len(results)} PDF417 barcode(s):\n")

        output_lines = []
        for i, res in enumerate(results):
            print(f"--- Barcode {i+1} ---")
            
            if parsed_args.verbose:
                print(f"Preprocess: {res['preprocess_method']}")
                print(f"Position: {res['rect']}")
                print(f"Quality: {res['quality']}")
            
            print(f"Data ({len(res['data'])} chars):")
            print(res['data'])
            print()

            output_lines.append(f"--- Barcode {i+1} ---")
            output_lines.append(res['data'])
            output_lines.append("")

        # Save to file if requested
        if parsed_args.output:
            with open(parsed_args.output, 'w', encoding='utf-8') as f:
                f.write("\n".join(output_lines))
            print(f"💾 Saved to {parsed_args.output}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
