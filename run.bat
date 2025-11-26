@echo off
REM Windows 

echo ====================================
echo Medical AI POC - Starting Application
echo ====================================
echo.

REM Check
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\activate
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate
echo [1/3] Activating virtual environment...
call venv\Scripts\activate

REM Check if 
if not exist ".env" (
    if exist "env.example" (
        echo.
        echo [WARNING] .env file not found!
        echo Please copy env.example to .env and add your API keys
        echo.
        echo Run: copy env.example .env
        echo Then edit .env with your keys
        echo.
        pause
        exit /b 1
    )
)

echo [2/3] Checking dependencies...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [ERROR] Dependencies not installed!
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [3/3] Starting Streamlit application...
echo.
echo Application will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run app_streamlit.py

pause

