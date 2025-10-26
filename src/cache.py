"""Caching system for decoded barcode results."""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timedelta

from .logger import get_logger

logger = get_logger(__name__)


class BarcodeCache:
    """Cache for barcode decoding results."""
    
    def __init__(self, cache_dir: str = ".cache", ttl_seconds: int = 86400):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time-to-live for cache entries in seconds (default: 24 hours)
        """
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_seconds
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self) -> None:
        """Create cache directory if it doesn't exist."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Cache directory: {self.cache_dir}")
    
    def _get_file_hash(self, file_path: str) -> str:
        """
        Calculate SHA256 hash of file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex digest of file hash
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def _get_cache_path(self, file_hash: str) -> Path:
        """Get cache file path for given hash."""
        return self.cache_dir / f"{file_hash}.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """
        Check if cache entry is still valid (not expired).
        
        Args:
            cache_path: Path to cache file
            
        Returns:
            True if cache is valid, False otherwise
        """
        if not cache_path.exists():
            return False
        
        # Check if cache has expired
        cache_age = time.time() - cache_path.stat().st_mtime
        
        if cache_age > self.ttl_seconds:
            logger.debug(f"Cache expired: {cache_path.name} (age: {cache_age:.0f}s)")
            return False
        
        return True
    
    def get(self, image_path: str) -> Optional[List[Dict]]:
        """
        Get cached results for image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Cached results if available and valid, None otherwise
        """
        try:
            file_hash = self._get_file_hash(image_path)
            cache_path = self._get_cache_path(file_hash)
            
            if not self._is_cache_valid(cache_path):
                return None
            
            logger.debug(f"Cache hit: {image_path}")
            
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Reconstruct results with mock objects for rect and polygon
            results = []
            for item in cache_data['results']:
                # Create mock rect object
                class MockRect:
                    def __init__(self, data):
                        self.left = data['left']
                        self.top = data['top']
                        self.width = data['width']
                        self.height = data['height']
                    
                    def __repr__(self):
                        return f"Rect(left={self.left}, top={self.top}, width={self.width}, height={self.height})"
                
                # Create mock point objects
                class MockPoint:
                    def __init__(self, x, y):
                        self.x = x
                        self.y = y
                
                result = {
                    'data': item['data'],
                    'type': item['type'],
                    'rect': MockRect(item['rect']),
                    'polygon': [MockPoint(p['x'], p['y']) for p in item['polygon']],
                    'quality': item['quality'],
                    'preprocess_method': item['preprocess_method']
                }
                results.append(result)
            
            logger.info(f"Loaded {len(results)} result(s) from cache")
            return results
            
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")
            return None
    
    def set(self, image_path: str, results: List[Dict]) -> None:
        """
        Cache results for image.
        
        Args:
            image_path: Path to image file
            results: Decoding results to cache
        """
        try:
            file_hash = self._get_file_hash(image_path)
            cache_path = self._get_cache_path(file_hash)
            
            # Convert results to JSON-serializable format
            serializable_results = []
            for result in results:
                serializable = {
                    'data': result['data'],
                    'type': str(result['type']),
                    'quality': result['quality'],
                    'preprocess_method': result['preprocess_method'],
                    'rect': {
                        'left': result['rect'].left,
                        'top': result['rect'].top,
                        'width': result['rect'].width,
                        'height': result['rect'].height
                    },
                    'polygon': [{'x': p.x, 'y': p.y} for p in result['polygon']]
                }
                serializable_results.append(serializable)
            
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'image_path': image_path,
                'file_hash': file_hash,
                'results': serializable_results
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            logger.debug(f"Cached {len(results)} result(s) for {image_path}")
            
        except Exception as e:
            logger.warning(f"Error writing cache: {e}")
    
    def clear(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of cache files deleted
        """
        count = 0
        
        if not self.cache_dir.exists():
            return count
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except Exception as e:
                logger.warning(f"Error deleting cache file {cache_file}: {e}")
        
        logger.info(f"Cleared {count} cache entries")
        return count
    
    def clear_expired(self) -> int:
        """
        Clear expired cache entries.
        
        Returns:
            Number of expired cache files deleted
        """
        count = 0
        
        if not self.cache_dir.exists():
            return count
        
        for cache_file in self.cache_dir.glob("*.json"):
            if not self._is_cache_valid(cache_file):
                try:
                    cache_file.unlink()
                    count += 1
                except Exception as e:
                    logger.warning(f"Error deleting expired cache file {cache_file}: {e}")
        
        logger.info(f"Cleared {count} expired cache entries")
        return count
    
    def get_stats(self) -> Dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        if not self.cache_dir.exists():
            return {
                'total_entries': 0,
                'valid_entries': 0,
                'expired_entries': 0,
                'total_size_bytes': 0
            }
        
        cache_files = list(self.cache_dir.glob("*.json"))
        total_entries = len(cache_files)
        valid_entries = sum(1 for f in cache_files if self._is_cache_valid(f))
        expired_entries = total_entries - valid_entries
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_entries': total_entries,
            'valid_entries': valid_entries,
            'expired_entries': expired_entries,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }


# Global cache instance
_cache_instance: Optional[BarcodeCache] = None


def get_cache(cache_dir: str = ".cache", ttl_seconds: int = 86400) -> BarcodeCache:
    """
    Get or create global cache instance.
    
    Args:
        cache_dir: Directory to store cache files
        ttl_seconds: Time-to-live for cache entries in seconds
        
    Returns:
        BarcodeCache instance
    """
    global _cache_instance
    
    if _cache_instance is None:
        _cache_instance = BarcodeCache(cache_dir, ttl_seconds)
    
    return _cache_instance
