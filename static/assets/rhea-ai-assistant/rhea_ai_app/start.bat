@echo off
REM rhea.framework AI Assistant - Start Script for Windows

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo X Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Check if Ollama is responding
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Ollama doesn't seem to be running.
    echo.
    echo Please start Ollama:
    echo   - Open Ollama from Start Menu, or
    echo   - Run: ollama serve
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo.
echo Starting rhea.framework AI Assistant...
echo.

call venv\Scripts\activate.bat
python rhea_ai_assistant.py
