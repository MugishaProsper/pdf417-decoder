"""Tests for cache module."""

import unittest
import tempfile
import shutil
import time
from pathlib import Path
from unittest.mock import MagicMock

from src.cache import BarcodeCache, get_cache


class TestBarcodeCache(unittest.TestCase):
    """Test cases for BarcodeCache."""
    
    def setUp(self):
        """Create temporary cache directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = BarcodeCache(cache_dir=self.temp_dir, ttl_seconds=2)
        
        # Create a temporary test image
        self.test_image = Path(self.temp_dir) / "test.jpg"
        self.test_image.write_bytes(b"fake image data")
        
        # Mock result data
        mock_rect = MagicMock()
        mock_rect.left = 10
        mock_rect.top = 20
        mock_rect.width = 100
        mock_rect.height = 50
        
        mock_point = MagicMock()
        mock_point.x = 10
        mock_point.y = 20
        
        self.test_results = [{
            'data': 'TEST_DATA',
            'type': 'PDF417',
            'rect': mock_rect,
            'polygon': [mock_point],
            'quality': 85,
            'preprocess_method': 'method_2'
        }]
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_cache_directory_created(self):
        """Test that cache directory is created."""
        self.assertTrue(Path(self.temp_dir).exists())
    
    def test_set_and_get(self):
        """Test caching and retrieving results."""
        # Cache results
        self.cache.set(str(self.test_image), self.test_results)
        
        # Retrieve from cache
        cached_results = self.cache.get(str(self.test_image))
        
        self.assertIsNotNone(cached_results)
        self.assertEqual(len(cached_results), 1)
        self.assertEqual(cached_results[0]['data'], 'TEST_DATA')
        self.assertEqual(cached_results[0]['quality'], 85)
    
    def test_cache_miss(self):
        """Test cache miss for non-existent file."""
        nonexistent = Path(self.temp_dir) / "nonexistent.jpg"
        nonexistent.write_bytes(b"different data")
        
        result = self.cache.get(str(nonexistent))
        self.assertIsNone(result)
    
    def test_cache_expiration(self):
        """Test that cache expires after TTL."""
        # Cache results
        self.cache.set(str(self.test_image), self.test_results)
        
        # Should be cached
        cached = self.cache.get(str(self.test_image))
        self.assertIsNotNone(cached)
        
        # Wait for expiration
        time.sleep(2.5)
        
        # Should be expired
        cached = self.cache.get(str(self.test_image))
        self.assertIsNone(cached)
    
    def test_clear_cache(self):
        """Test clearing all cache entries."""
        # Cache some results
        self.cache.set(str(self.test_image), self.test_results)
        
        # Clear cache
        count = self.cache.clear()
        
        self.assertGreater(count, 0)
        
        # Should not be cached anymore
        cached = self.cache.get(str(self.test_image))
        self.assertIsNone(cached)
    
    def test_get_stats(self):
        """Test cache statistics."""
        # Cache some results
        self.cache.set(str(self.test_image), self.test_results)
        
        stats = self.cache.get_stats()
        
        self.assertEqual(stats['total_entries'], 1)
        self.assertEqual(stats['valid_entries'], 1)
        self.assertEqual(stats['expired_entries'], 0)
        self.assertGreater(stats['total_size_bytes'], 0)
    
    def test_clear_expired(self):
        """Test clearing only expired entries."""
        # Cache results
        self.cache.set(str(self.test_image), self.test_results)
        
        # Wait for expiration
        time.sleep(2.5)
        
        # Clear expired
        count = self.cache.clear_expired()
        
        self.assertEqual(count, 1)
    
    def test_get_cache_singleton(self):
        """Test that get_cache returns singleton instance."""
        cache1 = get_cache()
        cache2 = get_cache()
        
        self.assertIs(cache1, cache2)


if __name__ == "__main__":
    unittest.main()
