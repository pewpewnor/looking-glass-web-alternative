#!/bin/bash

# Looking Glass Web Alternative - Quick Start Script

echo "========================================="
echo "Looking Glass Web Alternative"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or later."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

echo ""
echo "Starting Flask server on http://localhost:5001..."
echo "========================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

python3 app.py
