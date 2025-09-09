# Testing Guide for OpenAI WebSearchTool Integration

## 🚀 Quick Start Testing

### Method 1: Using the API Server (Recommended)

1. **Start the API server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Run the test script:**
   ```bash
   # In a new terminal
   cd backend
   ./test_api.sh
   ```

### Method 2: Direct Python Testing

1. **Install minimal dependencies:**
   ```bash
   pip install openai>=1.104.1 openai-agents>=0.2.11 python-dotenv
   ```

2. **Run the standalone test:**
   ```bash
   cd backend
   python standalone_test.py
   ```

### Method 3: Manual API Testing with curl

Test individual endpoints:

```bash
# Health check
curl http://localhost:8000/api/health

# Agent info
curl http://localhost:8000/api/agent/info

# Basic search
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest AI developments?",
    "context_size": "medium"
  }'

# Multi-query search
curl -X POST http://localhost:8000/api/search/multi-query \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "What is machine learning?",
      "What are neural networks?"
    ]
  }'

# Research endpoint
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Renewable energy trends",
    "depth": "detailed"
  }'
```

## 📋 Test Checklist

### Basic Functionality
- [ ] Server starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Agent info shows `openai-websearch` provider
- [ ] Basic search returns relevant results
- [ ] Search results include source citations

### WebSearchTool Features
- [ ] Different context sizes (low/medium/high) work
- [ ] Multi-query search synthesizes results
- [ ] Research endpoint generates comprehensive reports
- [ ] Chat with search enabled provides current information

### Error Handling
- [ ] Invalid queries return appropriate errors
- [ ] Missing API key shows clear error message
- [ ] Malformed requests return 400 errors

## 🔍 What to Look For

### Successful Search Response
```json
{
  "success": true,
  "query": "What are the latest AI developments?",
  "response": "Based on recent web searches, here are the latest developments...",
  "metadata": {
    "model": "gpt-4o",
    "search_context_size": "medium",
    "tool": "WebSearchTool"
  }
}
```

### Key Indicators of WebSearchTool Working
1. **Real-time information**: Responses should include current data (today's weather, recent news, etc.)
2. **Source citations**: URLs and references should be included in responses
3. **Context awareness**: Higher context sizes should provide more detailed responses
4. **Synthesis capability**: Multi-query searches should combine insights from multiple searches

## 🐛 Troubleshooting

### Common Issues

1. **Import Error: cannot import name 'Agent'**
   - Solution: Install `openai-agents>=0.2.11`
   ```bash
   pip install openai-agents>=0.2.11
   ```

2. **API Key Error**
   - Ensure `.env` file has valid `OPENAI_API_KEY`
   - Check that `AI_PROVIDER=openai-websearch`

3. **Dependency Conflicts**
   - Use a virtual environment
   - Install minimal dependencies first:
   ```bash
   pip install openai>=1.104.1 openai-agents>=0.2.11
   ```

4. **Connection Refused**
   - Ensure the server is running on port 8000
   - Check firewall settings

## 📊 Performance Expectations

- **Basic search**: 3-10 seconds
- **Multi-query search**: 10-30 seconds
- **Research (basic)**: 15-45 seconds
- **Research (comprehensive)**: 30-90 seconds

## 🎯 Testing Different Features

### Context Size Testing
```python
# Test different context sizes
for size in ["low", "medium", "high"]:
    response = await agent.search(
        "Explain quantum computing",
        context_size=size
    )
    print(f"{size}: {len(response['response'])} characters")
```

### Multi-Query Testing
```python
# Test synthesis of multiple related queries
queries = [
    "What is artificial intelligence?",
    "How does machine learning work?",
    "What are neural networks?"
]
result = await agent.multi_query_search(queries)
```

### Research Depth Testing
```python
# Test different research depths
for depth in ["basic", "detailed", "comprehensive"]:
    result = await agent.research_topic(
        "Climate change solutions",
        depth=depth
    )
```

## ✅ Success Criteria

Your OpenAI WebSearchTool integration is working correctly if:

1. ✅ Server starts with `AI_PROVIDER=openai-websearch`
2. ✅ Search queries return real-time web information
3. ✅ Responses include source URLs and citations
4. ✅ Different context sizes affect response detail
5. ✅ Multi-query search provides synthesized insights
6. ✅ Research endpoint generates comprehensive reports
7. ✅ Chat with search provides current information

## 📝 Example Test Session

```bash
# Terminal 1: Start server
cd backend
uvicorn app.main:app --reload

# Terminal 2: Run tests
cd backend
./test_api.sh

# Expected output:
# ✅ Health check passed
# ✅ Agent info retrieved (provider: openai-websearch)
# ✅ Search successful (with current information)
# ✅ Multi-query search successful
# ✅ Research successful
```

## 🔗 Additional Resources

- [OpenAI Agents Documentation](https://openai.github.io/openai-agents-python/)
- [WebSearchTool Reference](https://openai.github.io/openai-agents-python/ref/tool/)
- [API Documentation](./WEBSEARCH_INTEGRATION.md)
