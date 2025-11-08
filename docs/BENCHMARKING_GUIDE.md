# Performance Benchmarking Guide

## Overview

The PDF417 decoder includes a comprehensive benchmarking suite to measure and track performance across different operations.

---

## Quick Start

### Run Full Benchmark Suite

```bash
# Run with default settings (10 iterations)
python benchmarks/benchmark_suite.py

# Custom iterations
python benchmarks/benchmark_suite.py --iterations 100

# Specify test images
python benchmarks/benchmark_suite.py --images assets/sample1.jpg assets/sample2.jpg

# Custom output location
python benchmarks/benchmark_suite.py --output results/my_benchmark.json
```

### Using the Script

```bash
python scripts/run_benchmarks.py --iterations 50
```

---

## What Gets Benchmarked

### 1. Decode Performance
- Average decode time
- Min/max/median times
- Standard deviation
- Success rate
- Memory usage
- Barcodes found per image

### 2. Preprocessing Performance
- Total preprocessing time
- Individual method times
- Method comparison

### 3. Generation Performance
- Generation time by data length
- Generation time by format
- File size analysis

### 4. Cache Performance
- Cache hit vs miss times
- Speedup factor
- Cache effectiveness

---

## Benchmark Results

### Output Format

Results are saved as JSON:

```json
{
  "timestamp": "2025-11-08T10:00:00",
  "iterations": 10,
  "system_info": {
    "cpu_count": 8,
    "cpu_percent": 25.5,
    "memory_total_gb": 16.0,
    "memory_available_gb": 8.5
  },
  "benchmarks": [
    {
      "operation": "decode",
      "image": "assets/sample.jpg",
      "avg_time": 0.142,
      "success_rate": 100.0,
      "avg_memory_mb": 45.2
    }
  ],
  "summary": {
    "avg_decode_time": 0.142,
    "avg_generation_time": 0.085,
    "avg_cache_speedup": 23.5
  }
}
```

### Console Output

```
======================================================================
PDF417 DECODER - PERFORMANCE BENCHMARK RESULTS
======================================================================

Timestamp: 2025-11-08T10:00:00
Iterations per test: 10

--- System Information ---
CPU Cores: 8
CPU Usage: 25.5%
Memory Total: 16.00 GB
Memory Available: 8.50 GB

--- Benchmark Results ---

DECODE:
  Image: assets/sample.jpg
  Success Rate: 100.0%
  Avg Time: 142.35 ms
  Min Time: 135.20 ms
  Max Time: 158.90 ms
  Median Time: 140.50 ms
  Std Dev: 6.75 ms
  Avg Memory: 45.20 MB
  Avg Barcodes: 1.0

GENERATION:
  Data Length: 100 chars
  Format: png
  Avg Time: 85.40 ms
  Avg File Size: 12.50 KB

CACHE_PERFORMANCE:
  Image: assets/sample.jpg
  No Cache: 142.35 ms
  With Cache: 6.05 ms
  Speedup: 23.5x

--- Summary ---
Average Decode Time: 142.35 ms
Average Generation Time: 85.40 ms
Average Cache Speedup: 23.5x
Total Benchmarks: 15

======================================================================
```

---

## Python API

### Basic Usage

```python
from benchmarks.benchmark_suite import PerformanceBenchmark

# Create benchmark
benchmark = PerformanceBenchmark(iterations=10)

# Run full suite
results = benchmark.run_full_suite()

# Print results
benchmark.print_results(results)

# Save results
benchmark.save_results(results, 'results.json')
```

### Individual Benchmarks

```python
# Benchmark decode
decode_results = benchmark.benchmark_decode('image.jpg')

# Benchmark preprocessing
preprocess_results = benchmark.benchmark_preprocessing('image.jpg')

# Benchmark generation
gen_results = benchmark.benchmark_generation(data_length=100, format='png')

# Benchmark cache
cache_results = benchmark.benchmark_cache_performance('image.jpg')
```

---

## Interpreting Results

### Decode Performance

**Good Performance:**
- Avg Time: <200ms
- Success Rate: >95%
- Memory Usage: <100MB

