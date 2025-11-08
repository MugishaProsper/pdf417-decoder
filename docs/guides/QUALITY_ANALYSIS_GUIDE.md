# Image Quality Analysis Guide

## Overview

Analyze image quality to understand why barcode detection might fail and get actionable recommendations.

---

## Quick Start

```bash
# Analyze image quality
python main.py decode image.jpg --analyze

# Output includes:
# - Overall quality score
# - Resolution, contrast, sharpness, noise, brightness analysis
# - Detected issues
# - Actionable recommendations
```

---

## Command-Line Usage

```bash
# Basic quality analysis
python main.py decode image.jpg --analyze

# With verbose output
python main.py decode image.jpg --analyze --verbose

# Save analysis to file
python main.py decode image.jpg --analyze > analysis.txt
```

---

## Python API

### Basic Usage

```python
from src.quality_analyzer import analyze_image_quality

# Analyze image
analysis = analyze_image_quality('image.jpg')

# Get overall quality
print(f"Quality: {analysis['overall_quality']}")
print(f"Score: {analysis['overall_score']:.2f}/1.0")

# Check for issues
if analysis['issues']:
    print("Issues found:")
    for issue in analysis['issues']:
        print(f"  - {issue}")

# Get recommendations
print("\nRecommendations:")
for rec in analysis['recommendations']:
    print(f"  - {rec}")
```

### Detailed Analysis

```python
analysis = analyze_image_quality('image.jpg')

# Resolution
res = analysis['resolution']
print(f"Resolution: {res['width']}x{res['height']}")
print(f"Status: {res['status']}")

# Contrast
contrast = analysis['contrast']
print(f"Contrast: {contrast['score']:.2f} ({contrast['status']})")

# Sharpness
sharpness = analysis['sharpness']
print(f"Sharpness: {sharpness['score']:.2f} ({sharpness['status']})")

# Noise
noise = analysis['noise']
print(f"Noise: {noise['score']:.2f} ({noise['status']})")

# Brightness
brightness = analysis['brightness']
print(f"Brightness: {brightness['score']:.2f} ({brightness['status']})")
```

---

## Quality Metrics

### 1. Resolution

**What it measures:** Image dimensions

**Thresholds:**
- Good: ≥300x300 pixels
- Low: <300x300 pixels

**Recommendations:**
- Increase image resolution
- Use higher quality camera
- Scan at higher DPI

### 2. Contrast

**What it measures:** Difference between light and dark areas

**Thresholds:**
- Good: ≥0.6
- Moderate: 0.3-0.6
- Low: <0.3

**Recommendations:**
- Improve lighting conditions
- Adjust camera settings
- Increase contrast in post-processing

### 3. Sharpness

**What it measures:** Image focus and clarity

**Thresholds:**
- Sharp: ≥0.7
- Moderate: 0.4-0.7
- Blurry: <0.4

**Recommendations:**
- Ensure camera is focused
- Reduce motion blur
- Use tripod or stabilization
- Clean camera lens

### 4. Noise

**What it measures:** Random variations in brightness

**Thresholds:**
- Low: ≤0.1
- Moderate: 0.1-0.6
- High: >0.6

**Recommendations:**
- Reduce ISO/gain settings
- Improve lighting
- Use noise reduction
- Use better camera

### 5. Brightness

**What it measures:** Overall image brightness

**Thresholds:**
- Optimal: 0.4-0.6
- Acceptable: 0.3-0.7
- Too dark: <0.3
- Too bright: >0.7

**Recommendations:**
- Adjust exposure settings
- Add/reduce lighting
- Use flash or external light

---

## Understanding Results

### Overall Quality Score

Score range: 0.0 to 1.0

| Score | Rating | Description |
|-------|--------|-------------|
| 0.8-1.0 | Excellent | Ideal for barcode detection |
| 0.6-0.8 | Good | Should work well |
| 0.4-0.6 | Fair | May have issues |
| 0.0-0.4 | Poor | Likely to fail |

### Quality Ratings

- **excellent** - Perfect conditions
- **good** - Suitable for detection
- **fair** - Marginal, may work
- **poor** - Unlikely to work

---

## Common Issues and Solutions

### Issue: Low Resolution

**Symptoms:**
- Resolution < 300x300
- Barcode appears pixelated

**Solutions:**
```bash
# Check resolution
python main.py decode image.jpg --analyze

# Recommendations:
# - Scan at higher DPI (300+ recommended)
# - Use higher resolution camera
# - Move closer to barcode
```

### Issue: Low Contrast

**Symptoms:**
- Contrast score < 0.3
- Barcode blends with background

**Solutions:**
- Improve lighting
- Use flash
- Adjust camera exposure
- Post-process to increase contrast

### Issue: Blurry Image

**Symptoms:**
- Sharpness score < 0.4
- Barcode edges not clear

**Solutions:**
- Ensure proper focus
- Reduce camera shake
- Use faster shutter speed
- Clean lens

### Issue: High Noise

**Symptoms:**
- Noise score > 0.6
- Grainy appearance

**Solutions:**
- Reduce ISO settings
- Improve lighting
- Use better camera
- Apply noise reduction

### Issue: Poor Brightness

**Symptoms:**
- Too dark (< 0.3) or too bright (> 0.7)
- Details lost in shadows/highlights

**Solutions:**
- Adjust exposure
- Add/reduce lighting
- Use HDR mode
- Adjust camera settings

---

## Advanced Usage

### Batch Quality Analysis

