"""Tests for decoder module."""

import unittest
import os
from unittest.mock import patch, MagicMock
from src.decoder import decode_pdf417_from_image, _remove_duplicates


class TestDecoder(unittest.TestCase):
    """Test cases for decoder functions."""
    
    def test_file_not_found_raises_error(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        with self.assertRaises(FileNotFoundError):
            decode_pdf417_from_image("nonexistent_file.jpg")
    
    def test_remove_duplicates_removes_similar_results(self):
        """Test that duplicate results are removed."""
        mock_rect1 = MagicMock()
        mock_rect1.left = 10
        mock_rect1.top = 10
        
        mock_rect2 = MagicMock()
        mock_rect2.left = 15
        mock_rect2.top = 15
        
        results = [
            {'data': 'test', 'rect': mock_rect1},
            {'data': 'test', 'rect': mock_rect2},  # Duplicate
        ]
        
        unique = _remove_duplicates(results)
        self.assertEqual(len(unique), 1)
    
    def test_remove_duplicates_keeps_different_data(self):
        """Test that results with different data are kept."""
        mock_rect = MagicMock()
        mock_rect.left = 10
        mock_rect.top = 10
        
        results = [
            {'data': 'test1', 'rect': mock_rect},
            {'data': 'test2', 'rect': mock_rect},
        ]
        
        unique = _remove_duplicates(results)
        self.assertEqual(len(unique), 2)


if __name__ == "__main__":
    unittest.main()
