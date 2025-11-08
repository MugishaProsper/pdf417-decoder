# PDF417 Barcode Generator Guide

## Overview

The PDF417 decoder now includes barcode generation capabilities, making it a complete bidirectional tool for both decoding and creating PDF417 barcodes.

---

## Quick Start

### Generate from String

```bash
# Basic generation
python main.py generate "Hello World" -o barcode.png

# With custom settings
python main.py generate "My Data" -o barcode.png --error-correction high --scale 5
```

### Generate from File

```bash
# Read data from text file
python main.py generate --input data.txt -o barcode.png

# Generate SVG
python main.py generate --input data.txt -o barcode.svg --format svg
```

---

## CLI Usage

### Basic Command

```bash
python main.py generate [DATA] -o OUTPUT [OPTIONS]
```

### Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `DATA` | Data to encode (or use `--input`) | Yes* |
| `-o, --output` | Output file path | Yes |
| `-i, --input` | Read data from text file | No |
| `-f, --format` | Output format (png, jpg, bmp, svg) | No (default: png) |
| `--error-correction` | Error correction level | No (default: medium) |
| `--scale` | Scale factor (1-10) | No (default: 3) |
| `--ratio` | Aspect ratio | No (default: 3) |
| `--columns` | Number of columns (1-30) | No (default: auto) |

*Either `DATA` or `--input` must be provided

---

## Examples

### 1. Simple Text

```bash
python main.py generate "Hello, World!" -o hello.png
```

### 2. Long Data

```bash
python main.py generate "This is a longer message with more data to encode in the PDF417 barcode" -o long.png
```

### 3. From File

```bash
# Create data file
echo "My barcode data" > data.txt

# Generate barcode
python main.py generate --input data.txt -o barcode.png
```

### 4. High Error Correction

```bash
python main.py generate "Important Data" -o secure.png --error-correction very_high
```

### 5. Large Barcode

```bash
python main.py generate "Data" -o large.png --scale 10
```

### 6. SVG Output

```bash
python main.py generate "Vector Data" -o barcode.svg --format svg
```

### 7. Custom Columns

```bash
python main.py generate "Data" -o custom.png --columns 10
```

---

## Error Correction Levels

| Level | Correction | Use Case |
|-------|------------|----------|
| `low` | ~3% | Clean environments, large barcodes |
| `medium` | ~15% | General use (default) |
| `high` | ~25% | Damaged or dirty surfaces |
| `very_high` | ~40% | Critical data, harsh conditions |

Higher error correction = larger barcode size

---

## Output Formats

### PNG (Recommended)
- **Pros:** Lossless, good compression, widely supported
- **Cons:** Larger file size than JPG
- **Use:** General purpose, web, printing

```bash
python main.py generate "Data" -o barcode.png --format png
```

### JPG
- **Pros:** Smaller file size
- **Cons:** Lossy compression (may affect scanning)
- **Use:** When file size is critical

```bash
python main.py generate "Data" -o barcode.jpg --format jpg
```

### SVG (Vector)
- **Pros:** Scalable, perfect quality at any size
- **Cons:** Not supported by all scanners
- **Use:** Printing, design work, large displays

```bash
python main.py generate "Data" -o barcode.svg --format svg
```

### BMP
- **Pros:** Uncompressed, maximum quality
- **Cons:** Very large file size
- **Use:** When quality is paramount

```bash
python main.py generate "Data" -o barcode.bmp --format bmp
```

---

## Python API

### Basic Usage

```python
from src.generator import generate_barcode

# Generate barcode
output_path = generate_barcode(
    data="Hello World",
    output_path="barcode.png",
    format="png",
    error_correction="medium"
)

print(f"Barcode saved to: {output_path}")
```

### From File

```python
from src.generator import generate_barcode_from_file

# Generate from text file
output_path = generate_barcode_from_file(
    input_path="data.txt",
    output_path="barcode.png",
    format="png"
)
```

### Advanced Usage

```python
from src.generator import BarcodeGenerator

# Create generator with custom settings
generator = BarcodeGenerator(
    error_correction='high',
    columns=8
)

# Generate multiple barcodes
for i, data in enumerate(data_list):
    generator.generate(
        data=data,
        output_path=f"barcode_{i}.png",
        scale=5,
        ratio=3
    )
```

