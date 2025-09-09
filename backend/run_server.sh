#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists and has API key
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and add your OpenAI API key"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if grep -q "your-openai-api-key-here" .env; then
    echo "⚠️  Warning: Please update your OpenAI API key in the .env file"
    echo "Edit .env and replace 'your-openai-api-key-here' with your actual API key"
fi

echo "🚀 Starting Search Agent API server..."
echo "📚 API Documentation will be available at: http://localhost:8000/docs"
echo "🔍 API endpoints at: http://localhost:8000/api"
echo ""

# Run the server
python -m app.main
