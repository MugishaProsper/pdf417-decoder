# Output Formats Guide

## Overview

Export decoded barcode data in multiple formats: JSON, CSV, XML, and TXT.

---

## Quick Start

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

---

## Supported Formats

### 1. JSON (Recommended)

**Best for:**
- Structured data
- API responses
- Data processing
- Web applications

**Features:**
- Complete metadata
- Nested structures
- Easy to parse
- Human-readable

### 2. CSV

**Best for:**
- Spreadsheet import
- Data analysis
- Excel/Google Sheets
- Tabular data

**Features:**
- Flat structure
- Easy to import
- Widely supported
- Compact

### 3. XML

**Best for:**
- Enterprise systems
- Legacy applications
- SOAP services
- Structured documents

**Features:**
- Hierarchical structure
- Schema validation
- Industry standard
- Self-describing

### 4. TXT (Plain Text)

**Best for:**
- Simple output
- Human reading
- Quick viewing
- Logging

**Features:**
- Simple format
- Easy to read
- No parsing needed
- Minimal size

---

## Format Examples

### JSON Format

```json
{
  "metadata": {
    "source": "barcode.jpg",
    "timestamp": "2025-11-08T10:00:00",
    "format": "json"
  },
  "results": [
    {
      "data": "BARCODE_DATA_HERE",
      "type": "PDF417",
      "quality": 85,
      "preprocess_method": "method_2",
      "rect": {
        "left": 10,
        "top": 20,
        "width": 100,
        "height": 50
      },
      "polygon": [
        {"x": 10, "y": 20},
        {"x": 110, "y": 20},
        {"x": 110, "y": 70},
        {"x": 10, "y": 70}
      ]
    }
  ],
  "count": 1
}
```

### CSV Format

```csv
barcode_id,data,type,quality,preprocess_method,rect_left,rect_top,rect_width,rect_height,data_length
1,BARCODE_DATA_HERE,PDF417,85,method_2,10,20,100,50,18
```

### XML Format

```xml
<?xml version="1.0" encoding="utf-8"?>
<pdf417_results>
  <metadata>
    <source>barcode.jpg</source>
    <timestamp>2025-11-08T10:00:00</timestamp>
  </metadata>
  <barcodes count="1">
    <barcode id="1">
      <data>BARCODE_DATA_HERE</data>
      <type>PDF417</type>
      <quality>85</quality>
      <preprocess_method>method_2</preprocess_method>
      <rectangle left="10" top="20" width="100" height="50"/>
    </barcode>
  </barcodes>
</pdf417_results>
```

### TXT Format

```
# Decoded at: 2025-11-08T10:00:00
# Source: barcode.jpg

--- Barcode 1 ---
Data: BARCODE_DATA_HERE

```

---

## Command-Line Usage

### Basic Usage

```bash
# Specify format
python main.py decode image.jpg --format json -o output.json
python main.py decode image.jpg --format csv -o output.csv
python main.py decode image.jpg --format xml -o output.xml
python main.py decode image.jpg --format txt -o output.txt
```

### Batch Processing

```bash
# Batch with JSON output
python main.py decode photos/ --batch --format json -o batch.json

# Batch with CSV output
python main.py decode photos/ --batch --format csv -o batch.csv
```

---

## Python API

### Basic Usage

```python
from src import decode_pdf417_from_image, export_results

# Decode image
results = decode_pdf417_from_image('barcode.jpg')

# Export to JSON
export_results(
    results,
    'output.json',
    format_type='json',
    metadata={'source': 'barcode.jpg'}
)

# Export to CSV
export_results(results, 'output.csv', format_type='csv')

# Export to XML
export_results(results, 'output.xml', format_type='xml')

# Export to TXT
export_results(results, 'output.txt', format_type='txt')
```

### Custom Metadata

```python
from src import export_results

metadata = {
    'source': 'barcode.jpg',
    'timestamp': '2025-11-08T10:00:00',
    'operator': 'John Doe',
    'location': 'Warehouse A',
    'batch_id': 'BATCH-001'
}

export_results(
    results,
    'output.json',
    format_type='json',
    metadata=metadata
)
```

---

## Format-Specific Features

### JSON Features

**Advantages:**
- Complete data structure
- Nested objects
- Arrays support
- Easy parsing

**Usage:**
```python
import json

# Read JSON
with open('results.json') as f:
    data = json.load(f)

# Access data
for result in data['results']:
    print(result['data'])
    print(result['quality'])
```

### CSV Features

