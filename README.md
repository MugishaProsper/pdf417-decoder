# PDF417 Barcode Decoder

A robust Python-based PDF417 barcode decoder with multiple preprocessing techniques for improved detection accuracy.

## Features

### Core Features
- **Multiple Preprocessing Methods**: Applies 7 different image preprocessing techniques to maximize detection success
- **Robust Detection**: Automatically tries multiple approaches and removes duplicate detections
- **Visual Feedback**: Optional preview window showing detected barcodes with bounding boxes
- **Detailed Metadata**: Returns position, quality, and preprocessing method information

### New in v1.2.0
- **Intelligent Caching**: 20x+ speedup for repeated images with automatic cache management
- **Quality Analysis**: Comprehensive image quality assessment with actionable recommendations
- **Configuration Files**: Persistent settings via YAML/JSON config files

### New in v1.1.0
- **Batch Processing**: Process entire directories with progress bars
- **Multiple Output Formats**: Export as JSON, CSV, XML, or TXT
- **Structured Logging**: Colored console output and file logging

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Windows Users

If you encounter issues with `pyzbar` on Windows, you may need to:

1. Install Visual C++ Redistributable for Visual Studio 2015-2022
2. Or use conda: `conda install -c conda-forge pyzbar`

## Usage

### Command Line

#### Basic Usage
```bash
# Decode single image
python main.py path/to/image.jpg

# With preview window
python main.py path/to/image.jpg --show

# Verbose output
python main.py path/to/image.jpg --verbose
```

#### Output Formats (NEW in v1.1.0)
```bash
# JSON format
python main.py image.jpg --format json -o results.json

# CSV format
python main.py image.jpg --format csv -o results.csv

# XML format
python main.py image.jpg --format xml -o results.xml

# Text format (default)
python main.py image.jpg -o results.txt
```

#### Batch Processing (NEW in v1.1.0)
```bash
# Process all images in directory
python main.py assets/ --batch

# Recursive processing
python main.py assets/ --batch --recursive

# Batch with JSON output
python main.py assets/ --batch --format json -o batch_results.json
```

#### Quality Analysis (NEW in v1.2.0)
```bash
# Analyze image quality
python main.py image.jpg --analyze

# Output includes:
# - Resolution check
# - Contrast analysis
# - Sharpness detection
# - Noise level
# - Brightness assessment
# - Actionable recommendations
```

#### Caching (NEW in v1.2.0)
```bash
# Use cache (default)
python main.py image.jpg

# Bypass cache
python main.py image.jpg --no-cache

# View cache statistics
python main.py --cache-stats

# Clear cache
python main.py --clear-cache
```

#### Logging (NEW in v1.1.0)
```bash
# Set log level
python main.py image.jpg --log-level DEBUG

# Log to file
python main.py image.jpg --log-file logs/decode.log

# Both
python main.py image.jpg --log-level DEBUG --log-file logs/decode.log
```

#### Configuration File (NEW in v1.2.0)
```bash
# Use custom config
python main.py image.jpg --config myconfig.yaml

# Or create .pdf417rc in project root for auto-loading
```

### As a Python Module

```python
from src.decoder import decode_pdf417_from_image

# Decode barcodes from an image
results = decode_pdf417_from_image("path/to/image.jpg", show_preview=True)

for result in results:
    print(f"Data: {result['data']}")
    print(f"Position: {result['rect']}")
    print(f"Quality: {result['quality']}")
```

## Project Structure

```
pdf417-decoder/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── decoder.py           # Core decoding logic
│   ├── preprocessing.py     # Image preprocessing utilities
│   └── cli.py              # Command-line interface
├── assets/                  # Sample images (gitignored)
├── docs/                    # Documentation
├── tests/                   # Unit tests
├── main.py                  # Main entry point
├── setup.py                 # Package setup configuration
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Preprocessing Techniques

The decoder applies the following preprocessing methods:

1. **Original Image**: Raw input
2. **Grayscale**: Color to grayscale conversion
3. **Binary Threshold**: OTSU adaptive thresholding
4. **Inverted Binary**: Inverted threshold for dark-on-light barcodes
5. **Adaptive Threshold**: Gaussian adaptive thresholding
6. **Morphological Operations**: Gap closing with morphological operations
7. **Sharpening**: Edge enhancement filter

## Output Format

Each detected barcode returns:

```python
{
    'data': str,                    # Decoded barcode data
    'type': str,                    # Barcode type (PDF417)
    'rect': Rect,                   # Bounding rectangle
    'polygon': List[Point],         # Polygon points
    'quality': int,                 # Detection quality score
    'preprocess_method': str        # Which preprocessing method succeeded
}
```

## Troubleshooting

### pyzbar DLL Issues on Windows

If you see `FileNotFoundError: Could not find module 'libzbar-64.dll'`:

1. Install Visual C++ Redistributable
2. Use conda instead of pip
3. See `docs/troubleshooting.md` for detailed solutions

### No Barcodes Detected

- Ensure the image contains a PDF417 barcode
- Try increasing image resolution
- Check image quality and contrast
- Use `--show` flag to visualize detection attempts

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.