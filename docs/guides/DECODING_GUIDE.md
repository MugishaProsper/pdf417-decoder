# PDF417 Barcode Decoding Guide

## Overview

Complete guide to decoding PDF417 barcodes from images using the PDF417 decoder.

---

## Quick Start

### Basic Decoding

```bash
# Decode single image
python main.py decode image.jpg

# With verbose output
python main.py decode image.jpg --verbose

# With preview window
python main.py decode image.jpg --show
```

---

## Command-Line Usage

### Basic Commands

```bash
# Decode image
python main.py decode barcode.jpg

# Save output to file
python main.py decode barcode.jpg -o output.txt

# Show preview window
python main.py decode barcode.jpg --show

# Verbose mode
python main.py decode barcode.jpg --verbose
```

### Output Formats

```bash
# Text output (default)
python main.py decode barcode.jpg -o output.txt

# JSON output
python main.py decode barcode.jpg --format json -o output.json

# CSV output
python main.py decode barcode.jpg --format csv -o output.csv

# XML output
python main.py decode barcode.jpg --format xml -o output.xml
```

---

## Python API

### Basic Usage

```python
from src import decode_pdf417_from_image

# Decode image
results = decode_pdf417_from_image('barcode.jpg')

# Process results
for result in results:
    print(f"Data: {result['data']}")
    print(f"Quality: {result['quality']}")
    print(f"Position: {result['rect']}")
```

### With Preview

```python
# Show preview window
results = decode_pdf417_from_image('barcode.jpg', show_preview=True)
```

### Error Handling

```python
try:
    results = decode_pdf417_from_image('barcode.jpg')
    
    if not results:
        print("No barcodes found")
    else:
        for result in results:
            print(result['data'])
            
except FileNotFoundError:
    print("Image file not found")
except ValueError as e:
    print(f"Invalid image: {e}")
except RuntimeError as e:
    print(f"Decoding error: {e}")
```

---

## Understanding Results

### Result Structure

```python
{
    'data': str,                    # Decoded barcode data
    'type': str,                    # Barcode type (PDF417)
    'rect': Rect,                   # Bounding rectangle
    'polygon': List[Point],         # Polygon points
    'quality': int,                 # Detection quality (0-100)
    'preprocess_method': str        # Which method succeeded
}
```

### Accessing Result Data

```python
results = decode_pdf417_from_image('barcode.jpg')

for result in results:
    # Get decoded data
    data = result['data']
    
    # Get quality score
    quality = result['quality']
    
    # Get position
    rect = result['rect']
    x = rect.left
    y = rect.top
    width = rect.width
    height = rect.height
    
    # Get polygon points
    polygon = result['polygon']
    for point in polygon:
        print(f"Point: ({point.x}, {point.y})")
    
    # Get preprocessing method
    method = result['preprocess_method']
```

---

## Preprocessing Methods

The decoder tries 7 different preprocessing methods:

1. **Original** - Raw image
2. **Grayscale** - Color to grayscale conversion
3. **Binary Threshold** - OTSU adaptive thresholding
4. **Inverted Binary** - Inverted threshold
5. **Adaptive Threshold** - Gaussian adaptive thresholding
6. **Morphological** - Gap closing operations
7. **Sharpening** - Edge enhancement

The decoder automatically tries all methods and returns the best results.

---

## Image Requirements

### Recommended Specifications

- **Resolution:** Minimum 300x300 pixels
- **Format:** JPG, PNG, BMP, TIFF
- **Quality:** Clear, well-lit images
- **Contrast:** Good contrast between barcode and background
- **Focus:** Sharp, not blurry

### Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

---

## Troubleshooting

### No Barcodes Found

**Possible Causes:**
- Image quality too low
- Barcode too small
- Poor contrast
- Blurry image
- Wrong barcode type

**Solutions:**
```bash
# Analyze image quality
python main.py decode image.jpg --analyze

# Try with preview to see detection attempts
python main.py decode image.jpg --show

# Enable debug logging
python main.py decode image.jpg --log-level DEBUG
```

### Poor Quality Results

**Solutions:**
- Increase image resolution
- Improve lighting
- Ensure barcode is in focus
- Clean barcode surface
- Use quality analysis

### Multiple Barcodes

```python
# The decoder automatically finds all barcodes
results = decode_pdf417_from_image('multiple_barcodes.jpg')

print(f"Found {len(results)} barcodes")

for i, result in enumerate(results, 1):
    print(f"Barcode {i}: {result['data']}")
```

---

## Advanced Usage

### Custom Processing

```python
import cv2
from src.preprocessing import preprocess_image
from src.decoder import decode_pdf417_from_image

# Load image
image = cv2.imread('barcode.jpg')

# Apply custom preprocessing
processed = preprocess_image(image)

# Decode
results = decode_pdf417_from_image('barcode.jpg')
```

### Batch Processing

See [BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md)

### Quality Analysis

See [QUALITY_ANALYSIS_GUIDE.md](QUALITY_ANALYSIS_GUIDE.md)

---

## Performance Tips

1. **Use appropriate image size** - Not too large, not too small
2. **Good lighting** - Ensure even lighting
3. **Clean images** - Remove noise and artifacts
4. **Use caching** - For repeated images
5. **Batch processing** - For multiple images

---

## Examples

### Example 1: Simple Decode

```python
from src import decode_pdf417_from_image

results = decode_pdf417_from_image('license.jpg')

if results:
    print(f"License data: {results[0]['data']}")
else:
    print("No barcode found")
```

### Example 2: Multiple Barcodes

```python
results = decode_pdf417_from_image('shipping_label.jpg')

for i, result in enumerate(results, 1):
    print(f"Barcode {i}:")
    print(f"  Data: {result['data']}")
    print(f"  Quality: {result['quality']}")
    print(f"  Position: ({result['rect'].left}, {result['rect'].top})")
```

### Example 3: With Error Handling

```python
import sys

try:
    results = decode_pdf417_from_image('barcode.jpg')
    
    if not results:
        print("No barcodes found in image")
        sys.exit(1)
    
    # Process results
    for result in results:
        # Extract specific fields from data
        data = result['data']
        # Parse data as needed
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

---

## Integration Examples

### Web Application

```python
from flask import Flask, request, jsonify
from src import decode_pdf417_from_image
import tempfile

app = Flask(__name__)

@app.route('/decode', methods=['POST'])
def decode():
    file = request.files['image']
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        file.save(tmp.name)
        
        # Decode
        results = decode_pdf417_from_image(tmp.name)
        
        return jsonify({
            'success': len(results) > 0,
            'count': len(results),
            'results': [{'data': r['data'], 'quality': r['quality']} for r in results]
        })
```

### Command-Line Tool

```bash
#!/bin/bash
# Decode all images in directory

for img in *.jpg; do
    echo "Processing $img..."
    python main.py decode "$img" -o "${img%.jpg}.txt"
done
```

---

## Best Practices

1. **Validate input** - Check file exists and is valid image
2. **Handle errors** - Use try-catch blocks
3. **Check results** - Verify barcode was found
4. **Use quality analysis** - For problematic images
5. **Cache results** - For repeated processing
6. **Log operations** - For debugging and monitoring

---

## Related Guides

- [BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md) - Process multiple images
- [QUALITY_ANALYSIS_GUIDE.md](QUALITY_ANALYSIS_GUIDE.md) - Analyze image quality
- [CACHING_GUIDE.md](CACHING_GUIDE.md) - Use caching for performance
- [OUTPUT_FORMATS_GUIDE.md](OUTPUT_FORMATS_GUIDE.md) - Export in different formats

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
- API Reference: `docs/api.md`
