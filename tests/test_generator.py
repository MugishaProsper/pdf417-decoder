"""Tests for generator module."""

import unittest
import tempfile
import os
from pathlib import Path

from src.generator import BarcodeGenerator, generate_barcode, generate_barcode_from_file


class TestBarcodeGenerator(unittest.TestCase):
    """Test cases for barcode generator."""
    
    def setUp(self):
        """Create temporary directory for test outputs."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data = "TEST_BARCODE_DATA_123"
    
    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_generate_png(self):
        """Test PNG generation."""
        output_path = os.path.join(self.temp_dir, 'barcode.png')
        generator = BarcodeGenerator()
        
        result = generator.generate(self.test_data, output_path, format='png')
        
        self.assertTrue(os.path.exists(result))
        self.assertTrue(result.endswith('.png'))
    
    def test_generate_svg(self):
        """Test SVG generation."""
        output_path = os.path.join(self.temp_dir, 'barcode.svg')
        generator = BarcodeGenerator()
        
        result = generator.generate(self.test_data, output_path, format='svg')
        
        self.assertTrue(os.path.exists(result))
        self.assertTrue(result.endswith('.svg'))
        
        # Check SVG content
        with open(result, 'r') as f:
            content = f.read()
            self.assertIn('<svg', content)
    
    def test_generate_jpg(self):
        """Test JPG generation."""
        output_path = os.path.join(self.temp_dir, 'barcode.jpg')
        generator = BarcodeGenerator()
        
        result = generator.generate(self.test_data, output_path, format='jpg')
        
        self.assertTrue(os.path.exists(result))
        self.assertTrue(result.endswith('.jpg'))
    
    def test_error_correction_levels(self):
        """Test different error correction levels."""
        for level in ['low', 'medium', 'high', 'very_high']:
            output_path = os.path.join(self.temp_dir, f'barcode_{level}.png')
            generator = BarcodeGenerator(error_correction=level)
            
            result = generator.generate(self.test_data, output_path)
            
            self.assertTrue(os.path.exists(result))
    
    def test_generate_from_file(self):
        """Test generation from text file."""
        # Create input file
        input_path = os.path.join(self.temp_dir, 'input.txt')
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        output_path = os.path.join(self.temp_dir, 'barcode.png')
        generator = BarcodeGenerator()
        
        result = generator.generate_from_file(input_path, output_path)
        
        self.assertTrue(os.path.exists(result))
    
    def test_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        output_path = os.path.join(self.temp_dir, 'barcode.png')
        generator = BarcodeGenerator()
        
        with self.assertRaises(ValueError):
            generator.generate("", output_path)
    
    def test_invalid_format_raises_error(self):
        """Test that invalid format raises ValueError."""
        output_path = os.path.join(self.temp_dir, 'barcode.invalid')
        generator = BarcodeGenerator()
        
        with self.assertRaises(ValueError):
            generator.generate(self.test_data, output_path, format='invalid')
    
    def test_convenience_function(self):
        """Test convenience function."""
        output_path = os.path.join(self.temp_dir, 'barcode.png')
        
        result = generate_barcode(self.test_data, output_path)
        
        self.assertTrue(os.path.exists(result))
    
    def test_generate_from_file_convenience(self):
        """Test convenience function for file input."""
        # Create input file
        input_path = os.path.join(self.temp_dir, 'input.txt')
        with open(input_path, 'w') as f:
            f.write(self.test_data)
        
        output_path = os.path.join(self.temp_dir, 'barcode.png')
        
        result = generate_barcode_from_file(input_path, output_path)
        
        self.assertTrue(os.path.exists(result))
    
    def test_auto_extension_correction(self):
        """Test that file extension is automatically corrected."""
        output_path = os.path.join(self.temp_dir, 'barcode.wrong')
        generator = BarcodeGenerator()
        
        result = generator.generate(self.test_data, output_path, format='png')
        
        self.assertTrue(result.endswith('.png'))
        self.assertTrue(os.path.exists(result))


if __name__ == "__main__":
    unittest.main()
