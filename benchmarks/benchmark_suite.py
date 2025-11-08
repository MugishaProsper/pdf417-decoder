"""Performance benchmarking suite for PDF417 decoder."""

import time
import statistics
import psutil
import os
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

from src.decoder import decode_pdf417_from_image
from src.preprocessing import preprocess_image
from src.generator import generate_barcode
from src.logger import get_logger

logger = get_logger(__name__)


class PerformanceBenchmark:
    """Performance benchmarking for PDF417 operations."""
    
    def __init__(self, iterations: int = 10):
        """
        Initialize benchmark.
        
        Args:
            iterations: Number of iterations for each test
        """
        self.iterations = iterations
        self.results = {}
        self.process = psutil.Process(os.getpid())
    
    def benchmark_decode(
        self,
        image_path: str,
        use_cache: bool = False
    ) -> Dict:
        """
        Benchmark decoding performance.
        
        Args:
            image_path: Path to test image
            use_cache: Whether to use caching
            
        Returns:
            Benchmark results
        """
        logger.info(f"Benchmarking decode: {image_path} (cache={use_cache})")
        
        times = []
        memory_usage = []
        success_count = 0
        barcode_counts = []
        
        for i in range(self.iterations):
            # Measure memory before
            mem_before = self.process.memory_info().rss / 1024 / 1024  # MB
            
            # Measure time
            start_time = time.time()
            try:
                results = decode_pdf417_from_image(image_path, show_preview=False)
                elapsed = time.time() - start_time
                
                times.append(elapsed)
                success_count += 1
                barcode_counts.append(len(results))
            except Exception as e:
                logger.warning(f"Iteration {i+1} failed: {e}")
                times.append(float('inf'))
                barcode_counts.append(0)
            
            # Measure memory after
            mem_after = self.process.memory_info().rss / 1024 / 1024  # MB
            memory_usage.append(mem_after - mem_before)
        
        # Calculate statistics
        valid_times = [t for t in times if t != float('inf')]
        
        return {
            'operation': 'decode',
            'image': image_path,
            'iterations': self.iterations,
            'success_rate': success_count / self.iterations * 100,
            'avg_time': statistics.mean(valid_times) if valid_times else 0,
            'min_time': min(valid_times) if valid_times else 0,
            'max_time': max(valid_times) if valid_times else 0,
            'median_time': statistics.median(valid_times) if valid_times else 0,
            'std_dev': statistics.stdev(valid_times) if len(valid_times) > 1 else 0,
            'avg_memory_mb': statistics.mean(memory_usage),
            'peak_memory_mb': max(memory_usage),
            'avg_barcodes': statistics.mean(barcode_counts),
            'cache_enabled': use_cache
        }
    
    def benchmark_preprocessing(self, image_path: str) -> Dict:
        """
        Benchmark preprocessing performance.
        
        Args:
            image_path: Path to test image
            
        Returns:
            Benchmark results
        """
        logger.info(f"Benchmarking preprocessing: {image_path}")
        
        import cv2
        image = cv2.imread(image_path)
        
        times = []
        method_times = {i: [] for i in range(7)}
        
        for _ in range(self.iterations):
            start_time = time.time()
            processed = preprocess_image(image)
            elapsed = time.time() - start_time
            times.append(elapsed)
            
            # Benchmark individual methods
            for i in range(7):
                method_start = time.time()
                _ = processed[i] if i < len(processed) else None
                method_times[i].append(time.time() - method_start)
        
        return {
            'operation': 'preprocessing',
            'image': image_path,
            'iterations': self.iterations,
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'median_time': statistics.median(times),
            'method_times': {
                f'method_{i}': statistics.mean(times) 
                for i, times in method_times.items()
            }
        }
    
    def benchmark_generation(
        self,
        data_length: int = 100,
        format: str = 'png'
    ) -> Dict:
        """
        Benchmark barcode generation.
        
        Args:
            data_length: Length of data to encode
            format: Output format
            
        Returns:
            Benchmark results
        """
        logger.info(f"Benchmarking generation: {data_length} chars, {format}")
        
        import tempfile
        data = "X" * data_length
        
        times = []
        file_sizes = []
        
        for _ in range(self.iterations):
            with tempfile.NamedTemporaryFile(suffix=f'.{format}', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                start_time = time.time()
                result_path = generate_barcode(data, output_path, format=format)
                elapsed = time.time() - start_time
                
                times.append(elapsed)
                file_sizes.append(os.path.getsize(result_path) / 1024)  # KB
                
                # Cleanup
                os.unlink(result_path)
            except Exception as e:
                logger.warning(f"Generation failed: {e}")
                times.append(float('inf'))
        
        valid_times = [t for t in times if t != float('inf')]
        
        return {
            'operation': 'generation',
            'data_length': data_length,
            'format': format,
            'iterations': self.iterations,
            'avg_time': statistics.mean(valid_times) if valid_times else 0,
            'min_time': min(valid_times) if valid_times else 0,
            'max_time': max(valid_times) if valid_times else 0,
            'median_time': statistics.median(valid_times) if valid_times else 0,
            'avg_file_size_kb': statistics.mean(file_sizes) if file_sizes else 0
        }
    
    def benchmark_cache_performance(self, image_path: str) -> Dict:
        """
        Benchmark cache performance.
        
        Args:
            image_path: Path to test image
            
        Returns:
            Benchmark results
        """
        logger.info(f"Benchmarking cache: {image_path}")
        
        from src.cache import get_cache
        cache = get_cache()
        
        # Clear cache first
        cache.clear()
        
        # First run (no cache)
        start_time = time.time()
        results = decode_pdf417_from_image(image_path, show_preview=False)
        no_cache_time = time.time() - start_time
        
        # Cache the results
        cache.set(image_path, results)
        
        # Second run (with cache)
        start_time = time.time()
        cached_results = cache.get(image_path)
        cache_time = time.time() - start_time
        
        speedup = no_cache_time / cache_time if cache_time > 0 else 0
        
        return {
            'operation': 'cache_performance',
            'image': image_path,
            'no_cache_time': no_cache_time,
            'cache_time': cache_time,
            'speedup': speedup,
            'cache_hit': cached_results is not None
        }
    
    def run_full_suite(
        self,
        test_images: Optional[List[str]] = None
    ) -> Dict:
        """
        Run complete benchmark suite.
        
        Args:
            test_images: List of test image paths
            
        Returns:
            Complete benchmark results
        """
        logger.info("Starting full benchmark suite")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'iterations': self.iterations,
            'system_info': self._get_system_info(),
            'benchmarks': []
        }
        
        # Use default test images if none provided
        if not test_images:
            test_images = self._get_test_images()
        
        # Decode benchmarks
        for image_path in test_images:
            if os.path.exists(image_path):
                results['benchmarks'].append(
                    self.benchmark_decode(image_path, use_cache=False)
                )
                results['benchmarks'].append(
                    self.benchmark_preprocessing(image_path)
                )
                results['benchmarks'].append(
                    self.benchmark_cache_performance(image_path)
                )
        
        # Generation benchmarks
        for data_length in [50, 100, 500, 1000]:
            for format in ['png', 'svg']:
                results['benchmarks'].append(
                    self.benchmark_generation(data_length, format)
                )
        
        # Calculate summary
        results['summary'] = self._calculate_summary(results['benchmarks'])
        
        logger.info("Benchmark suite complete")
        return results
    
    def _get_system_info(self) -> Dict:
        """Get system information."""
        return {
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_total_gb': psutil.virtual_memory().total / 1024 / 1024 / 1024,
            'memory_available_gb': psutil.virtual_memory().available / 1024 / 1024 / 1024,
            'python_version': os.sys.version
        }
    
    def _get_test_images(self) -> List[str]:
        """Get list of test images."""
        test_images = []
        
        # Look for images in assets directory
        assets_dir = Path('assets')
        if assets_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png']:
                test_images.extend(str(p) for p in assets_dir.glob(ext))
        
        # Look for images in benchmarks/test_images
        test_dir = Path('benchmarks/test_images')
        if test_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png']:
                test_images.extend(str(p) for p in test_dir.glob(ext))
        
        return test_images[:5]  # Limit to 5 images
    
    def _calculate_summary(self, benchmarks: List[Dict]) -> Dict:
        """Calculate summary statistics."""
        decode_times = [b['avg_time'] for b in benchmarks if b['operation'] == 'decode']
        gen_times = [b['avg_time'] for b in benchmarks if b['operation'] == 'generation']
        cache_speedups = [b['speedup'] for b in benchmarks if b['operation'] == 'cache_performance']
        
        return {
            'avg_decode_time': statistics.mean(decode_times) if decode_times else 0,
            'avg_generation_time': statistics.mean(gen_times) if gen_times else 0,
            'avg_cache_speedup': statistics.mean(cache_speedups) if cache_speedups else 0,
            'total_benchmarks': len(benchmarks)
        }
    
    def save_results(self, results: Dict, output_path: str):
        """Save benchmark results to file."""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to: {output_path}")
    
    def print_results(self, results: Dict):
        """Print benchmark results to console."""
        print("\n" + "="*70)
        print("PDF417 DECODER - PERFORMANCE BENCHMARK RESULTS")
        print("="*70)
        
        print(f"\nTimestamp: {results['timestamp']}")
        print(f"Iterations per test: {results['iterations']}")
        
        print("\n--- System Information ---")
        sys_info = results['system_info']
        print(f"CPU Cores: {sys_info['cpu_count']}")
        print(f"CPU Usage: {sys_info['cpu_percent']}%")
        print(f"Memory Total: {sys_info['memory_total_gb']:.2f} GB")
        print(f"Memory Available: {sys_info['memory_available_gb']:.2f} GB")
        
        print("\n--- Benchmark Results ---")
        for benchmark in results['benchmarks']:
            op = benchmark['operation']
            print(f"\n{op.upper()}:")
            
            if op == 'decode':
                print(f"  Image: {benchmark['image']}")
                print(f"  Success Rate: {benchmark['success_rate']:.1f}%")
                print(f"  Avg Time: {benchmark['avg_time']*1000:.2f} ms")
                print(f"  Min Time: {benchmark['min_time']*1000:.2f} ms")
                print(f"  Max Time: {benchmark['max_time']*1000:.2f} ms")
                print(f"  Median Time: {benchmark['median_time']*1000:.2f} ms")
                print(f"  Std Dev: {benchmark['std_dev']*1000:.2f} ms")
                print(f"  Avg Memory: {benchmark['avg_memory_mb']:.2f} MB")
                print(f"  Avg Barcodes: {benchmark['avg_barcodes']:.1f}")
            
            elif op == 'generation':
                print(f"  Data Length: {benchmark['data_length']} chars")
                print(f"  Format: {benchmark['format']}")
                print(f"  Avg Time: {benchmark['avg_time']*1000:.2f} ms")
                print(f"  Avg File Size: {benchmark['avg_file_size_kb']:.2f} KB")
            
            elif op == 'cache_performance':
                print(f"  Image: {benchmark['image']}")
                print(f"  No Cache: {benchmark['no_cache_time']*1000:.2f} ms")
                print(f"  With Cache: {benchmark['cache_time']*1000:.2f} ms")
                print(f"  Speedup: {benchmark['speedup']:.1f}x")
        
        print("\n--- Summary ---")
        summary = results['summary']
        print(f"Average Decode Time: {summary['avg_decode_time']*1000:.2f} ms")
        print(f"Average Generation Time: {summary['avg_generation_time']*1000:.2f} ms")
        print(f"Average Cache Speedup: {summary['avg_cache_speedup']:.1f}x")
        print(f"Total Benchmarks: {summary['total_benchmarks']}")
        
        print("\n" + "="*70)


def main():
    """Run benchmark suite from command line."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PDF417 Performance Benchmark")
    parser.add_argument(
        '--iterations',
        type=int,
        default=10,
        help='Number of iterations per test (default: 10)'
    )
    parser.add_argument(
        '--output',
        default='benchmarks/results/benchmark_results.json',
        help='Output file path'
    )
    parser.add_argument(
        '--images',
        nargs='+',
        help='Test image paths'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run benchmarks
    benchmark = PerformanceBenchmark(iterations=args.iterations)
    results = benchmark.run_full_suite(test_images=args.images)
    
    # Print results
    benchmark.print_results(results)
    
    # Save results
    benchmark.save_results(results, args.output)
    
    print(f"\n✅ Benchmark complete! Results saved to: {args.output}")


if __name__ == "__main__":
    main()