```python
from pathlib import Path
from src.quality_analyzer import analyze_image_quality

def analyze_batch(directory):
    """Analyze quality of all images in directory."""
    results = []
    
    for image_path in Path(directory).glob('*.jpg'):
        try:
            analysis = analyze_image_quality(str(image_path))
            results.append({
                'image': str(image_path),
                'score': analysis['overall_score'],
                'quality': analysis['overall_quality'],
                'issues': analysis['issues']
            })
        except Exception as e:
            print(f"Error analyzing {image_path}: {e}")
    
    return results

# Analyze all images
results = analyze_batch('photos/')

# Find problematic images
poor_quality = [r for r in results if r['score'] < 0.4]
print(f"Found {len(poor_quality)} poor quality images")
```

### Quality-Based Filtering

```python
from src.quality_analyzer import analyze_image_quality

def should_process_image(image_path, min_score=0.5):
    """Check if image quality is sufficient."""
    analysis = analyze_image_quality(image_path)
    return analysis['overall_score'] >= min_score

# Filter images before processing
images = ['img1.jpg', 'img2.jpg', 'img3.jpg']
good_images = [img for img in images if should_process_image(img)]

print(f"Processing {len(good_images)}/{len(images)} images")
```

### Custom Quality Thresholds

```python
from src.quality_analyzer import ImageQualityAnalyzer
import cv2

# Load image
image = cv2.imread('barcode.jpg')

# Create analyzer
analyzer = ImageQualityAnalyzer(image)

# Override thresholds
analyzer.MIN_RESOLUTION = (400, 400)
analyzer.MIN_CONTRAST = 0.4
analyzer.MIN_SHARPNESS = 0.5

# Analyze with custom thresholds
analysis = analyzer.analyze()
```

---

## Integration Examples

### Pre-Processing Check

```python
from src.quality_analyzer import analyze_image_quality
from src import decode_pdf417_from_image

def decode_with_quality_check(image_path, min_score=0.5):
    """Decode only if quality is sufficient."""
    # Check quality first
    analysis = analyze_image_quality(image_path)
    
    if analysis['overall_score'] < min_score:
        print(f"Quality too low: {analysis['overall_score']:.2f}")
        print("Issues:", ', '.join(analysis['issues']))
        print("Recommendations:")
        for rec in analysis['recommendations']:
            print(f"  - {rec}")
        return None
    
    # Quality is good, proceed with decoding
    return decode_pdf417_from_image(image_path)
```

### Quality Report Generation

```python
from src.quality_analyzer import analyze_image_quality
import json

def generate_quality_report(image_paths, output_file):
    """Generate quality report for multiple images."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'images': []
    }
    
    for image_path in image_paths:
        analysis = analyze_image_quality(image_path)
        report['images'].append({
            'path': image_path,
            'score': analysis['overall_score'],
            'quality': analysis['overall_quality'],
            'issues': analysis['issues'],
            'recommendations': analysis['recommendations']
        })
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to {output_file}")
```

---

## Best Practices

1. **Analyze before batch processing** - Check quality of sample images
2. **Set quality thresholds** - Filter out poor quality images
3. **Log quality metrics** - Track quality over time
4. **Act on recommendations** - Improve image capture process
5. **Monitor trends** - Identify systematic quality issues

---

## Examples

### Example 1: Basic Analysis

```python
from src.quality_analyzer import analyze_image_quality

analysis = analyze_image_quality('barcode.jpg')

print(f"Overall: {analysis['overall_quality']} ({analysis['overall_score']:.2f})")

if analysis['issues']:
    print("\nIssues:")
    for issue in analysis['issues']:
        print(f"  ⚠️  {issue}")

print("\nRecommendations:")
for rec in analysis['recommendations']:
    print(f"  💡 {rec}")
```

### Example 2: Quality-Based Workflow

```python
from src.quality_analyzer import analyze_image_quality
from src import decode_pdf417_from_image

# Analyze quality
analysis = analyze_image_quality('barcode.jpg')

if analysis['overall_score'] >= 0.6:
    # Good quality - decode normally
    results = decode_pdf417_from_image('barcode.jpg')
elif analysis['overall_score'] >= 0.4:
    # Fair quality - try with preprocessing
    print("Fair quality - using enhanced preprocessing")
    results = decode_pdf417_from_image('barcode.jpg')
else:
    # Poor quality - recommend improvements
    print("Poor quality - please improve image:")
    for rec in analysis['recommendations']:
        print(f"  - {rec}")
    results = None
```

### Example 3: Batch Quality Check

```python
from pathlib import Path
from src.quality_analyzer import analyze_image_quality

def check_batch_quality(directory, min_score=0.5):
    """Check quality of all images in directory."""
    images = list(Path(directory).glob('*.jpg'))
    
    good = []
    poor = []
    
    for image_path in images:
        analysis = analyze_image_quality(str(image_path))
        
        if analysis['overall_score'] >= min_score:
            good.append(str(image_path))
        else:
            poor.append({
                'path': str(image_path),
                'score': analysis['overall_score'],
                'issues': analysis['issues']
            })
    
    print(f"Good quality: {len(good)}/{len(images)}")
    print(f"Poor quality: {len(poor)}/{len(images)}")
    
    if poor:
        print("\nPoor quality images:")
        for img in poor:
            print(f"  {img['path']}: {img['score']:.2f}")
            print(f"    Issues: {', '.join(img['issues'])}")
    
    return good, poor
```

---

## Related Guides

- [DECODING_GUIDE.md](DECODING_GUIDE.md) - Barcode decoding
- [BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md) - Batch processing
- [troubleshooting.md](../troubleshooting.md) - Troubleshooting

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
