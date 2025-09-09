# OpenAI WebSearchTool Integration

This document describes the integration of OpenAI's WebSearchTool into the search agent application.

## Overview

The OpenAI WebSearchTool is a hosted tool that enables LLMs to search the web in real-time. It's currently only supported with OpenAI models using the Responses API.

## Features

### 1. **Real-Time Web Search**
- Direct integration with OpenAI's web search capabilities
- No need for external search API subscriptions
- Automatic source citation and relevance ranking

### 2. **Configurable Search Context**
The WebSearchTool supports three levels of search context:
- **Low**: Quick searches with minimal context
- **Medium**: Balanced search with moderate context (default)
- **High**: Comprehensive searches with maximum context

### 3. **Location-Based Search**
- Optional user location parameter for geographically relevant results
- Customizes search results based on location preferences

### 4. **Advanced Search Filters**
- Filter results based on file attributes
- Customize search behavior for specific use cases

## Implementation

### OpenAI Agent with WebSearchTool

```python
from app.agents import OpenAISearchAgent, SearchConfig

# Initialize agent with default configuration
agent = OpenAISearchAgent()

# Or with custom configuration
config = SearchConfig(
    search_context_size="high",
    user_location=UserLocation(...)  # Optional
)
agent = OpenAISearchAgent(search_config=config)
```

### Basic Search

```python
# Perform a search
result = await agent.search("What are the latest AI developments?")

# With custom context size
result = await agent.search(
    "Explain quantum computing",
    context_size="high"
)
```

### Multi-Query Search

```python
# Search multiple queries and synthesize results
queries = [
    "What is machine learning?",
    "What are neural networks?",
    "How do transformers work?"
]
result = await agent.multi_query_search(queries)
```

### In-Depth Research

```python
# Conduct comprehensive research on a topic
result = await agent.research_topic(
    topic="Renewable energy trends",
    depth="comprehensive"  # Options: basic, detailed, comprehensive
)
```

## API Endpoints

### Search Endpoint
```http
POST /api/search
Content-Type: application/json

{
  "query": "What are the latest developments in AI?",
  "context_size": "medium"  // Optional: low, medium, high
}
```

### Multi-Query Search
```http
POST /api/search/multi-query
Content-Type: application/json

{
  "queries": [
    "What is machine learning?",
    "What are neural networks?"
  ]
}
```

### Research Endpoint
```http
POST /api/research
Content-Type: application/json

{
  "topic": "Climate change solutions",
  "depth": "detailed"  // Options: basic, detailed, comprehensive
}
```

### Chat with Web Search
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What's the weather in San Francisco?",
  "enable_search": true,
  "conversation_history": []  // Optional
}
```

## Configuration

### Environment Variables

Set the AI provider in your `.env` file:

```bash
# Use OpenAI with WebSearchTool
AI_PROVIDER=openai-websearch
OPENAI_API_KEY=your-openai-api-key-here
```

### Provider Options

- `openai`: Standard OpenAI agent with custom tools
- `openai-websearch`: OpenAI agent with WebSearchTool (real-time web search)
- `anthropic`: Anthropic Claude agent

## Benefits

1. **No External API Required**: WebSearchTool is hosted by OpenAI, eliminating the need for separate search API subscriptions

2. **Optimized for AI**: Search results are formatted and optimized for LLM consumption

3. **Automatic Citations**: Sources are automatically cited with URLs

4. **Scalable**: Handles multiple queries and complex research tasks

5. **Context-Aware**: Adjustable context size for different use cases

## Testing

Run the test script to verify the integration:

```bash
cd backend
python test_websearch.py
```

The test script covers:
- Basic web search functionality
- Different context size configurations
- Multi-query search and synthesis
- In-depth research capabilities
- Conversational search with history

## Requirements

- OpenAI API key with access to GPT-4o or later models
- `openai-agents>=0.2.0` package
- `openai>=1.50.0` package

## Best Practices

1. **Choose Appropriate Context Size**:
   - Use "low" for quick factual queries
   - Use "medium" for general searches (default)
   - Use "high" for complex research requiring comprehensive context

2. **Batch Related Queries**: Use multi-query search for related questions to get synthesized insights

3. **Leverage Research Mode**: For in-depth topics, use the research endpoint which automatically generates and executes multiple targeted queries

4. **Enable Search Selectively**: In chat mode, enable/disable search based on whether the query requires real-time information

## Limitations

- Currently only supported with OpenAI models
- Requires internet connectivity for real-time search
- Search results depend on OpenAI's web search capabilities
- May have rate limits based on your OpenAI API tier

## Future Enhancements

- Support for custom search filters
- Integration with specific domain searches
- Caching of frequent queries
- Advanced result ranking and filtering
- Support for image and video search results
