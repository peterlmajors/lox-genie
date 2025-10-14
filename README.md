# Welcome to the Lox Genie

<div align="center">
  <img src="static/lox-logo512.png" alt="Lox Logo" width="128" height="128">
</div>

This repository provides access to the Lox Genie, a fantasy football research assistant built with LangGraph and open source language models (gpt-oss:20b, llama3.1:8b, etc.), as well as the Lox MCP Server, to offer fantasy football tools and resources in a unified format.

## 🧠  Thesis

The use case for an agentic fantasy sports consultant is compelling: access to sports data is heavily democratized, player performances and news are constantly updating, and 'expert opinion' is bountiful thanks to social media, but difficult to apply.

Lox is designed for the fantasy sports power-user. By building a context-rich relationship with each user, Lox is able to apply strategic preferences across leagues and seasons — remembering not just who you manage, but how you like to play.

Existing fantasy football sites like [KeepTradeCut](https://keeptradecut.com/) crowdsource valuations through direct player comparisons, while others like [FantasyCalc](https://fantasycalc.com/redraft-rankings) apply optimization algorithms to real trades, generating market-driven rankings.

Behind the scenes, Lox performs a similar function, but with text data. Conversation histories are anonymized and useful insights are added to Lox's knowledge base, ensuring managers benefit from the network's collective intelligence. (*Premium Feature*)

Fantasy football brings people together. However, keeping up with the competition can turn into a time-consuming, isolating task. Let's fix that. Join Lox today.

## 🏈  What is Lox Genie?

Lox Genie is, fundamentally, a deep research agent which processes user queries by:

- **Assessing their relevance** for Lox's intended purpose and tool-calling cababilities
- **Optionally, engaging a human-in-the-loop** to gain additional information to achieve the user's goal
- **Plans research strategies** by breaking down complex questions into actionable subtasks
- **Executes research** using specialized MCP tools and resources for data gathering
- **Provides expert analysis** with concise, well-supported recommendations

The agent is instructed to be maximally truth-seeking, providing resolute and non-ambiguous answers by blending its knowledge base with ground-up analysis.

## 🛠️  Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Docker (for containerized deployment)

## 🚀  Quick Start

Get Lox Genie running locally on your Mac in 3 steps.

### Prerequisites
- Docker & Docker Compose
- ~2GB free disk space
- Mac (Intel or Apple Silicon)

### Step 1: Download Model

Download the GGUF model for llama.cpp (~2GB):

```bash
./scripts/setup-llama-model.sh
```

This downloads Llama 3.2 3B Instruct (Q4 quantized) optimized for Mac CPU.

### Step 2: Start Services

Start all services with llama.cpp for LLM inference:

```bash
docker-compose -f docker-compose-local.yml up
```

**First startup** takes 2-3 minutes to build images.

### Step 3: Test

Once running, test the LLM service:

```bash
# Health check
curl http://localhost:8002/health

# Chat completion
curl -X POST http://localhost:8002/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 50
  }'
```

### 🎉 Services Running

- **API**: http://localhost:8000
- **MCP**: http://localhost:8001
- **UI**: http://localhost
- **LLM**: http://localhost:8002 (Llama 3.2 3B via llama.cpp)
- **Redis**: localhost:6379

## 🔧 Development

### Local LLM (llama.cpp)
- **Model**: Llama 3.2 3B Instruct (Q4_K_M quantized)
- **Size**: ~2GB
- **Performance**: 10-15 tokens/sec on Mac
- **API**: OpenAI-compatible

### Testing
```bash
# Install test dependencies
uv sync

# Test LLM endpoint
python services/llm/test_llm.py

# Test agent integration
PYTHONPATH=. uv run python services/api/agent/test_integration.py
```

### View Logs
```bash
# All services
docker-compose -f docker-compose-local.yml logs -f

# Just LLM
docker-compose -f docker-compose-local.yml logs -f llama
```

### Stop Services
```bash
docker-compose -f docker-compose-local.yml down
```

## ☁️ Production Deployment (AWS with GPU)

```bash
# Set HuggingFace token (required for Llama models)
export HF_TOKEN=your_token_here

# Start with vLLM GPU acceleration
docker-compose -f docker-compose-prod.yml up
```