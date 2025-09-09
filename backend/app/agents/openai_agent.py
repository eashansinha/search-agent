"""OpenAI-based search agent implementation with WebSearchTool"""

import os
import json
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass
from agents import Agent, Runner
from agents.tool import WebSearchTool, UserLocation, Filters
import openai
from openai import OpenAI


@dataclass
class SearchConfig:
    """Configuration for web search"""
    user_location: Optional[UserLocation] = None
    filters: Optional[Filters] = None
    search_context_size: Literal["low", "medium", "high"] = "medium"


class OpenAISearchAgent:
    """A search agent using OpenAI's models with WebSearchTool"""
    
    def __init__(self, api_key: Optional[str] = None, search_config: Optional[SearchConfig] = None):
        """
        Initialize the OpenAI search agent with WebSearchTool.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            search_config: Configuration for the web search tool
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Set the API key for the agents SDK
        os.environ["OPENAI_API_KEY"] = self.api_key
        
        # Initialize OpenAI client for direct API access
        self.client = OpenAI(api_key=self.api_key)
        
        # Initialize search configuration
        self.search_config = search_config or SearchConfig()
        
        # Create WebSearchTool with configuration
        self.web_search_tool = WebSearchTool(
            user_location=self.search_config.user_location,
            filters=self.search_config.filters,
            search_context_size=self.search_config.search_context_size
        )
        
        # Create the agent with WebSearchTool
        self.agent = Agent(
            name="WebSearchAssistant",
            instructions="""You are an advanced search assistant powered by web search capabilities.
            You can help users find accurate, up-to-date information from the web.
            
            When searching:
            - Be thorough and provide comprehensive answers
            - Always cite your sources with URLs when available
            - Provide context and explanations for your findings
            - If information is uncertain or conflicting, mention multiple perspectives
            - Focus on recent and authoritative sources when possible
            
            Your goal is to provide helpful, accurate, and well-sourced information.""",
            tools=[self.web_search_tool],
            model="gpt-4o"  # Use GPT-4o for best performance with web search
        )
    
    def update_search_config(
        self, 
        user_location: Optional[UserLocation] = None,
        filters: Optional[Filters] = None,
        search_context_size: Optional[Literal["low", "medium", "high"]] = None
    ):
        """
        Update the web search configuration.
        
        Args:
            user_location: Optional location for customizing search results
            filters: Optional filters based on file attributes
            search_context_size: Amount of context to use ("low", "medium", "high")
        """
        if user_location is not None:
            self.search_config.user_location = user_location
            self.web_search_tool.user_location = user_location
        
        if filters is not None:
            self.search_config.filters = filters
            self.web_search_tool.filters = filters
        
        if search_context_size is not None:
            self.search_config.search_context_size = search_context_size
            self.web_search_tool.search_context_size = search_context_size
    
    async def search(self, query: str, context_size: Optional[Literal["low", "medium", "high"]] = None) -> Dict[str, Any]:
        """
        Perform a web search using the agent with WebSearchTool.
        
        Args:
            query: The search query
            context_size: Optional override for search context size
            
        Returns:
            Dictionary containing the search results and agent response
        """
        try:
            # Temporarily update context size if specified
            original_context_size = self.web_search_tool.search_context_size
            if context_size:
                self.web_search_tool.search_context_size = context_size
            
            # Run the agent with the search query
            result = Runner.run_sync(self.agent, query)
            
            # Restore original context size
            if context_size:
                self.web_search_tool.search_context_size = original_context_size
            
            return {
                "success": True,
                "query": query,
                "response": result.final_output,
                "metadata": {
                    "model": "gpt-4o",
                    "search_context_size": context_size or self.search_config.search_context_size,
                    "tokens_used": getattr(result, 'tokens_used', None),
                    "tool": "WebSearchTool"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def chat(
        self, 
        message: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None,
        enable_search: bool = True
    ) -> Dict[str, Any]:
        """
        Have a conversation with the agent, optionally with web search capabilities.
        
        Args:
            message: The user's message
            conversation_history: Optional conversation history
            enable_search: Whether to enable web search for this conversation
            
        Returns:
            Dictionary containing the agent's response
        """
        try:
            # Create agent with or without search tool based on enable_search
            if enable_search:
                agent = self.agent
            else:
                agent = Agent(
                    name="ChatAssistant",
                    instructions="""You are a helpful assistant. Provide clear, accurate,
                    and helpful responses based on your knowledge.""",
                    model="gpt-4o"
                )
            
            # Build conversation context
            if conversation_history:
                # Format conversation history for the agent
                context = "\n".join([
                    f"{msg.get('role', 'user')}: {msg.get('content', '')}"
                    for msg in conversation_history
                ])
                full_message = f"Conversation history:\n{context}\n\nCurrent message: {message}"
            else:
                full_message = message
            
            # Run the agent
            result = Runner.run_sync(agent, full_message)
            
            return {
                "success": True,
                "message": message,
                "response": result.final_output,
                "conversation_id": None,  # Implement session management as needed
                "metadata": {
                    "model": "gpt-4o",
                    "search_enabled": enable_search,
                    "tokens_used": getattr(result, 'tokens_used', None)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": message,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def multi_query_search(self, queries: List[str]) -> Dict[str, Any]:
        """
        Perform multiple searches and synthesize the results.
        
        Args:
            queries: List of search queries
            
        Returns:
            Dictionary containing synthesized results from all queries
        """
        try:
            results = []
            for query in queries:
                result = await self.search(query)
                if result["success"]:
                    results.append({
                        "query": query,
                        "response": result["response"]
                    })
            
            # Synthesize results
            synthesis_prompt = f"""Based on the following search results for multiple queries,
            provide a comprehensive synthesis that addresses all queries:
            
            {json.dumps(results, indent=2)}
            
            Provide a well-organized response that:
            1. Addresses each query
            2. Identifies common themes and connections
            3. Highlights any contradictions or different perspectives
            4. Provides a cohesive summary"""
            
            synthesis_result = Runner.run_sync(self.agent, synthesis_prompt)
            
            return {
                "success": True,
                "queries": queries,
                "individual_results": results,
                "synthesis": synthesis_result.final_output,
                "metadata": {
                    "model": "gpt-4o",
                    "num_queries": len(queries)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "queries": queries,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def research_topic(self, topic: str, depth: Literal["basic", "detailed", "comprehensive"] = "detailed") -> Dict[str, Any]:
        """
        Conduct in-depth research on a topic using multiple search strategies.
        
        Args:
            topic: The research topic
            depth: Level of research depth
            
        Returns:
            Dictionary containing comprehensive research results
        """
        try:
            # Adjust context size based on depth
            context_map = {
                "basic": "low",
                "detailed": "medium",
                "comprehensive": "high"
            }
            context_size = context_map[depth]
            
            # Generate research queries based on depth
            query_generation_prompt = f"""Generate {3 if depth == 'basic' else 5 if depth == 'detailed' else 7} 
            specific search queries to thoroughly research the topic: "{topic}".
            
            The queries should cover:
            - Overview and definition
            - Current state and recent developments
            - Key applications or implications
            - Expert opinions or authoritative sources
            - Future trends or predictions (if applicable)
            
            Return only the queries, one per line."""
            
            # Generate queries using the agent
            query_result = Runner.run_sync(
                Agent(
                    name="QueryGenerator",
                    instructions="Generate focused search queries for research.",
                    model="gpt-4o"
                ),
                query_generation_prompt
            )
            
            # Parse queries from response
            queries = [q.strip() for q in query_result.final_output.split('\n') if q.strip()]
            
            # Perform searches with appropriate context size
            search_results = []
            for query in queries:
                result = await self.search(query, context_size=context_size)
                if result["success"]:
                    search_results.append({
                        "query": query,
                        "findings": result["response"]
                    })
            
            # Compile comprehensive research report
            report_prompt = f"""Based on the following research findings about "{topic}",
            create a comprehensive research report:
            
            {json.dumps(search_results, indent=2)}
            
            Structure your report with:
            1. Executive Summary
            2. Detailed Findings (organized by theme)
            3. Key Insights and Implications
            4. Sources and References
            5. Conclusion
            
            Make it thorough, well-organized, and properly cited."""
            
            report_result = Runner.run_sync(self.agent, report_prompt)
            
            return {
                "success": True,
                "topic": topic,
                "depth": depth,
                "research_queries": queries,
                "findings": search_results,
                "report": report_result.final_output,
                "metadata": {
                    "model": "gpt-4o",
                    "context_size": context_size,
                    "num_queries": len(queries)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "topic": topic,
                "error": str(e),
                "error_type": type(e).__name__
            }
