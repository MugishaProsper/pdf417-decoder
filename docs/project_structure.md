# Project Structure

This document describes the organization of the PDF417 Decoder codebase.

## Directory Layout

```
pdf417-decoder/
├── src/                        # Source code package
│   ├── __init__.py            # Package initialization and exports
│   ├── cli.py                 # Command-line interface
│   ├── decoder.py             # Core decoding logic
│   └── preprocessing.py       # Image preprocessing utilities
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_decoder.py        # Tests for decoder module
│   └── test_preprocessing.py  # Tests for preprocessing module
│
├── docs/                       # Documentation
│   ├── api.md                 # API documentation
│   ├── troubleshooting.md     # Common issues and solutions
│   └── project_structure.md   # This file
│
├── assets/                     # Sample images and resources
│   ├── .gitkeep               # Keep directory in git
│   └── sample_img.jpg         # Sample barcode image
│
├── main.py                     # Main entry point
├── setup.py                    # Package installation configuration
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── README.md                   # Project overview and usage
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
├── .gitignore                  # Git ignore rules
├── .editorconfig              # Editor configuration
└── Makefile                    # Build automation commands
```

## Module Descriptions

### src/decoder.py
Core barcode decoding functionality. Contains:
- `decode_pdf417_from_image()`: Main decoding function
- `_remove_duplicates()`: Helper to remove duplicate detections
- `_show_preview()`: Display preview window

### src/preprocessing.py
Image preprocessing utilities. Contains:
- `preprocess_image()`: Apply multiple preprocessing techniques

### src/cli.py
Command-line interface implementation. Contains:
- `parse_args()`: Argument parsing
- `main()`: CLI entry point

### src/__init__.py
Package initialization that exports public API:
- `decode_pdf417_from_image`
- `preprocess_image`

## Design Principles

### Separation of Concerns
- **Decoder**: Handles barcode detection and decoding
- **Preprocessing**: Handles image manipulation
- **CLI**: Handles user interaction and I/O

### Modularity
Each module can be imported and used independently:

```python
# Use just the decoder
from src.decoder import decode_pdf417_from_image

# Use just preprocessing
from src.preprocessing import preprocess_image
```

### Testability
- All core logic is in separate modules
- Functions are small and focused
- Dependencies are minimal and explicit

## Testing Structure

Tests mirror the source structure:
- `tests/test_decoder.py` → `src/decoder.py`
- `tests/test_preprocessing.py` → `src/preprocessing.py`

Run tests with:
```bash
python -m pytest tests/
```

## Documentation Structure

- **README.md**: Quick start and basic usage
- **docs/api.md**: Detailed API reference
- **docs/troubleshooting.md**: Common issues and solutions
- **docs/project_structure.md**: Architecture overview
- **CONTRIBUTING.md**: Development guidelines

## Entry Points

### Command Line
```bash
python main.py image.jpg
```

### Python Module
```python
from src.decoder import decode_pdf417_from_image
results = decode_pdf417_from_image("image.jpg")
```

### Installed Package
After running `pip install -e .`:
```bash
pdf417-decode image.jpg
```

## Configuration Files

- **.gitignore**: Excludes build artifacts, virtual environments, etc.
- **.editorconfig**: Ensures consistent coding style across editors
- **setup.py**: Defines package metadata and dependencies
- **Makefile**: Provides convenient commands for common tasks

## Adding New Features

1. Add implementation to appropriate module in `src/`
2. Add tests to corresponding file in `tests/`
3. Update API documentation in `docs/api.md`
4. Update README.md if user-facing
5. Add entry to CHANGELOG (if exists)
