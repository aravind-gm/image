#!/bin/bash
# Quick Start Script for Image Similarity Analyzer (Linux/Mac)

echo ""
echo "============================================"
echo " Image Similarity Analyzer - Quick Start"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.9+ first"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

echo "[3/4] Installing dependencies..."
echo "This may take 3-5 minutes on first run..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[4/4] Starting application..."
echo ""
echo "============================================"
echo " Server running at: http://localhost:5000"
echo " Press Ctrl+C to stop"
echo "============================================"
echo ""

python app.py
