#!/usr/bin/env python3
"""Run the canonical application server with Flask debug logging enabled."""

import logging
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app import app  # noqa: E402


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=False, threaded=True)
