#!/usr/bin/env python3
"""Script to run performance benchmarks."""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from benchmarks.benchmark_suite import main

if __name__ == "__main__":
    main()
