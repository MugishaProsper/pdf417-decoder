# PDF417 Barcode Decoder

A robust Python-based PDF417 barcode decoder with multiple preprocessing techniques for improved detection accuracy.

## Features

### Core Features
- **Multiple Preprocessing Methods**: Applies 7 different image preprocessing techniques to maximize detection success
- **Robust Detection**: Automatically tries multiple approaches and removes duplicate detections
- **Visual Feedback**: Optional preview window showing detected barcodes with bounding boxes
- **Detailed Metadata**: Returns position, quality, and preprocessing method information

### New in v2.0.0 🎉
- **Parallel Processing**: 2-8x speedup for batch operations with multiprocessing
- **Performance Benchmarking**: Comprehensive benchmarking suite for performance tracking
- **Complete Documentation**: 11+ comprehensive feature guides

### New in v1.4.0
- **Barcode Generation**: Create PDF417 barcodes with multiple formats (PNG, JPG, SVG, BMP)
- **Error Correction Levels**: Customizable error correction for generated barcodes

### New in v1.3.0
- **REST API Server**: FastAPI-based API with Docker support and interactive documentation
- **Docker Support**: Easy deployment with Dockerfile and docker-compose

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

#### Basic Decoding
```bash
# Decode single image
python main.py decode image.jpg

# With preview window
python main.py decode image.jpg --show

# Verbose output
python main.py decode image.jpg --verbose
```

#### Output Formats
```bash
# JSON format
python main.py decode image.jpg --format json -o results.json

# CSV format
python main.py decode image.jpg --format csv -o results.csv

# XML format
python main.py decode image.jpg --format xml -o results.xml

# Text format (default)
python main.py decode image.jpg -o results.txt
```

#### Batch Processing
```bash
# Process all images in directory
python main.py decode photos/ --batch

# Recursive processing
python main.py decode photos/ --batch --recursive

# Parallel processing (NEW in v2.0.0)
python main.py decode photos/ --batch --parallel

# Custom worker count
python main.py decode photos/ --batch --parallel --workers 8

# Batch with JSON output
python main.py decode photos/ --batch --format json -o batch_results.json
```

#### Quality Analysis
```bash
# Analyze image quality
python main.py decode image.jpg --analyze

# Output includes:
# - Resolution check
# - Contrast analysis
# - Sharpness detection
# - Noise level
# - Brightness assessment
# - Actionable recommendations
```

#### Caching
```bash
# Use cache (default)
python main.py decode image.jpg

# Bypass cache
python main.py decode image.jpg --no-cache

# View cache statistics
python main.py --cache-stats

# Clear cache
python main.py --clear-cache
```

#### Logging
```bash
# Set log level
python main.py decode image.jpg --log-level DEBUG

# Log to file
python main.py decode image.jpg --log-file logs/decode.log

# Both
python main.py decode image.jpg --log-level DEBUG --log-file logs/decode.log
```

#### Configuration File
```bash
# Use custom config
python main.py decode image.jpg --config myconfig.yaml

# Or create .pdf417rc in project root for auto-loading
```

#### Barcode Generation (NEW in v1.4.0)
```bash
# Generate barcode from text
python main.py generate "Hello World" -o barcode.png

# Generate from file
python main.py generate --input data.txt -o barcode.svg --format svg

# With error correction
python main.py generate "Important Data" -o secure.png --error-correction high

# Custom scale
python main.py generate "Data" -o large.png --scale 10
```

#### REST API Server
```bash
# Start API server
python main.py --serve

# Custom port
python main.py --serve --port 8080

# Docker deployment
docker-compose up -d

# Test API
curl -X POST "http://localhost:8000/decode" -F "file=@barcode.jpg"

# Interactive docs
# Visit: http://localhost:8000/docs
```

#### Performance Benchmarking (NEW in v2.0.0)
```bash
# Run benchmarks
python benchmarks/benchmark_suite.py

# Custom iterations
python benchmarks/benchmark_suite.py --iterations 100

# Save results
python benchmarks/benchmark_suite.py --output results/benchmark.json
```

### As a Python Module

#### Decoding
```python
from src import decode_pdf417_from_image, decode_batch

# Decode single image
results = decode_pdf417_from_image("image.jpg", show_preview=True)

for result in results:
    print(f"Data: {result['data']}")
    print(f"Position: {result['rect']}")
    print(f"Quality: {result['quality']}")

# Batch processing
batch_results = decode_batch("photos/", use_parallel=True, workers=8)

for batch in batch_results:
    print(f"{batch['image']}: {len(batch['results'])} barcode(s)")
```

#### Generation
```python
from src import generate_barcode

# Generate barcode
output_path = generate_barcode(
    data="Hello World",
    output_path="barcode.png",
    format="png",
    error_correction="medium"
)

print(f"Barcode saved to: {output_path}")
```

#### Quality Analysis
```python
from src.quality_analyzer import analyze_image_quality

# Analyze image quality
analysis = analyze_image_quality("image.jpg")

print(f"Quality: {analysis['overall_quality']}")
print(f"Score: {analysis['overall_score']:.2f}")

if analysis['issues']:
    print("Issues:", ', '.join(analysis['issues']))
```

## Project Structure

