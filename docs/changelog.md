# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-11-08

### Added - Phase 2 Features

- **Caching System**: Intelligent result caching for faster repeated processing
  - New `src/cache.py` module with file hash-based caching
  - `--no-cache` flag to bypass cache
  - `--clear-cache` command to clear all cached results
  - `--cache-stats` command to view cache statistics
  - TTL-based cache expiration (default: 24 hours)
  - Automatic cache directory management

- **Image Quality Analysis**: Comprehensive quality assessment
  - New `src/quality_analyzer.py` module
  - `--analyze` flag for detailed quality reports
  - Analyzes resolution, contrast, sharpness, noise, and brightness
  - Overall quality scoring (0-1 scale)
  - Actionable recommendations for improving image quality
  - Identifies specific issues preventing successful detection

- **Configuration File Support**: Persistent settings management
  - New `src/config.py` module
  - Support for YAML and JSON configuration files
  - `--config` flag to specify custom config file
  - Auto-loads from `.pdf417rc`, `config.yaml`, or `config.json`
  - Dot notation for nested configuration access
  - Created `config.example.yaml` template
  - CLI arguments override config file settings

### Changed
- Enhanced CLI with new quality analysis and caching features
- Improved error handling and user feedback
- Updated documentation with new features

### Dependencies
- Added `pyyaml>=6.0` for YAML configuration support

---

## [1.1.0] - 2025-11-08

### Added - Phase 1 Features

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

---

## [1.0.0] - 2025-11-08

### Initial Release
- PDF417 barcode decoding with multiple preprocessing techniques
- Command-line interface
- Preview window support
- Basic text output
- Comprehensive documentation
