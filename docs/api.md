# API Documentation

## Core Functions

### decode_pdf417_from_image

Decode all PDF417 barcodes in an image with robust preprocessing.

```python
def decode_pdf417_from_image(
    image_path: str, 
    show_preview: bool = False
) -> List[Dict]
```

**Parameters:**
- `image_path` (str): Path to the image file
- `show_preview` (bool, optional): Whether to display a preview window. Default: False

**Returns:**
- List[Dict]: List of decoded barcode data with metadata

**Raises:**
- `FileNotFoundError`: If image file doesn't exist
- `ValueError`: If image cannot be loaded
- `RuntimeError`: If pyzbar is not available

**Example:**
```python
from src.decoder import decode_pdf417_from_image

results = decode_pdf417_from_image("barcode.jpg", show_preview=True)
for result in results:
    print(result['data'])
```

### preprocess_image

Apply multiple preprocessing techniques to improve detection.

```python
def preprocess_image(image: np.ndarray) -> List[np.ndarray]
```

**Parameters:**
- `image` (np.ndarray): Input image as numpy array

**Returns:**
- List[np.ndarray]: List of processed images

**Example:**
```python
import cv2
from src.preprocessing import preprocess_image

image = cv2.imread("barcode.jpg")
processed_images = preprocess_image(image)
```

## Result Format

Each decoded barcode returns a dictionary with the following structure:

```python
{
    'data': str,                    # Decoded barcode data
    'type': str,                    # Barcode type (PDF417)
    'rect': Rect,                   # Bounding rectangle (left, top, width, height)
    'polygon': List[Point],         # Polygon points defining barcode boundary
    'quality': int,                 # Detection quality score (0-100)
    'preprocess_method': str        # Which preprocessing method succeeded
}
```

## CLI Usage

The command-line interface is available through `main.py`:

```bash
python main.py [OPTIONS] IMAGE_PATH
```

**Options:**
- `-o, --output FILE`: Save decoded data to file
- `--show`: Show preview window with detected barcodes
- `--verbose`: Print detailed information
- `--version`: Show version information
- `-h, --help`: Show help message

**Examples:**

```bash
# Basic usage
python main.py image.jpg

# With preview
python main.py image.jpg --show

# Save output
python main.py image.jpg -o output.txt

# Verbose mode
python main.py image.jpg --verbose
```
