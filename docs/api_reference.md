# API Reference

## Overview

The PDF417 Decoder REST API provides programmatic access to barcode decoding and image quality analysis.

**Base URL:** `http://localhost:8000`  
**API Version:** 1.0.0

---

## Authentication

Currently, the API does not require authentication. For production use, implement appropriate authentication mechanisms.

---

## Endpoints

### GET /

Root endpoint with API information.

**Response:**
```json
{
  "message": "PDF417 Decoder API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "cache_enabled": true
}
```

---

### POST /decode

Decode PDF417 barcode from uploaded image.

**Parameters:**
- `file` (form-data, required): Image file to decode
- `use_cache` (query, optional): Use caching (default: true)
- `show_preview` (query, optional): Show preview (not supported in API, default: false)

**Request:**
```bash
curl -X POST "http://localhost:8000/decode?use_cache=true" \
  -F "file=@barcode.jpg"
```

**Response:**
```json
{
  "success": true,
  "count": 1,
  "results": [
    {
      "data": "DECODED_BARCODE_DATA",
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
  "cache_hit": false,
  "filename": "barcode.jpg"
}
```

**Error Response:**
```json
{
  "detail": "Error processing image: ..."
}
```

---

### POST /analyze

Analyze image quality for barcode detection.

**Parameters:**
- `file` (form-data, required): Image file to analyze

**Request:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@image.jpg"
```

**Response:**
```json
{
  "success": true,
  "filename": "image.jpg",
  "overall_score": 0.75,
  "overall_quality": "good",
  "resolution": {
    "score": 1.0,
    "status": "good",
    "message": "Resolution: 1407x389",
    "width": 1407,
    "height": 389
  },
  "contrast": {
    "score": 0.68,
    "status": "good",
    "message": "Contrast: good (0.68)"
  },
  "sharpness": {
    "score": 0.52,
    "status": "moderate",
    "message": "Sharpness: moderate (0.52)"
  },
  "noise": {
    "score": 0.08,
    "status": "low",
    "message": "Noise: low (0.08)"
  },
  "brightness": {
    "score": 1.0,
    "status": "optimal",
    "message": "Brightness: optimal (0.48)"
  },
  "issues": [],
  "recommendations": [
    "Image quality is good for barcode detection"
  ]
}
```

---

### GET /cache/stats

Get cache statistics.

**Request:**
```bash
curl http://localhost:8000/cache/stats
```

**Response:**
```json
{
  "success": true,
  "total_entries": 15,
  "valid_entries": 12,
  "expired_entries": 3,
  "total_size_bytes": 2457600,
  "total_size_mb": 2.34
}
```

---

### DELETE /cache

Clear all cache entries.

**Request:**
```bash
curl -X DELETE http://localhost:8000/cache
```

**Response:**
```json
{
  "success": true,
  "message": "Cleared 15 cache entries"
}
```

---

## Interactive Documentation

The API provides interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Python Client Example

```python
import requests

# Decode barcode
with open('barcode.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/decode',
        files={'file': f}
    )
    
result = response.json()
if result['success']:
    for barcode in result['results']:
        print(f"Data: {barcode['data']}")
        print(f"Quality: {barcode['quality']}")

# Analyze quality
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze',
        files={'file': f}
    )
    
analysis = response.json()
print(f"Quality: {analysis['overall_quality']}")
print(f"Score: {analysis['overall_score']}")
```

---

## JavaScript Client Example

```javascript
// Decode barcode
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/decode', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      data.results.forEach(barcode => {
        console.log('Data:', barcode.data);
        console.log('Quality:', barcode.quality);
      });
    }
  });

// Analyze quality
fetch('http://localhost:8000/analyze', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    console.log('Quality:', data.overall_quality);
    console.log('Score:', data.overall_score);
  });
```

---

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t pdf417-decoder-api .

# Run container
docker run -d -p 8000:8000 --name pdf417-api pdf417-decoder-api

# Or use docker-compose
docker-compose up -d
```

### Environment Variables

- `LOG_LEVEL`: Logging level (default: INFO)

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid file type, etc.) |
| 500 | Internal Server Error |

---

## Best Practices

1. **Use caching** for repeated images to improve performance
2. **Validate file types** before uploading
3. **Handle errors** gracefully in your client code
4. **Monitor cache stats** to optimize cache TTL
5. **Use quality analysis** before batch processing

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `/docs`
