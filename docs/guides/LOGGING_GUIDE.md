# Logging System Guide

## Overview

Comprehensive logging system with colored console output and file logging for debugging and monitoring.

---

## Quick Start

```bash
# Default logging (INFO level)
python main.py decode image.jpg

# Debug logging
python main.py decode image.jpg --log-level DEBUG

# Log to file
python main.py decode image.jpg --log-file logs/decode.log

# Both console and file
python main.py decode image.jpg --log-level DEBUG --log-file logs/debug.log
```

---

## Log Levels

### Available Levels

1. **DEBUG** - Detailed debugging information
2. **INFO** - General information (default)
3. **WARNING** - Warning messages
4. **ERROR** - Error messages
5. **CRITICAL** - Critical errors

### When to Use Each Level

**DEBUG:**
- Development and troubleshooting
- Detailed operation tracking
- Performance analysis

**INFO:**
- Normal operation messages
- Progress updates
- Success confirmations

**WARNING:**
- Potential issues
- Deprecated features
- Non-critical problems

**ERROR:**
- Operation failures
- Exception handling
- Critical issues

**CRITICAL:**
- System failures
- Unrecoverable errors
- Emergency situations

---

## Command-Line Usage

### Basic Logging

```bash
# Set log level
python main.py decode image.jpg --log-level DEBUG
python main.py decode image.jpg --log-level INFO
python main.py decode image.jpg --log-level WARNING

# Log to file
python main.py decode image.jpg --log-file logs/app.log

# Both
python main.py decode image.jpg --log-level DEBUG --log-file logs/debug.log
```

### Log Output Examples

**INFO Level:**
```
INFO - Processing image: barcode.jpg
INFO - Decoding completed in 0.142s - found 1 barcode(s)
INFO - Results exported to output.json
```

**DEBUG Level:**
```
DEBUG - Loading image: barcode.jpg
DEBUG - Image loaded successfully: (389, 1407, 3)
DEBUG - Starting preprocessing
DEBUG - Generated 7 preprocessed versions
DEBUG - Trying preprocessing method 0
DEBUG - Trying preprocessing method 1
DEBUG - Method 2 found 1 barcode(s)
DEBUG - Found 1 total results before deduplication
DEBUG - After deduplication: 1 unique results
INFO - Decoding completed in 0.142s - found 1 barcode(s)
```

---

## Python API

### Basic Usage

```python
from src.logger import setup_logger, get_logger

# Setup logger
logger = setup_logger(level='INFO', console=True)

# Get logger in your module
logger = get_logger(__name__)

# Log messages
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical error")
```

### File Logging

```python
from src.logger import setup_logger

# Log to file
logger = setup_logger(
    level='DEBUG',
    log_file='logs/app.log',
    console=True
)

# Now all logs go to both console and file
logger.info("This goes to console and file")
```

### Custom Logger

```python
from src.logger import setup_logger

# Create custom logger
logger = setup_logger(
    name='my_module',
    level='DEBUG',
    log_file='logs/my_module.log',
    console=True
)

logger.info("Custom logger message")
```

---

## Log Format

### Console Format

```
LEVEL - message
```

Example:
```
INFO - Processing image: barcode.jpg
DEBUG - Method 2 found 1 barcode(s)
ERROR - Error processing image: File not found
```

### File Format

```
timestamp - name - LEVEL - function:line - message
```

Example:
```
2025-11-08 10:30:00 - pdf417_decoder - INFO - decode_pdf417_from_image:45 - Processing image: barcode.jpg
2025-11-08 10:30:01 - pdf417_decoder - DEBUG - decode_pdf417_from_image:78 - Method 2 found 1 barcode(s)
```

---

## Colored Console Output

### Color Scheme

- **DEBUG:** Cyan
- **INFO:** Green
- **WARNING:** Yellow
- **ERROR:** Red
- **CRITICAL:** Magenta

### Disable Colors

Colors are automatically disabled when:
- Output is redirected to file
- Terminal doesn't support colors
- Running in non-TTY environment

---

## Configuration

### Via Configuration File

```yaml
# .pdf417rc
logging:
  level: DEBUG
  file: logs/app.log
```

### Via Environment Variables

```bash
# Set log level
export PDF417_LOG_LEVEL=DEBUG

# Set log file
export PDF417_LOG_FILE=logs/app.log

# Run application
python main.py decode image.jpg
```

---

## Advanced Usage

### Structured Logging

```python
from src.logger import get_logger

logger = get_logger(__name__)

# Log with context
logger.info(
    "Decoded barcode",
    extra={
        'image': 'barcode.jpg',
        'barcodes_found': 1,
        'processing_time': 0.142
    }
)
```

### Exception Logging

```python
from src.logger import get_logger

logger = get_logger(__name__)

try:
    results = decode_pdf417_from_image('image.jpg')
except Exception as e:
    logger.error(f"Error decoding image: {e}", exc_info=True)
    # exc_info=True includes full traceback
```

### Performance Logging

