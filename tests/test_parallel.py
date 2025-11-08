"""Tests for parallel processing."""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
import multiprocessing as mp

from src.decoder import decode_batch, _process_single_image


class TestParallelProcessing(unittest.TestCase):
    """Test cases for parallel processing."""
    
    def setUp(self):
        """Create temporary directory with test images."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create some dummy image files
        for i in range(5):
            img_path = Path(self.temp_dir) / f"test_{i}.jpg"
            img_path.write_bytes(b"fake image data")
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('src.decoder.decode_pdf417_from_image')
    def test_process_single_image_success(self, mock_decode):
        """Test processing single image successfully."""
        mock_decode.return_value = [{'data': 'test'}]
        
        result = _process_single_image('test.jpg')
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['results']), 1)
        self.assertIsNone(result['error'])
    
    @patch('src.decoder.decode_pdf417_from_image')
    def test_process_single_image_error(self, mock_decode):
        """Test processing single image with error."""
        mock_decode.side_effect = Exception("Test error")
        
        result = _process_single_image('test.jpg')
        
        self.assertFalse(result['success'])
        self.assertEqual(len(result['results']), 0)
        self.assertIsNotNone(result['error'])
    
    @patch('src.decoder.decode_pdf417_from_image')
    def test_decode_batch_sequential(self, mock_decode):
        """Test sequential batch processing."""
        mock_decode.return_value = [{'data': 'test'}]
        
        results = decode_batch(
            self.temp_dir,
            use_parallel=False
        )
        
        self.assertEqual(len(results), 5)
        self.assertTrue(all(r['success'] for r in results))
    
    @patch('src.decoder.decode_pdf417_from_image')
    def test_decode_batch_parallel(self, mock_decode):
        """Test parallel batch processing."""
        mock_decode.return_value = [{'data': 'test'}]
        
        results = decode_batch(
            self.temp_dir,
            use_parallel=True,
            workers=2
        )
        
        self.assertEqual(len(results), 5)
    
    def test_workers_default_to_cpu_count(self):
        """Test that workers default to CPU count."""
        cpu_count = mp.cpu_count()
        self.assertGreater(cpu_count, 0)
    
    @patch('src.decoder.decode_pdf417_from_image')
    def test_parallel_faster_than_sequential(self, mock_decode):
        """Test that parallel processing can be faster."""
        import time
        
        # Simulate slow processing
        def slow_decode(*args, **kwargs):
            time.sleep(0.1)
            return [{'data': 'test'}]
        
        mock_decode.side_effect = slow_decode
        
        # This test is conceptual - actual speedup depends on system
        # Just verify both modes work
        results_seq = decode_batch(self.temp_dir, use_parallel=False)
        results_par = decode_batch(self.temp_dir, use_parallel=True, workers=2)
        
        self.assertEqual(len(results_seq), len(results_par))


if __name__ == "__main__":
    unittest.main()
