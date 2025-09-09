# Search Agent

A modern search agent application built with OpenAI's Agents SDK, FastAPI, and Next.js.

## Project Structure

```
search-agent/
├── backend/           # Python FastAPI backend
│   ├── app/
│   │   ├── agents/   # Agent implementations
│   │   ├── api/      # API routes
│   │   ├── config.py # Configuration
│   │   └── main.py   # FastAPI application
│   ├── requirements.txt
│   └── .env.example
├── frontend/          # Next.js TypeScript frontend (coming soon)
└── README.md
```

## Features

- 🤖 **AI-Powered Search**: Leverages OpenAI's Agents SDK for intelligent search capabilities
- 🚀 **FastAPI Backend**: High-performance async API with automatic documentation
- 🔍 **Search Tools**: Web search and content summarization capabilities
- 💬 **Chat Interface**: Conversational interaction with the search agent
- 🎨 **Modern Frontend**: Next.js with TypeScript (planned)

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- Node.js 18+ (for frontend, when implemented)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the server:**
   ```bash
   # Development mode
   python -m app.main
   
   # Or using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - API Endpoint: http://localhost:8000/api

## API Endpoints

### Search
```bash
POST /api/search
{
  "query": "What is machine learning?",
  "num_results": 5
}
```

### Chat
```bash
POST /api/chat
{
  "message": "Tell me about quantum computing",
  "conversation_history": []
}
```

### Health Check
```bash
GET /api/health
```

### Agent Info
```bash
GET /api/agent/info
```

## Development Roadmap

### Phase 1: Backend (Current)
- [x] FastAPI application setup
- [x] OpenAI Agents SDK integration
- [x] Basic search agent implementation
- [x] API endpoints for search and chat
- [ ] Real search API integration (Google, Bing, or Tavily)
- [ ] Session management for conversations
- [ ] Enhanced error handling and logging

### Phase 2: Frontend (Next)
- [ ] Next.js project setup with TypeScript
- [ ] Modern UI with Tailwind CSS
- [ ] Search interface component
- [ ] Chat interface component
- [ ] Real-time streaming responses
- [ ] Conversation history management

### Phase 3: Advanced Features
- [ ] Multi-agent coordination
- [ ] Custom tool integration
- [ ] Advanced search filters
- [ ] Result caching
- [ ] User authentication
- [ ] Rate limiting
- [ ] Analytics and monitoring

## Technology Stack

### Backend
- **Framework**: FastAPI
- **AI/ML**: OpenAI Agents SDK, OpenAI API
- **Language**: Python 3.8+
- **Server**: Uvicorn (ASGI)

### Frontend (Planned)
- **Framework**: Next.js 14+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context/Zustand
- **API Client**: Axios/Fetch

## Configuration

Key configuration options in `.env`:

```env
OPENAI_API_KEY=your-api-key
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Production Deployment

### Backend
```bash
# Using Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker (create Dockerfile)
docker build -t search-agent-backend .
docker run -p 8000:8000 search-agent-backend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