```python
import time
from src.logger import get_logger

logger = get_logger(__name__)

start_time = time.time()

# Operation
results = decode_pdf417_from_image('image.jpg')

elapsed = time.time() - start_time
logger.info(f"Decoding completed in {elapsed:.3f}s")
```

---

## Log Rotation

### Manual Rotation

```python
import logging
from logging.handlers import RotatingFileHandler
from src.logger import get_logger

# Create rotating file handler
handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)

# Add to logger
logger = get_logger(__name__)
logger.addHandler(handler)
```

### Time-Based Rotation

```python
from logging.handlers import TimedRotatingFileHandler

# Rotate daily
handler = TimedRotatingFileHandler(
    'logs/app.log',
    when='midnight',
    interval=1,
    backupCount=7
)

logger = get_logger(__name__)
logger.addHandler(handler)
```

---

## Best Practices

1. **Use appropriate log levels** - Don't log everything as ERROR
2. **Include context** - Add relevant information to log messages
3. **Log exceptions** - Use exc_info=True for tracebacks
4. **Rotate log files** - Prevent unlimited growth
5. **Monitor logs** - Set up log monitoring and alerts
6. **Structured logging** - Use consistent format
7. **Performance logging** - Track operation times

---

## Examples

### Example 1: Basic Logging

```python
from src.logger import get_logger

logger = get_logger(__name__)

logger.info("Starting barcode decoding")

try:
    results = decode_pdf417_from_image('barcode.jpg')
    logger.info(f"Found {len(results)} barcode(s)")
except Exception as e:
    logger.error(f"Decoding failed: {e}")
```

### Example 2: Debug Logging

```python
from src.logger import setup_logger, get_logger

# Enable debug logging
setup_logger(level='DEBUG', log_file='logs/debug.log')

logger = get_logger(__name__)

logger.debug("Loading image")
image = cv2.imread('barcode.jpg')
logger.debug(f"Image shape: {image.shape}")

logger.debug("Starting preprocessing")
processed = preprocess_image(image)
logger.debug(f"Generated {len(processed)} versions")

logger.debug("Decoding barcodes")
results = decode_pdf417_from_image('barcode.jpg')
logger.debug(f"Found {len(results)} results")
```

### Example 3: Production Logging

```python
from src.logger import setup_logger, get_logger
import time

# Setup production logging
setup_logger(
    level='INFO',
    log_file='/var/log/pdf417/app.log',
    console=False  # No console output in production
)

logger = get_logger(__name__)

def process_barcode(image_path):
    """Process barcode with logging."""
    start_time = time.time()
    
    logger.info(f"Processing: {image_path}")
    
    try:
        results = decode_pdf417_from_image(image_path)
        
        elapsed = time.time() - start_time
        logger.info(
            f"Success: {image_path} - "
            f"{len(results)} barcode(s) in {elapsed:.3f}s"
        )
        
        return results
        
    except Exception as e:
        logger.error(
            f"Failed: {image_path} - {e}",
            exc_info=True
        )
        return None
```

---

## Troubleshooting

### Logs Not Appearing

**Check:**
1. Log level is appropriate
2. Logger is properly initialized
3. Console output not redirected
4. File permissions for log file

**Debug:**
```python
import logging

# Check current log level
logger = logging.getLogger('pdf417_decoder')
print(f"Log level: {logger.level}")

# Check handlers
print(f"Handlers: {logger.handlers}")
```

### Log File Not Created

**Check:**
1. Directory exists
2. Write permissions
3. Disk space available
4. Path is correct

**Solution:**
```python
from pathlib import Path

# Ensure log directory exists
log_file = 'logs/app.log'
Path(log_file).parent.mkdir(parents=True, exist_ok=True)

# Setup logger
setup_logger(log_file=log_file)
```

### Too Many Log Messages

**Solutions:**
```bash
# Increase log level
python main.py decode image.jpg --log-level WARNING

# Or filter in code
logger.setLevel(logging.WARNING)
```

---

## Integration Examples

### Web Application

```python
from flask import Flask
from src.logger import setup_logger, get_logger

app = Flask(__name__)

# Setup logging
setup_logger(
    level='INFO',
    log_file='logs/web.log',
    console=True
)

logger = get_logger(__name__)

@app.route('/decode', methods=['POST'])
def decode():
    logger.info(f"Decode request from {request.remote_addr}")
    
    try:
        # Process request
        results = decode_pdf417_from_image(file)
        logger.info(f"Decoded {len(results)} barcode(s)")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Decode error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
```

### Monitoring Integration

```python
from src.logger import get_logger
import sentry_sdk

# Initialize Sentry
sentry_sdk.init("your-dsn")

logger = get_logger(__name__)

try:
    results = decode_pdf417_from_image('image.jpg')
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    sentry_sdk.capture_exception(e)
```

---

## Related Guides

- [DECODING_GUIDE.md](DECODING_GUIDE.md) - Barcode decoding
- [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) - Configuration
- [BENCHMARKING_GUIDE.md](../BENCHMARKING_GUIDE.md) - Performance monitoring

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
