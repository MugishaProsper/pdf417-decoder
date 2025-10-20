# API Server Guide

## Quick Start

### Start the Server

```bash
# Using CLI
python main.py --serve

# Custom port
python main.py --serve --port 8080

# Or directly
python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8000
```

### Access Documentation

Once the server is running:
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## Docker Deployment

### Using Docker

```bash
# Build image
docker build -t pdf417-decoder-api .

# Run container
docker run -d -p 8000:8000 --name pdf417-api pdf417-decoder-api

# View logs
docker logs -f pdf417-api

# Stop container
docker stop pdf417-api
```

### Using Docker Compose

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

---

## API Usage Examples

### Python Client

```python
import requests

# Decode barcode
with open('barcode.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/decode',
        files={'file': ('barcode.jpg', f, 'image/jpeg')}
    )

result = response.json()
print(f"Found {result['count']} barcode(s)")

for barcode in result['results']:
    print(f"Data: {barcode['data']}")
    print(f"Quality: {barcode['quality']}")

# Analyze quality
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze',
        files={'file': ('image.jpg', f, 'image/jpeg')}
    )

analysis = response.json()
print(f"Quality: {analysis['overall_quality']}")
print(f"Score: {analysis['overall_score']:.2f}")
print(f"Issues: {', '.join(analysis['issues']) or 'None'}")
```

### cURL Examples

```bash
# Decode barcode
curl -X POST "http://localhost:8000/decode" \
  -F "file=@barcode.jpg"

# Decode without cache
curl -X POST "http://localhost:8000/decode?use_cache=false" \
  -F "file=@barcode.jpg"

# Analyze quality
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@image.jpg"

# Get cache stats
curl http://localhost:8000/cache/stats

# Clear cache
curl -X DELETE http://localhost:8000/cache

# Health check
curl http://localhost:8000/health
```

### JavaScript/Fetch

```javascript
// Decode barcode
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/decode', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Found ${result.count} barcode(s)`);

result.results.forEach(barcode => {
  console.log('Data:', barcode.data);
  console.log('Quality:', barcode.quality);
});
```

### Axios (Node.js)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

// Decode barcode
const form = new FormData();
form.append('file', fs.createReadStream('barcode.jpg'));

axios.post('http://localhost:8000/decode', form, {
  headers: form.getHeaders()
})
  .then(response => {
    console.log(`Found ${response.data.count} barcode(s)`);
    response.data.results.forEach(barcode => {
      console.log('Data:', barcode.data);
    });
  })
  .catch(error => {
    console.error('Error:', error.response.data);
  });
```

---

## Response Formats

### Successful Decode

```json
{
  "success": true,
  "count": 1,
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
  "cache_hit": false,
  "filename": "barcode.jpg"
}
```

### No Barcodes Found

```json
{
  "success": true,
  "count": 0,
  "results": [],
  "cache_hit": false,
  "filename": "image.jpg"
}
```

### Quality Analysis

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
    "message": "Contrast: good (0.68)",
    "std_dev": 43.5
  },
  "sharpness": {
    "score": 0.52,
    "status": "moderate",
    "message": "Sharpness: moderate (0.52)",
    "variance": 260.3
  },
  "noise": {
    "score": 0.08,
    "status": "low",
    "message": "Noise: low (0.08)",
    "level": 0.08
  },
  "brightness": {
    "score": 1.0,
    "status": "optimal",
    "message": "Brightness: optimal (0.48)",
    "mean": 0.48
  },
  "issues": [],
  "recommendations": [
    "Image quality is good for barcode detection"
  ]
}
```

### Error Response

```json
{
  "detail": "Error processing image: Invalid image format"
}
```

---

## Production Deployment

### Environment Variables

```bash
# .env file
LOG_LEVEL=INFO
CACHE_TTL=86400
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for large files
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        
        # Increase max body size
        client_max_body_size 10M;
    }
}
```

### Systemd Service

```ini
# /etc/systemd/system/pdf417-api.service
[Unit]
Description=PDF417 Decoder API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/pdf417-decoder
Environment="PATH=/opt/pdf417-decoder/venv/bin"
ExecStart=/opt/pdf417-decoder/venv/bin/python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable pdf417-api
sudo systemctl start pdf417-api
sudo systemctl status pdf417-api
```

---

## Performance Tips

1. **Use caching** - Enabled by default, provides 20x+ speedup
2. **Monitor cache stats** - Adjust TTL based on usage patterns
3. **Limit file sizes** - Configure max upload size in nginx/proxy
4. **Use Docker** - Easier deployment and scaling
5. **Add rate limiting** - Protect against abuse
6. **Monitor logs** - Track errors and performance

---

## Security Considerations

1. **Add authentication** - Implement API keys or OAuth
2. **Rate limiting** - Prevent abuse
3. **Input validation** - Already implemented for file types
4. **HTTPS** - Use SSL/TLS in production
5. **CORS** - Configure allowed origins appropriately
6. **File size limits** - Prevent DoS attacks

---

## Troubleshooting

### Server won't start

```bash
# Check if port is in use
netstat -an | grep 8000

# Try different port
python main.py --serve --port 8080
```

### Import errors

```bash
# Install API dependencies
pip install fastapi uvicorn[standard] python-multipart pydantic
```

### Docker issues

```bash
# Check logs
docker logs pdf417-api

# Rebuild image
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Monitoring

### Health Check

```bash
# Simple health check
curl http://localhost:8000/health

# With monitoring tool
watch -n 5 'curl -s http://localhost:8000/health | jq'
```

### Cache Monitoring

```bash
# Check cache stats
curl http://localhost:8000/cache/stats | jq

# Monitor cache growth
watch -n 10 'curl -s http://localhost:8000/cache/stats | jq ".total_size_mb"'
```

---

## API Limits

- **Max file size:** 10MB (configurable)
- **Supported formats:** JPG, PNG, BMP, TIFF
- **Rate limit:** None (add middleware for production)
- **Concurrent requests:** Depends on server resources

---

## Support

- **Documentation:** http://localhost:8000/docs
- **GitHub Issues:** [your-repo-url]
- **API Reference:** `docs/api_reference.md`
