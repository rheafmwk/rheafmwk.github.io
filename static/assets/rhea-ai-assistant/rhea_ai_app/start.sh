#!/bin/bash
# rhea.framework AI Assistant - Start Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama doesn't seem to be running."
    echo ""
    echo "Please start Ollama in another terminal:"
    echo "   ollama serve"
    echo ""
    echo "Or if it's already running on a different port, that's fine."
    echo ""
fi

echo ""
echo "🚀 Starting rhea.framework AI Assistant..."
echo ""

# Check if virtual environment exists, if so use it
if [ -d "venv" ]; then
    source venv/bin/activate
    # Ensure packages are installed in venv
    pip install -q flask langchain langchain-community chromadb gpt4all 2>/dev/null
fi

python3 rhea_ai_assistant.py
