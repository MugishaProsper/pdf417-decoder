"""PDF417 barcode generation functionality."""

import os
from pathlib import Path
from typing import Optional, Union
from PIL import Image
import pdf417gen

from .logger import get_logger

logger = get_logger(__name__)


class BarcodeGenerator:
    """Generate PDF417 barcodes."""
    
    # Error correction levels
    ERROR_CORRECTION_LEVELS = {
        'low': 0,      # ~3% error correction
        'medium': 3,   # ~15% error correction
        'high': 5,     # ~25% error correction
        'very_high': 7 # ~40% error correction
    }
    
    def __init__(
        self,
        error_correction: str = 'medium',
        columns: Optional[int] = None,
        security_level: Optional[int] = None
    ):
        """
        Initialize barcode generator.
        
        Args:
            error_correction: Error correction level (low, medium, high, very_high)
            columns: Number of data columns (1-30, None for auto)
            security_level: Security level (0-8, None for auto)
        """
        self.error_correction = self.ERROR_CORRECTION_LEVELS.get(
            error_correction.lower(), 
            3
        )
        self.columns = columns
        self.security_level = security_level or self.error_correction
        
        logger.debug(
            f"Generator initialized: error_correction={error_correction}, "
            f"columns={columns}, security_level={self.security_level}"
        )
    
    def generate(
        self,
        data: str,
        output_path: str,
        format: str = 'png',
        scale: int = 3,
        ratio: int = 3
    ) -> str:
        """
        Generate PDF417 barcode and save to file.
        
        Args:
            data: Data to encode in barcode
            output_path: Path to save barcode image
            format: Output format (png, jpg, bmp, svg)
            scale: Scale factor for barcode size
            ratio: Aspect ratio (height/width of modules)
            
        Returns:
            Path to generated barcode file
            
        Raises:
            ValueError: If data is empty or format is invalid
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        format = format.lower()
        if format not in ['png', 'jpg', 'jpeg', 'bmp', 'svg']:
            raise ValueError(f"Unsupported format: {format}. Use png, jpg, bmp, or svg")
        
        logger.info(f"Generating PDF417 barcode: {len(data)} characters")
        
        try:
            # Generate barcode codes
            codes = pdf417gen.encode(
                data,
                columns=self.columns or 6,
                security_level=self.security_level
            )
            
            if format == 'svg':
                # Generate SVG
                svg_data = pdf417gen.render_svg(
                    codes,
                    scale=scale,
                    ratio=ratio
                )
                
                # Save SVG
                output_path = self._ensure_extension(output_path, 'svg')
                with open(output_path, 'w') as f:
                    f.write(svg_data)
            else:
                # Generate image
                image = pdf417gen.render_image(
                    codes,
                    scale=scale,
                    ratio=ratio
                )
                
                # Save image
                output_path = self._ensure_extension(output_path, format)
                image.save(output_path, format.upper())
            
            logger.info(f"Barcode saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating barcode: {e}")
            raise
    
    def generate_from_file(
        self,
        input_path: str,
        output_path: str,
        format: str = 'png',
        scale: int = 3,
        ratio: int = 3
    ) -> str:
        """
        Generate PDF417 barcode from text file.
        
        Args:
            input_path: Path to text file containing data
            output_path: Path to save barcode image
            format: Output format (png, jpg, bmp, svg)
            scale: Scale factor for barcode size
            ratio: Aspect ratio
            
        Returns:
            Path to generated barcode file
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        logger.debug(f"Reading data from: {input_path}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = f.read()
        
        return self.generate(data, output_path, format, scale, ratio)
    
    def _ensure_extension(self, path: str, extension: str) -> str:
        """Ensure file has correct extension."""
        path_obj = Path(path)
        
        if path_obj.suffix.lower() != f'.{extension}':
            path = str(path_obj.with_suffix(f'.{extension}'))
        
        return path


def generate_barcode(
    data: str,
    output_path: str,
    format: str = 'png',
    error_correction: str = 'medium',
    scale: int = 3,
    ratio: int = 3,
    columns: Optional[int] = None
) -> str:
    """
    Generate PDF417 barcode (convenience function).
    
    Args:
        data: Data to encode
        output_path: Output file path
        format: Output format (png, jpg, bmp, svg)
        error_correction: Error correction level (low, medium, high, very_high)
        scale: Scale factor
        ratio: Aspect ratio
        columns: Number of columns (None for auto)
        
    Returns:
        Path to generated barcode
    """
    generator = BarcodeGenerator(
        error_correction=error_correction,
        columns=columns
    )
    
    return generator.generate(
        data=data,
        output_path=output_path,
        format=format,
        scale=scale,
        ratio=ratio
    )


def generate_barcode_from_file(
    input_path: str,
    output_path: str,
    format: str = 'png',
    error_correction: str = 'medium',
    scale: int = 3,
    ratio: int = 3
) -> str:
    """
    Generate PDF417 barcode from text file (convenience function).
    
    Args:
        input_path: Input text file path
        output_path: Output file path
        format: Output format (png, jpg, bmp, svg)
        error_correction: Error correction level
        scale: Scale factor
        ratio: Aspect ratio
        
    Returns:
        Path to generated barcode
    """
    generator = BarcodeGenerator(error_correction=error_correction)
    
    return generator.generate_from_file(
        input_path=input_path,
        output_path=output_path,
        format=format,
        scale=scale,
        ratio=ratio
    )
