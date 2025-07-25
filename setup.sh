#!/bin/bash

# AccessEduChatbot Setup Script
echo "╔═════════════════════════════════════════════╗"
echo "║       AccessEduChatbot Setup Script         ║"
echo "╚═════════════════════════════════════════════╝"

# Check for Python installation
echo "Checking for Python installation..."
if command -v python3 &>/dev/null; then
    echo "Python 3 found."
    python_cmd="python3"
elif command -v python &>/dev/null; then
    echo "Python found."
    python_cmd="python"
else
    echo "Error: Python not found. Please install Python 3.x and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
$python_cmd -m venv venv
echo "Virtual environment created."

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi
echo "Virtual environment activated."

# Install dependencies
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Requirements installed."

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "WARNING: OPENAI_API_KEY environment variable not set."
    echo "To set your OpenAI API key, run:"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        echo "set OPENAI_API_KEY=your_api_key_here"
    else
        # Linux/Mac
        echo "export OPENAI_API_KEY=your_api_key_here"
    fi
else
    echo "OpenAI API key found in environment variables."
fi

echo "╔═════════════════════════════════════════════╗"
echo "║      Setup complete! To run the app:        ║"
echo "║      1. Make sure venv is activated         ║"
echo "║      2. Run: python app.py                  ║"
echo "╚═════════════════════════════════════════════╝"
