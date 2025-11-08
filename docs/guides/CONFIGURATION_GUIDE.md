# Configuration Guide

## Overview

Configure the PDF417 decoder using YAML or JSON configuration files for persistent settings.

---

## Quick Start

```bash
# Create configuration file
cp config.example.yaml .pdf417rc

# Edit configuration
nano .pdf417rc

# Use configuration (auto-loaded)
python main.py decode image.jpg

# Or specify custom config
python main.py decode image.jpg --config myconfig.yaml
```

---

## Configuration File Locations

The decoder looks for configuration files in this order:

1. File specified with `--config` flag
2. `.pdf417rc` in current directory
3. `.pdf417rc.yaml` in current directory
4. `.pdf417rc.json` in current directory
5. `config.yaml` in current directory
6. `config.json` in current directory

---

## Configuration Format

### YAML Format (Recommended)

```yaml
# .pdf417rc
preprocessing:
  methods: all
  enabled: true

output:
  format: json
  verbose: false

cache:
  enabled: true
  ttl: 86400
  directory: .cache

batch:
  recursive: false
  show_progress: true

logging:
  level: INFO
  file: null
```

### JSON Format

```json
{
  "preprocessing": {
    "methods": "all",
    "enabled": true
  },
  "output": {
    "format": "json",
    "verbose": false
  },
  "cache": {
    "enabled": true,
    "ttl": 86400,
    "directory": ".cache"
  },
  "batch": {
    "recursive": false,
    "show_progress": true
  },
  "logging": {
    "level": "INFO",
    "file": null
  }
}
```

---

## Configuration Options

### Preprocessing

```yaml
preprocessing:
  methods: all          # 'all' or list of method indices [0-6]
  enabled: true         # Enable/disable preprocessing
```

**Options:**
- `methods`: Which preprocessing methods to use
  - `all`: Use all 7 methods (default)
  - `[0, 1, 2]`: Use specific methods
- `enabled`: Enable/disable preprocessing

### Output

```yaml
output:
  format: json          # txt, json, csv, xml
  verbose: false        # Verbose output
```

**Options:**
- `format`: Default output format
  - `txt`: Plain text (default)
  - `json`: JSON format
  - `csv`: CSV format
  - `xml`: XML format
- `verbose`: Include detailed information

### Cache

```yaml
cache:
  enabled: true         # Enable/disable caching
  ttl: 86400           # Time-to-live in seconds (24 hours)
  directory: .cache    # Cache directory
```

**Options:**
- `enabled`: Enable/disable caching
- `ttl`: Cache entry lifetime in seconds
  - `3600`: 1 hour
  - `86400`: 24 hours (default)
  - `604800`: 1 week
- `directory`: Where to store cache files

### Batch Processing

```yaml
batch:
  recursive: false      # Recursively process subdirectories
  show_progress: true   # Show progress bar
```

**Options:**
- `recursive`: Include subdirectories
- `show_progress`: Display progress bar

### Logging

```yaml
logging:
  level: INFO          # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: null           # Log file path (null for no file)
```

**Options:**
- `level`: Logging level
  - `DEBUG`: Detailed debugging information
  - `INFO`: General information (default)
  - `WARNING`: Warning messages
  - `ERROR`: Error messages
  - `CRITICAL`: Critical errors
- `file`: Log file path
  - `null`: No file logging
  - `logs/app.log`: Log to file

---

## Command-Line Usage

### Using Configuration

```bash
# Auto-load from .pdf417rc
python main.py decode image.jpg

# Specify custom config
python main.py decode image.jpg --config myconfig.yaml

# Override config with CLI args
python main.py decode image.jpg --format csv  # Overrides config format
```

### CLI Arguments Override Config

CLI arguments always take precedence over configuration file settings.

```bash
# Config says format: json
# CLI says format: csv
# Result: CSV format is used
python main.py decode image.jpg --format csv
```

---

## Python API

### Loading Configuration

```python
from src.config import load_config

# Load default config
config = load_config()

# Load custom config
config = load_config('myconfig.yaml')

# Get values
format = config.get('output.format')
cache_enabled = config.get('cache.enabled')
log_level = config.get('logging.level')
```

### Accessing Configuration

```python
# Dot notation
format = config.get('output.format')
ttl = config.get('cache.ttl')

# With default value
workers = config.get('batch.workers', 4)

# Nested access
preprocessing_methods = config.get('preprocessing.methods')
```

### Setting Configuration

```python
# Set value
config.set('output.format', 'json')
config.set('cache.ttl', 3600)

# Save to file
config.save('myconfig.yaml')
```