```
pdf417-decoder/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Command-line interface
│   ├── decoder.py               # Core decoding + parallel processing
│   ├── generator.py             # Barcode generation
│   ├── preprocessing.py         # Image preprocessing
│   ├── exporters.py             # Multiple output formats
│   ├── logger.py                # Logging system
│   ├── cache.py                 # Caching system
│   ├── config.py                # Configuration management
│   ├── quality_analyzer.py      # Image quality analysis
│   └── api/
│       ├── server.py            # FastAPI server
│       └── models.py            # Pydantic models
├── tests/                       # Unit tests
│   ├── test_decoder.py
│   ├── test_generator.py
│   ├── test_exporters.py
│   ├── test_cache.py
│   └── test_parallel.py
├── benchmarks/                  # Performance benchmarking
│   └── benchmark_suite.py
├── docs/                        # Documentation
│   ├── guides/                  # Feature guides
│   │   ├── DECODING_GUIDE.md
│   │   ├── CACHING_GUIDE.md
│   │   ├── BATCH_PROCESSING_GUIDE.md
│   │   ├── QUALITY_ANALYSIS_GUIDE.md
│   │   ├── OUTPUT_FORMATS_GUIDE.md
│   │   ├── CONFIGURATION_GUIDE.md
│   │   └── LOGGING_GUIDE.md
│   ├── GENERATOR_GUIDE.md
│   ├── PARALLEL_PROCESSING_GUIDE.md
│   ├── API_GUIDE.md
│   ├── BENCHMARKING_GUIDE.md
│   ├── GUIDES_INDEX.md
│   └── QUICK_REFERENCE.md
├── assets/                      # Sample images
├── main.py                      # Main entry point
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
├── config.example.yaml          # Configuration template
├── Dockerfile                   # Docker container
├── docker-compose.yml           # Docker orchestration
└── README.md                    # This file
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

## Documentation

### Quick Start
- [Quick Reference](docs/QUICK_REFERENCE.md) - Command cheat sheet
- [Guides Index](docs/GUIDES_INDEX.md) - Complete guide navigation

### Feature Guides
- [Decoding Guide](docs/guides/DECODING_GUIDE.md) - Barcode decoding
- [Generation Guide](docs/GENERATOR_GUIDE.md) - Barcode generation
- [Batch Processing Guide](docs/guides/BATCH_PROCESSING_GUIDE.md) - Multiple images
- [Parallel Processing Guide](docs/PARALLEL_PROCESSING_GUIDE.md) - Performance optimization
- [Caching Guide](docs/guides/CACHING_GUIDE.md) - Result caching
- [Quality Analysis Guide](docs/guides/QUALITY_ANALYSIS_GUIDE.md) - Image quality
- [Output Formats Guide](docs/guides/OUTPUT_FORMATS_GUIDE.md) - Export formats
- [Configuration Guide](docs/guides/CONFIGURATION_GUIDE.md) - Settings
- [Logging Guide](docs/guides/LOGGING_GUIDE.md) - Logging system
- [API Guide](docs/API_GUIDE.md) - REST API
- [Benchmarking Guide](docs/BENCHMARKING_GUIDE.md) - Performance tracking

### Additional Resources
- [API Reference](docs/api_reference.md) - REST API endpoints
- [Troubleshooting](docs/troubleshooting.md) - Common issues
- [Contributing](CONTRIBUTING.md) - Contribution guidelines

## Performance

- **Caching**: 20x+ speedup for repeated images
- **Parallel Processing**: 2-8x speedup for batch operations
- **Benchmarking**: Comprehensive performance tracking
- **Optimized**: Production-ready performance

## Troubleshooting

### pyzbar DLL Issues on Windows

If you see `FileNotFoundError: Could not find module 'libzbar-64.dll'`:

1. Install Visual C++ Redistributable
2. Use conda instead of pip
3. See [Troubleshooting Guide](docs/troubleshooting.md) for detailed solutions

### No Barcodes Detected

```bash
# Analyze image quality first
python main.py decode image.jpg --analyze

# Try with preview to see detection attempts
python main.py decode image.jpg --show

# Enable debug logging
python main.py decode image.jpg --log-level DEBUG
```

See [Troubleshooting Guide](docs/troubleshooting.md) for more solutions.

## Features Summary

✅ **Decode** PDF417 barcodes from images  
✅ **Generate** PDF417 barcodes with customization  
✅ **Batch Process** multiple images efficiently  
✅ **Parallel Processing** for 2-8x speedup  
✅ **Quality Analysis** with actionable recommendations  
✅ **Multiple Formats** - JSON, CSV, XML, TXT  
✅ **Intelligent Caching** for 20x+ speedup  
✅ **REST API** with Docker support  
✅ **Configuration** via YAML/JSON files  
✅ **Comprehensive Logging** with colored output  
✅ **Performance Benchmarking** suite  
✅ **Extensive Documentation** - 11+ guides  

## Version

**Current Version:** 2.0.0  
**Status:** Production-Ready  
**Completion:** 100% (10/10 planned features)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- **Documentation**: [docs/](docs/)
- **Guides**: [docs/GUIDES_INDEX.md](docs/GUIDES_INDEX.md)
- **Issues**: GitHub Issues
- **Quick Reference**: [docs/QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)