#!/bin/bash
# rhea.framework AI Assistant - Setup Script
# For macOS and Linux

echo ""
echo "=============================================="
echo "  rhea.framework AI Assistant - Setup"
echo "=============================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo ""
    echo "Please install Python 3.9 or later:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu: sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python $PYTHON_VERSION found"

# Check for Ollama
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "⚠️  Ollama is not installed (required for AI functionality)"
    echo ""
    echo "Would you like to install Ollama now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo ""
        echo "Please install Ollama manually from: https://ollama.ai"
        echo "After installation, run: ollama pull llama3.2"
        echo ""
    fi
else
    echo "✅ Ollama found"
fi

# Create virtual environment
echo ""
echo "📦 Setting up Python environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

echo ""
echo "=============================================="
echo "  Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Make sure Ollama is running:"
echo "   ollama serve"
echo ""
echo "2. Pull the AI model (if not already done):"
echo "   ollama pull llama3.2"
echo ""
echo "3. Start the AI Assistant:"
echo "   ./start.sh"
echo "   OR"
echo "   source venv/bin/activate && python rhea_ai_assistant.py"
echo ""
echo "The assistant will open in your web browser automatically."
echo ""