---

## Configuration Examples

### Example 1: Development Config

```yaml
# dev.yaml
output:
  format: json
  verbose: true

cache:
  enabled: false  # Disable cache for testing

logging:
  level: DEBUG
  file: logs/dev.log

batch:
  show_progress: true
```

### Example 2: Production Config

```yaml
# prod.yaml
output:
  format: json
  verbose: false

cache:
  enabled: true
  ttl: 86400
  directory: /var/cache/pdf417

logging:
  level: WARNING
  file: /var/log/pdf417/app.log

batch:
  recursive: true
  show_progress: false
```

### Example 3: High Performance Config

```yaml
# performance.yaml
preprocessing:
  methods: [0, 1, 2]  # Use only fast methods

output:
  format: json
  verbose: false

cache:
  enabled: true
  ttl: 604800  # 1 week

batch:
  recursive: true
  show_progress: true
```

---

## Advanced Usage

### Environment-Specific Configs

```bash
# Development
python main.py decode image.jpg --config config.dev.yaml

# Staging
python main.py decode image.jpg --config config.staging.yaml

# Production
python main.py decode image.jpg --config config.prod.yaml
```

### Dynamic Configuration

```python
from src.config import Config

# Create config programmatically
config = Config()

# Set values
config.set('output.format', 'json')
config.set('cache.enabled', True)
config.set('logging.level', 'DEBUG')

# Save
config.save('dynamic.yaml')
```

### Configuration Validation

```python
from src.config import load_config

def validate_config(config):
    """Validate configuration values."""
    # Check format
    valid_formats = ['txt', 'json', 'csv', 'xml']
    format = config.get('output.format')
    if format not in valid_formats:
        raise ValueError(f"Invalid format: {format}")
    
    # Check TTL
    ttl = config.get('cache.ttl')
    if ttl < 0:
        raise ValueError(f"Invalid TTL: {ttl}")
    
    # Check log level
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    level = config.get('logging.level')
    if level not in valid_levels:
        raise ValueError(f"Invalid log level: {level}")
    
    return True

# Load and validate
config = load_config('myconfig.yaml')
validate_config(config)
```

---

## Best Practices

1. **Use YAML format** - More readable than JSON
2. **Version control configs** - Track configuration changes
3. **Environment-specific configs** - Separate dev/staging/prod
4. **Document custom settings** - Add comments to explain
5. **Validate configuration** - Check values before use
6. **Use defaults wisely** - Override only what's needed
7. **Secure sensitive data** - Don't commit secrets

---

## Troubleshooting

### Config Not Loading

**Check:**
1. File exists in expected location
2. File has correct extension (.yaml, .yml, .json)
3. File has valid syntax
4. File is readable

**Debug:**
```bash
# Enable debug logging
python main.py decode image.jpg --log-level DEBUG

# Check for config loading messages
```

### Invalid Configuration

**Symptoms:**
- Error messages about invalid values
- Unexpected behavior

**Solutions:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.pdf417rc'))"

# Validate JSON syntax
python -c "import json; json.load(open('config.json'))"
```

### CLI Args Not Overriding

**Check:**
- CLI arguments are specified correctly
- Configuration is being loaded
- No typos in argument names

---

## Examples

### Example 1: Basic Configuration

```yaml
# .pdf417rc
output:
  format: json

cache:
  enabled: true
  ttl: 86400

logging:
  level: INFO
```

```bash
# Use configuration
python main.py decode image.jpg
```

### Example 2: Custom Configuration

```python
from src.config import load_config
from src import decode_pdf417_from_image

# Load custom config
config = load_config('myconfig.yaml')

# Use config values
format = config.get('output.format', 'txt')
verbose = config.get('output.verbose', False)

# Decode
results = decode_pdf417_from_image('image.jpg')

# Export using config format
from src import export_results
export_results(results, f'output.{format}', format_type=format)
```

### Example 3: Multiple Environments

```bash
# Development
export PDF417_CONFIG=config.dev.yaml
python main.py decode image.jpg --config $PDF417_CONFIG

# Production
export PDF417_CONFIG=config.prod.yaml
python main.py decode image.jpg --config $PDF417_CONFIG
```

---

## Related Guides

- [DECODING_GUIDE.md](DECODING_GUIDE.md) - Barcode decoding
- [CACHING_GUIDE.md](CACHING_GUIDE.md) - Caching system
- [LOGGING_GUIDE.md](LOGGING_GUIDE.md) - Logging system

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
