# Quick Reference Guide

## Common Commands

### Single Image Processing
```bash
# Basic decode
python main.py image.jpg

# With preview
python main.py image.jpg --show

# Save as JSON
python main.py image.jpg --format json -o results.json

# Analyze quality
python main.py image.jpg --analyze
```

### Batch Processing
```bash
# Process directory
python main.py photos/ --batch

# Recursive
python main.py photos/ --batch --recursive

# With output
python main.py photos/ --batch --format json -o batch.json
```

### Cache Management
```bash
# View stats
python main.py --cache-stats

# Clear cache
python main.py --clear-cache

# Bypass cache
python main.py image.jpg --no-cache
```

### Logging
```bash
# Debug mode
python main.py image.jpg --log-level DEBUG

# Log to file
python main.py image.jpg --log-file logs/decode.log
```

## CLI Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `image` | Image path or directory | `image.jpg` or `photos/` |
| `--show` | Show preview window | `--show` |
| `--verbose` | Verbose output | `--verbose` |
| `-o, --output` | Output file path | `-o results.json` |
| `-f, --format` | Output format | `--format json` |
| `--batch` | Batch processing mode | `--batch` |
| `--recursive` | Recursive directory scan | `--recursive` |
| `--analyze` | Quality analysis | `--analyze` |
| `--no-cache` | Bypass cache | `--no-cache` |
| `--clear-cache` | Clear all cache | `--clear-cache` |
| `--cache-stats` | Show cache stats | `--cache-stats` |
| `--log-level` | Logging level | `--log-level DEBUG` |
| `--log-file` | Log file path | `--log-file logs/app.log` |
| `--config` | Config file path | `--config myconfig.yaml` |

## Output Formats

### JSON
```json
{
  "metadata": {
    "source": "image.jpg",
    "timestamp": "2025-11-08T10:00:00"
  },
  "results": [
    {
      "data": "BARCODE_DATA",
      "quality": 85,
      "rect": {"left": 10, "top": 20, "width": 100, "height": 50}
    }
  ]
}
```

### CSV
```csv
barcode_id,data,type,quality,rect_left,rect_top,rect_width,rect_height
1,BARCODE_DATA,PDF417,85,10,20,100,50
```

### XML
```xml
<?xml version="1.0" encoding="utf-8"?>
<pdf417_results>
  <barcodes count="1">
    <barcode id="1">
      <data>BARCODE_DATA</data>
      <quality>85</quality>
    </barcode>
  </barcodes>
</pdf417_results>
```

## Configuration File

Create `.pdf417rc` or `config.yaml`:

```yaml
output:
  format: json
  verbose: true

cache:
  enabled: true
  ttl: 86400

batch:
  recursive: false
  show_progress: true

logging:
  level: INFO
  file: null
```

## Quality Analysis Output

```
Overall Quality: GOOD (0.75/1.0)

Detailed Analysis:
  • Resolution: 1407x389
  • Contrast: good (0.68)
  • Sharpness: moderate (0.52)
  • Noise: low (0.08)
  • Brightness: optimal (0.48)

💡 Recommendations:
  • Image quality is good for barcode detection
```

## Cache Statistics

```
📊 Cache Statistics:
   Total entries: 15
   Valid entries: 12
   Expired entries: 3
   Total size: 2.4 MB
```

## Python API

```python
from src import decode_pdf417_from_image, decode_batch

# Single image
results = decode_pdf417_from_image("image.jpg")
for result in results:
    print(result['data'])

# Batch processing
batch_results = decode_batch("photos/", recursive=True)
for batch in batch_results:
    print(f"{batch['image']}: {len(batch['results'])} barcodes")

# With caching
from src import get_cache
cache = get_cache()
cached_results = cache.get("image.jpg")

# Quality analysis
from src.quality_analyzer import analyze_image_quality
analysis = analyze_image_quality("image.jpg")
print(f"Quality: {analysis['overall_quality']}")
```

## Troubleshooting

### No barcodes found
```bash
# Check image quality
python main.py image.jpg --analyze

# Try with preview to see detection attempts
python main.py image.jpg --show

# Enable debug logging
python main.py image.jpg --log-level DEBUG
```

### Slow processing
```bash
# Use cache (enabled by default)
python main.py image.jpg

# Check cache stats
python main.py --cache-stats
```

### pyzbar errors
See `docs/troubleshooting.md` for Windows DLL issues.

## Performance Tips

1. **Use caching** for repeated images (20x+ speedup)
2. **Batch processing** for multiple images
3. **Quality analysis** before processing large batches
4. **Appropriate format** - JSON for structured data, CSV for spreadsheets
5. **Log to file** for debugging without console clutter
