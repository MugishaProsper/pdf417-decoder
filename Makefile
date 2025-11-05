.PHONY: help install test clean lint format run

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make run        - Run the decoder (requires IMAGE variable)"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ -v --cov=src

lint:
	flake8 src/ tests/
	mypy src/
	pylint src/

format:
	black src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	@if [ -z "$(IMAGE)" ]; then \
		echo "Usage: make run IMAGE=path/to/image.jpg"; \
	else \
		python main.py $(IMAGE) $(ARGS); \
	fi
