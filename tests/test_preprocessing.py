"""Tests for image preprocessing module."""

import unittest
import numpy as np
import cv2
from src.preprocessing import preprocess_image


class TestPreprocessing(unittest.TestCase):
    """Test cases for preprocessing functions."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.test_image[25:75, 25:75] = [255, 255, 255]
    
    def test_preprocess_image_returns_list(self):
        """Test that preprocess_image returns a list."""
        result = preprocess_image(self.test_image)
        self.assertIsInstance(result, list)
    
    def test_preprocess_image_returns_multiple_versions(self):
        """Test that multiple preprocessing versions are returned."""
        result = preprocess_image(self.test_image)
        self.assertGreater(len(result), 1)
    
    def test_preprocess_image_includes_original(self):
        """Test that the first result is the original image."""
        result = preprocess_image(self.test_image)
        np.testing.assert_array_equal(result[0], self.test_image)
    
    def test_preprocess_image_creates_grayscale(self):
        """Test that grayscale version is created."""
        result = preprocess_image(self.test_image)
        # Second image should be grayscale (2D array)
        self.assertEqual(len(result[1].shape), 2)


if __name__ == "__main__":
    unittest.main()
