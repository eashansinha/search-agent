# OpenAI WebSearchTool Agent

A powerful search agent built with OpenAI's WebSearchTool for real-time web search capabilities.

## Features

- 🔍 **Real-time Web Search**: Access current information from the internet
- 📚 **Source Citation**: Automatic citation of sources and URLs
- 🎯 **Configurable Context**: Adjust search depth (low/medium/high)
- 🔄 **Multi-Query Synthesis**: Combine insights from multiple searches
- 📊 **Research Mode**: In-depth research with automatic query generation
- 💬 **Conversational Interface**: Chat with optional web search

## Quick Start

### 1. Installation

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run the Application

**Option A: FastAPI Server**
```bash
python websearch_app.py
# Server runs on http://localhost:8000
```

**Option B: Direct Testing**
```bash
python test_websearch_agent.py
```

## API Endpoints

### Search
```bash
POST /search
{
  "query": "What are the latest AI developments?",
  "context_size": "medium"  # low, medium, or high
}
```

### Multi-Query Search
```bash
POST /search/multi-query
{
  "queries": ["What is AI?", "What is ML?"]
}
```

### Research
```bash
POST /research
{
  "topic": "Quantum computing",
  "depth": "detailed"  # basic, detailed, or comprehensive
}
```

### Chat
```bash
POST /chat
{
  "message": "What's the weather today?",
  "enable_search": true
}
```

## Project Structure

```
search-agent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── openai_agent.py      # OpenAI WebSearchTool implementation
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py            # API endpoints
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration
│   │   └── main.py                  # FastAPI app
│   ├── .env                         # Environment variables
│   ├── .env.example                 # Example environment file
│   ├── requirements.txt             # Python dependencies
│   ├── websearch_app.py            # Standalone FastAPI app
│   ├── test_websearch_agent.py     # Test script
│   └── test_api.sh                 # API testing script
├── WEBSEARCH_INTEGRATION.md        # Detailed integration docs
├── TESTING_GUIDE.md                # Testing documentation
└── README.md                        # This file
```

## Requirements

- Python 3.8+
- OpenAI API key with access to GPT-4o
- `openai-agents>=0.2.11`
- `openai>=1.104.1`

## Testing

Run the comprehensive test:
```bash
python test_websearch_agent.py
```

Or test the API endpoints:
```bash
./test_api.sh
```

## Documentation

- [WebSearchTool Integration Guide](WEBSEARCH_INTEGRATION.md)
- [Testing Guide](TESTING_GUIDE.md)

## License

MIT
