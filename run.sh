#!/bin/bash
# Linux/Mac shell script to run the Medical AI application

echo "===================================="
echo "Medical AI POC - Starting Application"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate"
    echo "Then run: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "[1/3] Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        echo ""
        echo "[WARNING] .env file not found!"
        echo "Please copy env.example to .env and add your API keys"
        echo ""
        echo "Run: cp env.example .env"
        echo "Then edit .env with your keys"
        echo ""
        exit 1
    fi
fi

# Check if dependencies are installed
echo "[2/3] Checking dependencies..."
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] Dependencies not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "[3/3] Starting Streamlit application..."
echo ""
echo "Application will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app_streamlit.py

