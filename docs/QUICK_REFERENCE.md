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
barcode_id,data,type,quality,rect_left,rect_top,rect