**Advantages:**
- Spreadsheet compatible
- Flat structure
- Easy to analyze
- Compact

**Usage:**
```python
import csv

# Read CSV
with open('results.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['data'])
        print(row['quality'])
```

### XML Features

**Advantages:**
- Hierarchical structure
- Schema validation
- Industry standard
- Self-describing

**Usage:**
```python
import xml.etree.ElementTree as ET

# Read XML
tree = ET.parse('results.xml')
root = tree.getroot()

# Access data
for barcode in root.find('barcodes'):
    data = barcode.find('data').text
    quality = barcode.find('quality').text
    print(f"{data}: {quality}")
```

### TXT Features

**Advantages:**
- Human-readable
- Simple format
- No parsing needed
- Universal support

**Usage:**
```python
# Read TXT
with open('results.txt') as f:
    content = f.read()
    print(content)
```

---

## Advanced Usage

### Multiple Format Export

```python
from src import decode_pdf417_from_image, export_results

# Decode once
results = decode_pdf417_from_image('barcode.jpg')

# Export to multiple formats
formats = ['json', 'csv', 'xml', 'txt']
for fmt in formats:
    export_results(
        results,
        f'output.{fmt}',
        format_type=fmt
    )
```

### Custom Exporter

```python
from src.exporters import BaseExporter

class CustomExporter(BaseExporter):
    """Custom export format."""
    
    def export(self, results, output_path, metadata=None):
        """Export in custom format."""
        with open(output_path, 'w') as f:
            f.write("CUSTOM FORMAT\n")
            f.write("=" * 50 + "\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"\nBarcode {i}:\n")
                f.write(f"  Data: {result['data']}\n")
                f.write(f"  Quality: {result['quality']}\n")

# Use custom exporter
exporter = CustomExporter()
exporter.export(results, 'output.custom')
```

---

## Best Practices

1. **Choose appropriate format** for your use case
2. **Include metadata** for context
3. **Validate output** after export
4. **Use JSON** for APIs and data processing
5. **Use CSV** for spreadsheets and analysis
6. **Use XML** for enterprise systems
7. **Use TXT** for simple viewing

---

## Examples

### Example 1: Export to JSON

```python
from src import decode_pdf417_from_image, export_results

# Decode
results = decode_pdf417_from_image('barcode.jpg')

# Export with metadata
export_results(
    results,
    'output.json',
    format_type='json',
    metadata={
        'source': 'barcode.jpg',
        'timestamp': '2025-11-08T10:00:00',
        'count': len(results)
    }
)
```

### Example 2: Batch to CSV

```python
from src import decode_batch, export_results

# Process batch
batch_results = decode_batch('photos/')

# Flatten results
all_results = []
for batch in batch_results:
    for result in batch['results']:
        result['source_image'] = batch['image']
        all_results.append(result)

# Export to CSV
export_results(
    all_results,
    'batch_results.csv',
    format_type='csv'
)
```

### Example 3: Multiple Formats

```python
from src import decode_pdf417_from_image, export_results

results = decode_pdf417_from_image('barcode.jpg')

# Export to all formats
for fmt in ['json', 'csv', 'xml', 'txt']:
    output_file = f'results.{fmt}'
    export_results(results, output_file, format_type=fmt)
    print(f"Exported to {output_file}")
```

---

## Integration Examples

### Web API Response

```python
from flask import Flask, jsonify
from src import decode_pdf417_from_image

app = Flask(__name__)

@app.route('/decode', methods=['POST'])
def decode():
    # Decode image
    results = decode_pdf417_from_image('uploaded.jpg')
    
    # Return JSON response
    return jsonify({
        'success': len(results) > 0,
        'count': len(results),
        'results': [
            {
                'data': r['data'],
                'quality': r['quality']
            }
            for r in results
        ]
    })
```

### Excel Export

```python
import pandas as pd
from src import decode_batch

# Process batch
results = decode_batch('photos/')

# Convert to DataFrame
data = []
for batch in results:
    for result in batch['results']:
        data.append({
            'Image': batch['image'],
            'Data': result['data'],
            'Quality': result['quality'],
            'Method': result['preprocess_method']
        })

df = pd.DataFrame(data)

# Export to Excel
df.to_excel('results.xlsx', index=False)
```

---

## Related Guides

- [DECODING_GUIDE.md](DECODING_GUIDE.md) - Barcode decoding
- [BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md) - Batch processing
- [API_GUIDE.md](../API_GUIDE.md) - REST API

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