**Needs Improvement:**
- Avg Time: >500ms
- Success Rate: <80%
- Memory Usage: >200MB

### Cache Performance

**Effective Caching:**
- Speedup: >10x
- Cache Hit: True

**Ineffective Caching:**
- Speedup: <5x
- High cache miss rate

### Generation Performance

**Good Performance:**
- <100ms for 100 chars
- <200ms for 500 chars
- <500ms for 1000 chars

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Performance Benchmarks

on: [push, pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run benchmarks
        run: python benchmarks/benchmark_suite.py --iterations 5
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: benchmark-results
          path: benchmarks/results/
```

---

## Comparing Results

### Track Performance Over Time

```python
import json
from pathlib import Path

# Load multiple benchmark results
results_dir = Path('benchmarks/results')
all_results = []

for result_file in results_dir.glob('*.json'):
    with open(result_file) as f:
        all_results.append(json.load(f))

# Compare decode times
for result in all_results:
    timestamp = result['timestamp']
    avg_time = result['summary']['avg_decode_time']
    print(f"{timestamp}: {avg_time*1000:.2f} ms")
```

### Regression Detection

```python
def check_regression(current_results, baseline_results, threshold=1.2):
    """Check if performance has regressed."""
    current_time = current_results['summary']['avg_decode_time']
    baseline_time = baseline_results['summary']['avg_decode_time']
    
    if current_time > baseline_time * threshold:
        print(f"⚠️ Performance regression detected!")
        print(f"Current: {current_time*1000:.2f} ms")
        print(f"Baseline: {baseline_time*1000:.2f} ms")
        print(f"Slowdown: {(current_time/baseline_time):.2f}x")
        return True
    return False
```

---

## Best Practices

### 1. Consistent Environment

Run benchmarks in consistent conditions:
- Same hardware
- Same system load
- Same Python version
- Same dependencies

### 2. Sufficient Iterations

```bash
# Quick check
python benchmarks/benchmark_suite.py --iterations 5

# Reliable results
python benchmarks/benchmark_suite.py --iterations 50

# High precision
python benchmarks/benchmark_suite.py --iterations 100
```

### 3. Representative Test Data

Use images that represent real-world usage:
- Various sizes
- Different quality levels
- Multiple barcode types

### 4. Regular Monitoring

```bash
# Run daily benchmarks
0 2 * * * cd /path/to/project && python benchmarks/benchmark_suite.py --output results/daily_$(date +\%Y\%m\%d).json
```

---

## Troubleshooting

### High Variance

If results show high variance:
- Increase iterations
- Close other applications
- Check system load
- Use dedicated hardware

### Memory Issues

If benchmarks fail due to memory:
- Reduce iterations
- Use smaller test images
- Close other applications

### Slow Benchmarks

If benchmarks take too long:
- Reduce iterations
- Reduce number of test images
- Skip generation benchmarks

---

## Advanced Usage

### Custom Benchmarks

```python
from benchmarks.benchmark_suite import PerformanceBenchmark

class CustomBenchmark(PerformanceBenchmark):
    def benchmark_custom_operation(self):
        """Benchmark custom operation."""
        times = []
        for _ in range(self.iterations):
            start = time.time()
            # Your operation here
            times.append(time.time() - start)
        
        return {
            'operation': 'custom',
            'avg_time': statistics.mean(times)
        }

# Run custom benchmark
benchmark = CustomBenchmark(iterations=10)
results = benchmark.benchmark_custom_operation()
```

### Profiling Integration

```python
import cProfile
import pstats

# Profile decode operation
profiler = cProfile.Profile()
profiler.enable()

decode_pdf417_from_image('image.jpg')

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

---

## Performance Goals

### Target Metrics

| Operation | Target | Excellent |
|-----------|--------|-----------|
| Decode (small) | <200ms | <100ms |
| Decode (large) | <500ms | <300ms |
| Generation | <100ms | <50ms |
| Cache speedup | >10x | >20x |
| Success rate | >95% | >99% |

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
- Examples: See above
