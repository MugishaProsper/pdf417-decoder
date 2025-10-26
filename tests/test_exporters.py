"""Tests for export module."""

import unittest
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import MagicMock
import tempfile
import os

from src.exporters import (
    TextExporter, JSONExporter, CSVExporter, XMLExporter,
    get_exporter, export_results
)


class TestExporters(unittest.TestCase):
    """Test cases for exporter classes."""
    
    def setUp(self):
        """Create test data."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock result data
        mock_rect = MagicMock()
        mock_rect.left = 10
        mock_rect.top = 20
        mock_rect.width = 100
        mock_rect.height = 50
        
        mock_point1 = MagicMock()
        mock_point1.x = 10
        mock_point1.y = 20
        
        mock_point2 = MagicMock()
        mock_point2.x = 110
        mock_point2.y = 70
        
        self.test_results = [{
            'data': 'TEST_DATA_123',
            'type': 'PDF417',
            'rect': mock_rect,
            'polygon': [mock_point1, mock_point2],
            'quality': 85,
            'preprocess_method': 'method_2'
        }]
        
        self.metadata = {
            'timestamp': '2025-11-08T10:00:00',
            'source': 'test.jpg'
        }
    
    def tearDown(self):
        """Clean up temp files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_text_exporter(self):
        """Test text export."""
        output_path = os.path.join(self.temp_dir, 'output.txt')
        exporter = TextExporter()
        exporter.export(self.test_results, output_path, self.metadata)
        
        self.assertTrue(os.path.exists(output_path))
        
        with open(output_path, 'r') as f:
            content = f.read()
            self.assertIn('TEST_DATA_123', content)
            self.assertIn('Barcode 1', content)
    
    def test_json_exporter(self):
        """Test JSON export."""
        output_path = os.path.join(self.temp_dir, 'output.json')
        exporter = JSONExporter()
        exporter.export(self.test_results, output_path, self.metadata)
        
        self.assertTrue(os.path.exists(output_path))
        
        with open(output_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['count'], 1)
            self.assertEqual(data['results'][0]['data'], 'TEST_DATA_123')
            self.assertEqual(data['results'][0]['quality'], 85)
    
    def test_csv_exporter(self):
        """Test CSV export."""
        output_path = os.path.join(self.temp_dir, 'output.csv')
        exporter = CSVExporter()
        exporter.export(self.test_results, output_path, self.metadata)
        
        self.assertTrue(os.path.exists(output_path))
        
        with open(output_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['data'], 'TEST_DATA_123')
            self.assertEqual(rows[0]['quality'], '85')
    
    def test_xml_exporter(self):
        """Test XML export."""
        output_path = os.path.join(self.temp_dir, 'output.xml')
        exporter = XMLExporter()
        exporter.export(self.test_results, output_path, self.metadata)
        
        self.assertTrue(os.path.exists(output_path))
        
        tree = ET.parse(output_path)
        root = tree.getroot()
        self.assertEqual(root.tag, 'pdf417_results')
        
        barcodes = root.find('barcodes')
        self.assertEqual(barcodes.get('count'), '1')
        
        barcode = barcodes.find('barcode')
        data = barcode.find('data')
        self.assertEqual(data.text, 'TEST_DATA_123')
    
    def test_get_exporter_valid(self):
        """Test getting valid exporter."""
        exporter = get_exporter('json')
        self.assertIsInstance(exporter, JSONExporter)
    
    def test_get_exporter_invalid(self):
        """Test getting invalid exporter raises error."""
        with self.assertRaises(ValueError):
            get_exporter('invalid_format')
    
    def test_export_results_function(self):
        """Test main export_results function."""
        output_path = os.path.join(self.temp_dir, 'output.json')
        export_results(self.test_results, output_path, 'json', self.metadata)
        
        self.assertTrue(os.path.exists(output_path))


if __name__ == "__main__":
    unittest.main()
