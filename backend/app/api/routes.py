"""API routes for the OpenAI WebSearchTool agent"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from ..agents import OpenAISearchAgent, SearchConfig
from ..config import settings

router = APIRouter()

# Initialize the OpenAI WebSearchTool agent
if not settings.openai_api_key:
    raise ValueError("OpenAI API key is required")

search_agent = OpenAISearchAgent(api_key=settings.openai_api_key)
agent_provider = "openai-websearch"
agent_model = "gpt-4o"


class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(..., description="The search query")
    num_results: int = Field(default=5, ge=1, le=20, description="Number of results to return")
    context_size: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Search context size (for WebSearchTool)"
    )


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="The user's message")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Optional conversation history"
    )
    enable_search: bool = Field(
        default=True,
        description="Enable web search for this conversation"
    )


class MultiQueryRequest(BaseModel):
    """Multi-query search request model"""
    queries: List[str] = Field(..., description="List of search queries")


class ResearchRequest(BaseModel):
    """Research request model"""
    topic: str = Field(..., description="The research topic")
    depth: Literal["basic", "detailed", "comprehensive"] = Field(
        default="detailed",
        description="Level of research depth"
    )


class SearchResponse(BaseModel):
    """Search response model"""
    success: bool
    query: str
    response: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool
    message: str
    response: Optional[str] = None
    conversation_id: Optional[str] = None
    error: Optional[str] = None


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Search Agent API",
        "version": "0.1.0",
        "endpoints": {
            "search": "/api/search",
            "chat": "/api/chat",
            "health": "/api/health"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "search-agent"}


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Perform a search using the agent.
    
    Args:
        request: Search request containing the query
        
    Returns:
        Search results from the agent
    """
    try:
        # Use context_size for OpenAI WebSearch agent
        if agent_provider == "openai-websearch" and hasattr(search_agent, 'search'):
            result = await search_agent.search(request.query, context_size=request.context_size)
        else:
            result = await search_agent.search(request.query)
        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the agent.
    
    Args:
        request: Chat request containing the message and optional history
        
    Returns:
        Agent's response
    """
    try:
        # Use enable_search for OpenAI WebSearch agent
        if agent_provider == "openai-websearch" and hasattr(search_agent, 'chat'):
            result = await search_agent.chat(
                request.message,
                request.conversation_history,
                enable_search=request.enable_search
            )
        else:
            result = await search_agent.chat(
                request.message,
                request.conversation_history
            )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/structured", response_model=SearchResponse)
async def structured_search(request: SearchRequest):
    """
    Perform a structured search using OpenAI's Responses API.
    Returns results in a structured JSON format.
    
    Args:
        request: Search request containing the query
        
    Returns:
        Structured search results from the agent
    """
    try:
        # Only available for OpenAI agent
        if agent_provider == "openai":
            result = await search_agent.structured_search(request.query)
            return SearchResponse(**result)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Structured search is only available with OpenAI provider"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/multi-query")
async def multi_query_search(request: MultiQueryRequest):
    """
    Perform multiple searches and synthesize the results.
    Only available with OpenAI WebSearch agent.
    
    Args:
        request: Multi-query request containing multiple search queries
        
    Returns:
        Synthesized results from all queries
    """
    try:
        if agent_provider == "openai-websearch" and hasattr(search_agent, 'multi_query_search'):
            result = await search_agent.multi_query_search(request.queries)
            return result
        else:
            raise HTTPException(
                status_code=400,
                detail="Multi-query search is only available with OpenAI WebSearch provider"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/research")
async def research_topic(request: ResearchRequest):
    """
    Conduct in-depth research on a topic.
    Only available with OpenAI WebSearch agent.
    
    Args:
        request: Research request containing the topic and depth
        
    Returns:
        Comprehensive research results
    """
    try:
        if agent_provider == "openai-websearch" and hasattr(search_agent, 'research_topic'):
            result = await search_agent.research_topic(request.topic, request.depth)
            return result
        else:
            raise HTTPException(
                status_code=400,
                detail="Research feature is only available with OpenAI WebSearch provider"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/info")
async def agent_info():
    """Get information about the search agent"""
    capabilities = [
        "Web search",
        "Content summarization",
        "Question answering",
        "Conversational interaction"
    ]
    
    endpoints = {
        "search": "/api/search",
        "chat": "/api/chat"
    }
    
    tools = ["web_search", "summarize_content"]
    
    # Add provider-specific capabilities
    if agent_provider == "openai":
        capabilities.append("Structured search")
        endpoints["structured_search"] = "/api/search/structured"
    elif agent_provider == "openai-websearch":
        capabilities.extend([
            "Real-time web search (WebSearchTool)",
            "Multi-query synthesis",
            "In-depth research",
            "Configurable search context"
        ])
        endpoints["multi_query_search"] = "/api/search/multi-query"
        endpoints["research"] = "/api/research"
        tools = ["WebSearchTool"]
    
    return {
        "name": "SearchAssistant",
        "provider": agent_provider,
        "model": agent_model,
        "capabilities": [c for c in capabilities if c],
        "tools": tools,
        "endpoints": {k: v for k, v in endpoints.items() if v}
    }
