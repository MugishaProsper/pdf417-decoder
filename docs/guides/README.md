# Feature Guides

Complete guides for every feature in the PDF417 Decoder system.

---

## Core Features

### [Decoding Guide](DECODING_GUIDE.md)
Complete guide to decoding PDF417 barcodes from images.
- Basic and advanced decoding
- Understanding results
- Preprocessing methods
- Troubleshooting

### [Generation Guide](../GENERATOR_GUIDE.md)
Complete guide to generating PDF417 barcodes.
- Creating barcodes from text
- Multiple output formats
- Error correction levels
- Customization options

---

## Performance Features

### [Caching Guide](CACHING_GUIDE.md)
Intelligent result caching for 20x+ speedup.
- How caching works
- Cache management
- Performance impact
- Best practices

### [Batch Processing Guide](BATCH_PROCESSING_GUIDE.md)
Process multiple images efficiently.
- Directory processing
- Recursive scanning
- Progress tracking
- Error handling

### [Parallel Processing Guide](../PARALLEL_PROCESSING_GUIDE.md)
Multiprocessing for 2-8x speedup.
- Parallel vs sequential
- Worker management
- Performance optimization
- Memory considerations

---

## Quality Features

### [Quality Analysis Guide](QUALITY_ANALYSIS_GUIDE.md)
Analyze image quality and get recommendations.
- Quality metrics
- Issue detection
- Actionable recommendations
- Troubleshooting

### [Output Formats Guide](OUTPUT_FORMATS_GUIDE.md)
Export data in multiple formats.
- JSON, CSV, XML, TXT
- Format comparison
- Best practices
- Integration examples

---

## Configuration Features

### [Configuration Guide](CONFIGURATION_GUIDE.md)
Persistent settings via config files.
- YAML/JSON configuration
- Configuration options
- Environment-specific configs
- Best practices

### [Logging Guide](LOGGING_GUIDE.md)
Comprehensive logging system.
- Log levels
- Console and file logging
- Colored output
- Best practices

---

## Advanced Features

### [API Guide](../API_GUIDE.md)
REST API server with Docker support.
- Starting the server
- API endpoints
- Docker deployment
- Integration examples

### [Benchmarking Guide](../BENCHMARKING_GUIDE.md)
Performance benchmarking suite.
- Running benchmarks
- Understanding results
- Performance tracking
- CI/CD integration

---

## Quick Reference

### Common Tasks

**Decode single image:**
```bash
python main.py decode image.jpg
```

**Batch process directory:**
```bash
python main.py decode photos/ --batch --parallel
```

**Generate barcode:**
```bash
python main.py generate "Hello World" -o barcode.png
```

**Analyze quality:**
```bash
python main.py decode image.jpg --analyze
```

**Export to JSON:**
```bash
python main.py decode image.jpg --format json -o output.json
```

**Start API server:**
```bash
python main.py --serve
```

**Run benchmarks:**
```bash
python benchmarks/benchmark_suite.py
```

---

## Guide Index

| Guide | Feature | Complexity |
|-------|---------|------------|
| [Decoding](DECODING_GUIDE.md) | Barcode decoding | Basic |
| [Generation](../GENERATOR_GUIDE.md) | Barcode generation | Basic |
| [Caching](CACHING_GUIDE.md) | Result caching | Intermediate |
| [Batch Processing](BATCH_PROCESSING_GUIDE.md) | Multiple images | Intermediate |
| [Parallel Processing](../PARALLEL_PROCESSING_GUIDE.md) | Multiprocessing | Advanced |
| [Quality Analysis](QUALITY_ANALYSIS_GUIDE.md) | Image quality | Intermediate |
| [Output Formats](OUTPUT_FORMATS_GUIDE.md) | Export formats | Basic |
| [Configuration](CONFIGURATION_GUIDE.md) | Settings | Intermediate |
| [Logging](LOGGING_GUIDE.md) | Logging system | Intermediate |
| [API](../API_GUIDE.md) | REST API | Advanced |
| [Benchmarking](../BENCHMARKING_GUIDE.md) | Performance | Advanced |

---

## Getting Started

1. **New Users:** Start with [Decoding Guide](DECODING_GUIDE.md)
2. **Performance:** Read [Caching Guide](CACHING_GUIDE.md) and [Parallel Processing Guide](../PARALLEL_PROCESSING_GUIDE.md)
3. **Quality Issues:** Check [Quality Analysis Guide](QUALITY_ANALYSIS_GUIDE.md)
4. **Integration:** See [API Guide](../API_GUIDE.md)
5. **Production:** Review [Configuration Guide](CONFIGURATION_GUIDE.md) and [Logging Guide](LOGGING_GUIDE.md)

---

## Support

For issues or questions:
- GitHub Issues: [your-repo-url]
- Documentation: `docs/`
- Quick Reference: `docs/QUICK_REFERENCE.md`
