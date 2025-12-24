@echo off
REM rhea.framework AI Assistant - Setup Script for Windows

echo.
echo ==============================================
echo   rhea.framework AI Assistant - Setup
echo ==============================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed.
    echo.
    echo Please download and install Python 3.9+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found

REM Check for Ollama
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Ollama is not installed (required for AI functionality)
    echo.
    echo Please download and install Ollama from:
    echo   https://ollama.ai
    echo.
    echo After installation, run: ollama pull llama3.2
    echo.
) else (
    echo [OK] Ollama found
)

REM Create virtual environment
echo.
echo [*] Setting up Python environment...
python -m venv venv

REM Activate and install
echo [*] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

echo.
echo ==============================================
echo   Setup Complete!
echo ==============================================
echo.
echo Next steps:
echo.
echo 1. Make sure Ollama is running:
echo    - Open Ollama from Start Menu, or
echo    - Run: ollama serve
echo.
echo 2. Pull the AI model (if not already done):
echo    ollama pull llama3.2
echo.
echo 3. Start the AI Assistant:
echo    Double-click start.bat
echo.
echo The assistant will open in your web browser automatically.
echo.
pause
