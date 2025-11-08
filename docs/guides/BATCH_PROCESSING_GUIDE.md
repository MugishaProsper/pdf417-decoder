# Batch Processing Guide

## Overview

Process multiple PDF417 barcodes from directories of images efficiently.

---

## Quick Start

```bash
# Process all images in directory
python main.py decode photos/ --batch

# Recursive processing
python main.py decode photos/ --batch --recursive

# With parallel processing
python main.py decode photos/ --batch --parallel
```

---

## Command-Line Usage

### Basic Batch Processing

```bash
# Process directory
python main.py decode photos/ --batch

# Recursive (include subdirectories)
python main.py decode photos/ --batch --recursive

# Save results
python main.py decode photos/ --batch -o results.json --format json
```

### Parallel Processing

```bash
# Enable parallel processing
python main.py decode photos/ --batch --parallel

# Custom worker count
python main.py decode photos/ --batch --parallel --workers 8

# Recursive with parallel
python main.py decode photos/ --batch --recursive --parallel
```

---

## Python API

### Basic Batch Processing

```python
from src import decode_batch

# Process directory
results = decode_batch('photos/')

# Process results
for result in results:
    if result['success']:
        print(f"{result['image']}: {len(result['results'])} barcode(s)")
    else:
        print(f"{result['image']}: Error - {result['error']}")
```

### Recursive Processing

```python
# Include subdirectories
results = decode_batch('photos/', recursive=True)
```

### Parallel Processing

```python
# Enable parallel processing
results = decode_batch('photos/', use_parallel=True)

# Custom worker count
results = decode_batch('photos/', use_parallel=True, workers=4)
```

---

## Result Structure

### Batch Result Format

```python
{
    'image': str,           # Image file path
    'results': List[Dict],  # Decoded barcodes
    'success': bool,        # Whether any barcodes found
    'error': str or None    # Error message if failed
}
```

### Processing Results

```python
results = decode_batch('photos/')

# Count successful
successful = sum(1 for r in results if r['success'])
print(f"Successfully processed: {successful}/{len(results)}")

# Count total barcodes
total_barcodes = sum(len(r['results']) for r in results)
print(f"Total barcodes found: {total_barcodes}")

# List errors
errors = [r for r in results if not r['success']]
for error in errors:
    print(f"Failed: {error['image']} - {error['error']}")
```

---

## Performance Optimization

### Sequential vs Parallel

**Sequential (Default):**
- Processes one image at a time
- Lower memory usage
- Predictable performance
- Good for small batches

**Parallel:**
- Processes multiple images simultaneously
- Higher memory usage
- 2-8x faster on multi-core CPUs
- Best for large batches

### When to Use Parallel

```python
import multiprocessing as mp

# Get CPU count
cpu_count = mp.cpu_count()

# Use parallel for large batches
if image_count > 10 and cpu_count > 2:
    results = decode_batch('photos/', use_parallel=True)
else:
    results = decode_batch('photos/', use_parallel=False)
```

---

## Progress Tracking

### With tqdm (Automatic)

```bash
# Progress bar shows automatically if tqdm is installed
python main.py decode photos/ --batch

# Output:
# Processing images: 100%|████████| 50/50 [00:45<00:00, 1.11img/s]
```

### Without tqdm

```python
from src import decode_batch

results = decode_batch('photos/')

# Manual progress tracking
for i, result in enumerate(results, 1):
    print(f"Processed {i}/{len(results)}: {result['image']}")
```

---

## Output Formats

### JSON Output

```bash
python main.py decode photos/ --batch --format json -o results.json
```

```json
{
  "metadata": {
    "source": "photos/",
    "batch_mode": true,
    "total_images": 50,
    "successful_images": 45,
    "total_barcodes": 67
  },
  "results": [
    {
      "data": "BARCODE_DATA",
      "source_image": "photos/image1.jpg",
      "quality": 85
    }
  ]
}
```

### CSV Output

```bash
python main.py decode photos/ --batch --format csv -o results.csv
```

---

## Error Handling

### Handling Failed Images

```python
results = decode_batch('photos/')

# Separate successful and failed
successful = [r for r in results if r['success']]
failed = [r for r in results if not r['success']]

print(f"Successful: {len(successful)}")
print(f"Failed: {len(failed)}")

# Log errors
for result in failed:
    print(f"Error in {result['image']}: {result['error']}")
```

