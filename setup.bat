@echo off
REM AccessEduChatbot Setup Script for Windows

echo ===================================================
echo         AccessEduChatbot Setup Script
echo ===================================================

REM Check for Python installation
echo Checking for Python installation...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please install Python 3.x and try again.
    exit /b 1
)
echo Python found.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated.

REM Install dependencies
echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt
echo Requirements installed.

REM Check for OpenAI API key
if "%OPENAI_API_KEY%"=="" (
    echo WARNING: OPENAI_API_KEY environment variable not set.
    echo To set your OpenAI API key, run:
    echo set OPENAI_API_KEY=your_api_key_here
) else (
    echo OpenAI API key found in environment variables.
)

echo ===================================================
echo       Setup complete! To run the app:
echo       1. Make sure venv is activated
echo       2. Run: python app.py
echo ===================================================
