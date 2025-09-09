#!/bin/bash

# Test script for OpenAI WebSearchTool API endpoints
# Make sure the server is running: uvicorn app.main:app --reload

BASE_URL="http://localhost:8000"

echo "=================================================="
echo "🧪 Testing OpenAI WebSearchTool API Endpoints"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "\n1️⃣ Testing Health Endpoint..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    echo "Response: $body"
else
    echo -e "${RED}❌ Health check failed (HTTP $http_code)${NC}"
fi

# Test 2: Agent Info
echo -e "\n2️⃣ Testing Agent Info Endpoint..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/agent/info")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Agent info retrieved${NC}"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo -e "${RED}❌ Agent info failed (HTTP $http_code)${NC}"
fi

# Test 3: Basic Search
echo -e "\n3️⃣ Testing Search Endpoint..."
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/search" \
    -H "Content-Type: application/json" \
    -d '{
        "query": "What are the latest developments in AI?",
        "context_size": "medium"
    }')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Search successful${NC}"
    echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print('Response preview:', data.get('response', '')[:300] + '...')" 2>/dev/null || echo "$body"
else
    echo -e "${RED}❌ Search failed (HTTP $http_code)${NC}"
    echo "$body"
fi

# Test 4: Chat with Search
echo -e "\n4️⃣ Testing Chat Endpoint..."
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{
        "message": "What is the weather in San Francisco today?",
        "enable_search": true
    }')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Chat successful${NC}"
    echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print('Response preview:', data.get('response', '')[:300] + '...')" 2>/dev/null || echo "$body"
else
    echo -e "${RED}❌ Chat failed (HTTP $http_code)${NC}"
    echo "$body"
fi

# Test 5: Multi-Query Search (WebSearchTool specific)
echo -e "\n5️⃣ Testing Multi-Query Search Endpoint..."
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/search/multi-query" \
    -H "Content-Type: application/json" \
    -d '{
        "queries": [
            "What is machine learning?",
            "What are neural networks?"
        ]
    }')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Multi-query search successful${NC}"
    echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print('Synthesis preview:', data.get('synthesis', '')[:300] + '...')" 2>/dev/null || echo "$body"
else
    echo -e "${RED}❌ Multi-query search failed (HTTP $http_code)${NC}"
    echo "$body"
fi

# Test 6: Research Endpoint (WebSearchTool specific)
echo -e "\n6️⃣ Testing Research Endpoint..."
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/research" \
    -H "Content-Type: application/json" \
    -d '{
        "topic": "Quantum computing basics",
        "depth": "basic"
    }')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Research successful${NC}"
    echo "$body" | python3 -c "import sys, json; data=json.load(sys.stdin); print('Report preview:', data.get('report', '')[:300] + '...')" 2>/dev/null || echo "$body"
else
    echo -e "${RED}❌ Research failed (HTTP $http_code)${NC}"
    echo "$body"
fi

echo -e "\n=================================================="
echo "✅ Testing complete!"
echo "=================================================="
