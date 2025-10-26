# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-11-08

### Added
- **Multiple Output Formats**: Support for JSON, CSV, and XML export formats
  - New `--format` CLI argument (txt, json, csv, xml)
  - Created `src/exporters.py` module with format-specific exporters
  - Comprehensive test suite for all export formats

- **Logging System**: Structured logging with colored console output
  - New `src/logger.py` module
  - `--log-level` argument (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - `--log-file` argument for file logging
  - Colored console output for better readability
  - Detailed logging throughout the codebase

- **Batch Processing**: Process multiple images at once
  - New `decode_batch()` function
  - `--batch` flag for directory processing
  - `--recursive` flag for subdirectory scanning
  - Progress bars using tqdm
  - Batch summary reporting
  - Support for multiple image formats

### Changed
- Restructured codebase into modular components
- Updated CLI to support new features
- Enhanced error handling and reporting
- Improved documentation

### Dependencies
- Added `tqdm>=4.65.0` for progress bars

## [1.0.0] - 2025-11-08

### Initial Release
- PDF417 barcode decoding with multiple preprocessing techniques
- Command-line interface
- Preview window support
- Basic text output
- Comprehensive documentation
