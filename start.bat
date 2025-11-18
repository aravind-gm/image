@echo off
REM Quick Start Script for Image Similarity Analyzer (Windows)

echo.
echo ============================================
echo  Image Similarity Analyzer - Quick Start
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/4] Installing dependencies...
echo This may take 3-5 minutes on first run...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Starting application...
echo.
echo ============================================
echo  Server running at: http://loca
lhost:5000
echo  Press Ctrl+C to stop
echo ============================================
echo.

python app.py

pause
