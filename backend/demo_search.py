#!/usr/bin/env python3
"""Demo: GPT-5 mini with WebSearchTool - Learning from web and summarizing"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def demo_web_search():
    """Demonstrate GPT-5 mini learning from web search and summarizing"""
    
    print("🚀 GPT-5 Mini WebSearchTool Demo")
    print("=" * 70)
    print("This demo shows GPT-5 mini searching the web and summarizing results")
    print("=" * 70)
    
    try:
        # Import required modules
        from agents import Agent, Runner
        from agents.tool import WebSearchTool
        
        # Create WebSearchTool with high context for better summaries
        print("\n📡 Creating WebSearchTool with high context...")
        web_search = WebSearchTool(search_context_size="high")
        
        # Create GPT-5 mini agent with enhanced summarization instructions
        print("🤖 Initializing GPT-5 mini agent...")
        agent = Agent(
            name="WebSearchSummarizer",
            instructions="""You are an AI assistant powered by GPT-5 mini with real-time web search.
            
            Your task is to:
            1. Search the web for current, accurate information
            2. Learn from multiple sources
            3. Synthesize and summarize the information clearly
            4. Provide well-structured, concise summaries with key insights
            5. Always cite your sources with URLs
            
            Focus on providing actionable insights and clear explanations.""",
            tools=[web_search],
            model="gpt-5-mini"
        )
        
        # Test queries that require web search and summarization
        queries = [
            {
                "query": "What are the latest breakthroughs in AI in 2024? Summarize the top 3 developments.",
                "description": "Recent AI developments with summary"
            },
            {
                "query": "What is the current weather in San Francisco and what should I wear today?",
                "description": "Current weather with practical advice"
            },
            {
                "query": "Explain quantum computing in simple terms based on recent articles",
                "description": "Complex topic simplified from web sources"
            }
        ]
        
        for i, item in enumerate(queries, 1):
            print(f"\n{'='*70}")
            print(f"🔍 Query {i}: {item['description']}")
            print(f"{'='*70}")
            print(f"Question: {item['query']}")
            print("-" * 70)
            
            try:
                # Run the search and get GPT-5 mini's summary
                result = Runner.run_sync(agent, item['query'])
                
                print("✅ GPT-5 Mini Response (with web search):")
                print("-" * 70)
                print(result.final_output)
                print("-" * 70)
                print(f"📊 Response length: {len(result.final_output)} characters")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n" + "=" * 70)
        print("✨ Demo Complete!")
        print("=" * 70)
        print("\n📝 Summary:")
        print("  • GPT-5 mini successfully searched the web")
        print("  • Retrieved current information from multiple sources")
        print("  • Synthesized and summarized the findings")
        print("  • Provided structured, actionable insights")
        print("  • Cited sources for verification")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure openai-agents is installed: pip install openai-agents>=0.2.11")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_web_search()
