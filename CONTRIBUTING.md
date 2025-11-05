# Contributing to PDF417 Decoder

Thank you for your interest in contributing! Here are some guidelines to help you get started.

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

## Running Tests

```bash
python -m pytest tests/
```

Or run individual test files:
```bash
python -m unittest tests/test_decoder.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all public functions
- Keep functions focused and modular

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your fork
8. Submit a pull request

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Error messages
- Steps to reproduce
- Sample images (if applicable)

## Feature Requests

We welcome feature requests! Please open an issue describing:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered
