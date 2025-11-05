# PDF417 Barcode Decoder

A robust Python-based PDF417 barcode decoder with multiple preprocessing techniques for improved detection accuracy.

## Features

- **Multiple Preprocessing Methods**: Applies 7 different image preprocessing techniques to maximize detection success
- **Robust Detection**: Automatically tries multiple approaches and removes duplicate detections
- **Visual Feedback**: Optional preview window showing detected barcodes with bounding boxes
- **CLI Interface**: Easy-to-use command-line interface
- **Detailed Metadata**: Returns position, quality, and preprocessing method information

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

Basic usage:
```bash
python main.py path/to/image.jpg
```

With preview window:
```bash
python main.py path/to/image.jpg --show
```

Save output to file:
```bash
python main.py path/to/image.jpg -o output.txt
```

Verbose mode:
```bash
python main.py path/to/image.jpg --verbose
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
