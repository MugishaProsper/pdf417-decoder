# Troubleshooting Guide

## pyzbar Installation Issues on Windows

### Problem: DLL Not Found Error

```
FileNotFoundError: Could not find module 'libzbar-64.dll'
```

### Solutions

#### Method 1: Install Visual C++ Redistributable (Recommended)

1. Download [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Install the redistributable
3. Restart your terminal/IDE
4. Try running the decoder again

#### Method 2: Use Conda

```bash
conda install -c conda-forge pyzbar
```

#### Method 3: Use Alternative Package

```bash
pip uninstall pyzbar
pip install pyzbar-upright
```

#### Method 4: Manual DLL Installation

1. Download zbar DLLs from the [official repository](https://github.com/NuGet/Home/issues/2685)
2. Place DLLs in your Python's `site-packages/pyzbar` directory
3. Restart your application

## No Barcodes Detected

### Possible Causes

1. **Image Quality**: Low resolution or poor contrast
2. **Barcode Type**: Ensure the image contains PDF417 barcodes
3. **Image Format**: Some formats may not be supported

### Solutions

- Increase image resolution (minimum 300 DPI recommended)
- Enhance image contrast before processing
- Try the `--show` flag to visualize detection attempts
- Use the `--verbose` flag for detailed debugging information

## Import Errors

### Problem: Module Not Found

```
ModuleNotFoundError: No module named 'cv2'
```

### Solution

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Performance Issues

### Problem: Slow Processing

The decoder tries multiple preprocessing methods, which can be slow for large images.

### Solutions

- Resize large images before processing
- Process images in batch mode
- Consider using a subset of preprocessing methods

## Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/yourusername/pdf417-decoder/issues)
2. Create a new issue with:
   - Your Python version
   - Operating system
   - Error message
   - Sample image (if possible)
