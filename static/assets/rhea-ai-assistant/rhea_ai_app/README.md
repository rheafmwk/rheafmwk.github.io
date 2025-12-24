# rhea.framework AI Assistant

A local AI-powered assistant for team leadership knowledge, built on the rhea.framework knowledge base.

![Screenshot](screenshot.png)

## Features

- 🤖 **Private & Local**: All AI processing happens on your device - no data sent to external servers
- 📚 **Knowledge-Based**: Answers grounded in the rhea.framework knowledge base
- 🔍 **Source Citations**: See which patterns and practices inform each response
- 🌐 **Web Interface**: Easy-to-use browser interface - no command line needed after setup
- ⚡ **Fast**: Uses efficient local AI models through Ollama

## Quick Start

### Prerequisites

1. **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
2. **Ollama** - [Download Ollama](https://ollama.ai)

### Installation

#### macOS / Linux

```bash
# 1. Extract this folder and open Terminal in it

# 2. Run the setup script
chmod +x setup.sh start.sh
./setup.sh

# 3. Make sure Ollama is running (in another terminal)
ollama serve

# 4. Pull the AI model (first time only)
ollama pull llama3.2

# 5. Start the assistant
./start.sh
```

#### Windows

1. Extract this folder
2. Double-click `setup.bat` and follow the instructions
3. Make sure Ollama is running (from Start Menu or run `ollama serve`)
4. Pull the AI model: `ollama pull llama3.2`
5. Double-click `start.bat`

### Usage

Once started, the AI Assistant opens automatically in your web browser at `http://localhost:5050`.

Simply type your question about team leadership and press Enter!

**Example Questions:**
- "How do I handle conflicts between team members?"
- "What patterns help with building trust in a new team?"
- "How should I delegate complex tasks effectively?"
- "What are best practices for remote team communication?"

## Configuration

You can customize the assistant using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `llama3.2` | The AI model to use |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `PORT` | `5050` | Web server port |
| `CHROMA_DB_PATH` | `./chroma_db` | Path to knowledge base |

### Using a Different Model

```bash
# Try a larger, more capable model
OLLAMA_MODEL=llama3.1:8b ./start.sh

# Or a smaller, faster model
OLLAMA_MODEL=llama3.2:1b ./start.sh
```

## Troubleshooting

### "Ollama not running"
- Make sure Ollama is installed and the service is running
- On macOS/Linux: Run `ollama serve` in a separate terminal
- On Windows: Open Ollama from Start Menu

### "Model not found"
```bash
# Download the required model
ollama pull llama3.2
```

### "Python not found"
- Install Python 3.9 or later
- On Windows, make sure "Add Python to PATH" was checked during installation

### Slow responses
- The first query may be slow as the model loads
- Try a smaller model: `OLLAMA_MODEL=llama3.2:1b`
- Ensure you have enough RAM (8GB+ recommended)

## About rhea.framework

The rhea.framework is an educational resource for experiential learning in team leadership for ICT projects, developed at the University of Vienna.

Learn more at [rheafmwk.io](https://rheafmwk.io)

## License

This work is licensed under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).