---

## Best Practices

### 1. Choose Appropriate Error Correction

```bash
# For clean environments
python main.py generate "Data" -o barcode.png --error-correction low

# For general use
python main.py generate "Data" -o barcode.png --error-correction medium

# For harsh conditions
python main.py generate "Data" -o barcode.png --error-correction very_high
```

### 2. Optimize Barcode Size

```bash
# Smaller barcode (faster scanning)
python main.py generate "Data" -o small.png --scale 2 --columns 3

# Larger barcode (easier scanning)
python main.py generate "Data" -o large.png --scale 5 --columns 10
```

### 3. Test Scanning

Always test generated barcodes with your target scanner:

```bash
# Generate barcode
python main.py generate "Test Data" -o test.png

# Decode to verify
python main.py decode test.png
```

### 4. Use SVG for Printing

For high-quality printing, use SVG format:

```bash
python main.py generate "Print Data" -o print.svg --format svg --scale 5
```

---

## Troubleshooting

### Barcode Too Small

```bash
# Increase scale
python main.py generate "Data" -o barcode.png --scale 10
```

### Barcode Too Large

```bash
# Decrease scale or columns
python main.py generate "Data" -o barcode.png --scale 2 --columns 3
```

### Data Too Long

```bash
# Use higher error correction and more columns
python main.py generate "Very long data..." -o barcode.png --columns 15
```

### Scanning Issues

```bash
# Increase error correction
python main.py generate "Data" -o barcode.png --error-correction very_high

# Or increase scale
python main.py generate "Data" -o barcode.png --scale 8
```

---

## Integration Examples

### Web Application

```python
from flask import Flask, request, send_file
from src.generator import generate_barcode
import tempfile

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json['data']
    
    # Generate barcode
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        output_path = generate_barcode(data, tmp.name)
        return send_file(output_path, mimetype='image/png')
```

### Batch Generation

```python
from src.generator import BarcodeGenerator

generator = BarcodeGenerator(error_correction='high')

# Generate multiple barcodes
data_list = ["Data1", "Data2", "Data3"]

for i, data in enumerate(data_list):
    generator.generate(
        data=data,
        output_path=f"output/barcode_{i:03d}.png"
    )
```

### REST API Endpoint

Add to `src/api/server.py`:

```python
@app.post("/generate")
async def generate_barcode_endpoint(
    data: str,
    format: str = "png",
    error_correction: str = "medium"
):
    """Generate PDF417 barcode."""
    with tempfile.NamedTemporaryFile(suffix=f'.{format}', delete=False) as tmp:
        output_path = generate_barcode(
            data=data,
            output_path=tmp.name,
            format=format,
            error_correction=error_correction
        )
        return FileResponse(output_path, media_type=f'image/{format}')
```

---

## Specifications

### PDF417 Standard
- **Standard:** ISO/IEC 15438
- **Type:** Stacked linear barcode
- **Capacity:** Up to 1,850 ASCII characters
- **Error Correction:** Reed-Solomon
- **Columns:** 1-30 data columns
- **Rows:** 3-90 rows

### Supported Data
- ASCII characters
- Binary data
- Unicode (UTF-8)
- Numeric data
- Alphanumeric data

---

## Performance

### Generation Speed
- Small barcode (<100 chars): <0.1s
- Medium barcode (100-500 chars): <0.2s
- Large barcode (500-1000 chars): <0.5s

### File Sizes (approximate)
- PNG: 5-50 KB
- JPG: 2-20 KB
- SVG: 10-100 KB
- BMP: 50-500 KB

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
- Examples: See above

---

## Related Commands

```bash
# Generate and immediately decode
python main.py generate "Test" -o test.png && python main.py decode test.png

# Generate multiple formats
for fmt in png jpg svg; do
  python main.py generate "Data" -o barcode.$fmt --format $fmt
done

# Batch generate from file list
while read line; do
  python main.py generate "$line" -o "output_$(echo $line | md5sum | cut -d' ' -f1).png"
done < data_list.txt
```
