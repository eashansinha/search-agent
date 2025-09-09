#!/usr/bin/env python3
"""Simple FastAPI app with OpenAI WebSearchTool - minimal dependencies"""

import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="OpenAI WebSearch Agent API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query")
    context_size: Optional[Literal["low", "medium", "high"]] = Field(
        default="medium",
        description="Search context size"
    )

class SearchResponse(BaseModel):
    success: bool
    query: str
    response: Optional[str] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None


# Initialize agent on startup
agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize the OpenAI agent with WebSearchTool"""
    global agent
    
    try:
        from agents import Agent
        from agents.tool import WebSearchTool
        
        # Create WebSearchTool
        web_search = WebSearchTool(search_context_size="medium")
        
        # Create agent
        agent = Agent(
            name="WebSearchAssistant",
            instructions="""You are a helpful search assistant with real-time web search capabilities.
            Provide accurate, well-sourced information and always cite your sources.""",
            tools=[web_search],
            model="gpt-4o"
        )
        
        print("✅ OpenAI WebSearchTool agent initialized successfully!")
        
    except ImportError as e:
        print(f"❌ Failed to import openai-agents: {e}")
        print("Install with: pip install openai-agents>=0.2.11 openai>=1.104.1")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OpenAI WebSearch Agent API",
        "version": "1.0.0",
        "status": "running" if agent else "agent not initialized",
        "endpoints": {
            "health": "/health",
            "search": "/search",
            "agent_info": "/agent/info"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_ready": agent is not None
    }


@app.get("/agent/info")
async def agent_info():
    """Get agent information"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return {
        "name": "WebSearchAssistant",
        "provider": "openai-websearch",
        "model": "gpt-4o",
        "tools": ["WebSearchTool"],
        "capabilities": [
            "Real-time web search",
            "Source citation",
            "Configurable context size"
        ]
    }


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Perform a web search"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized. Install openai-agents package.")
    
    try:
        from agents import Runner
        import concurrent.futures
        
        # Update context size if needed
        if request.context_size and request.context_size != "medium":
            from agents.tool import WebSearchTool
            web_search = WebSearchTool(search_context_size=request.context_size)
            agent.tools = [web_search]
        
        # Run the search - use asyncio to run in executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: Runner.run_sync(agent, request.query)
        )
        
        return SearchResponse(
            success=True,
            query=request.query,
            response=result.final_output,
            metadata={
                "model": "gpt-4o",
                "context_size": request.context_size,
                "tool": "WebSearchTool"
            }
        )
        
    except Exception as e:
        return SearchResponse(
            success=False,
            query=request.query,
            error=str(e)
        )


@app.post("/chat")
async def chat(message: str):
    """Simple chat endpoint"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        from agents import Runner
        import concurrent.futures
        
        # Run in executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: Runner.run_sync(agent, message)
        )
        
        return {
            "success": True,
            "message": message,
            "response": result.final_output
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": message,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