### Retry Failed Images

```python
# First attempt
results = decode_batch('photos/')

# Get failed images
failed_images = [r['image'] for r in results if not r['success']]

# Retry with different settings
if failed_images:
    print(f"Retrying {len(failed_images)} failed images...")
    # Implement retry logic
```

---

## Advanced Usage

### Custom File Extensions

```python
# Process specific file types
results = decode_batch(
    'photos/',
    image_extensions=('.jpg', '.png', '.tif')
)
```

### Filter Results

```python
results = decode_batch('photos/')

# Filter by quality
high_quality = [
    r for r in results 
    if r['success'] and any(b['quality'] > 80 for b in r['results'])
]

# Filter by data content
specific_data = [
    r for r in results
    if r['success'] and any('SPECIFIC' in b['data'] for b in r['results'])
]
```

### Process in Chunks

```python
from pathlib import Path

def process_in_chunks(directory, chunk_size=100):
    """Process large directories in chunks."""
    image_files = list(Path(directory).glob('*.jpg'))
    
    all_results = []
    for i in range(0, len(image_files), chunk_size):
        chunk = image_files[i:i+chunk_size]
        print(f"Processing chunk {i//chunk_size + 1}")
        
        # Create temp directory for chunk
        # Process chunk
        # Collect results
        
    return all_results
```

---

## Memory Management

### Monitor Memory Usage

```python
import psutil
import os

process = psutil.Process(os.getpid())

# Before processing
mem_before = process.memory_info().rss / 1024 / 1024  # MB

# Process batch
results = decode_batch('photos/', use_parallel=True, workers=4)

# After processing
mem_after = process.memory_info().rss / 1024 / 1024  # MB

print(f"Memory used: {mem_after - mem_before:.2f} MB")
```

### Reduce Memory Usage

```bash
# Use fewer workers
python main.py decode photos/ --batch --parallel --workers 2

# Process in smaller batches
python main.py decode photos/batch1/ --batch
python main.py decode photos/batch2/ --batch
```

---

## Examples

### Example 1: Simple Batch

```python
from src import decode_batch

results = decode_batch('photos/')

print(f"Processed {len(results)} images")
print(f"Found {sum(len(r['results']) for r in results)} barcodes")
```

### Example 2: Parallel with Progress

```python
from src import decode_batch

print("Processing images in parallel...")
results = decode_batch(
    'photos/',
    use_parallel=True,
    workers=8,
    recursive=True
)

# Summary
successful = sum(1 for r in results if r['success'])
total_barcodes = sum(len(r['results']) for r in results)

print(f"\nResults:")
print(f"  Images processed: {len(results)}")
print(f"  Successful: {successful}")
print(f"  Total barcodes: {total_barcodes}")
```

### Example 3: Export Results

```python
from src import decode_batch, export_results

# Process batch
batch_results = decode_batch('photos/', use_parallel=True)

# Flatten results for export
all_results = []
for batch_result in batch_results:
    for result in batch_result['results']:
        result['source_image'] = batch_result['image']
        all_results.append(result)

# Export to JSON
export_results(
    all_results,
    'batch_results.json',
    format_type='json',
    metadata={
        'total_images': len(batch_results),
        'total_barcodes': len(all_results)
    }
)
```

---

## Best Practices

1. **Use parallel for large batches** (>10 images)
2. **Monitor memory usage** with many workers
3. **Handle errors gracefully** - don't stop on first error
4. **Use appropriate worker count** (CPU count - 1)
5. **Save results incrementally** for very large batches
6. **Use progress bars** for user feedback
7. **Log processing details** for debugging

---

## Performance Tips

1. **Enable parallel processing** for batches >10 images
2. **Use SSD storage** for faster I/O
3. **Close other applications** to free resources
4. **Use caching** for repeated processing
5. **Process in chunks** for very large batches
6. **Optimize worker count** based on CPU cores

---

## Related Guides

- [PARALLEL_PROCESSING_GUIDE.md](../PARALLEL_PROCESSING_GUIDE.md) - Parallel processing details
- [DECODING_GUIDE.md](DECODING_GUIDE.md) - Single image decoding
- [OUTPUT_FORMATS_GUIDE.md](OUTPUT_FORMATS_GUIDE.md) - Export formats
- [CACHING_GUIDE.md](CACHING_GUIDE.md) - Performance optimization

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
