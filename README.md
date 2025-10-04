# Welcome to the Lox API

<div align="center">
  <img src="static/lox-logo512.png" alt="Lox Logo" width="128" height="128">
</div>

This repository provides access to the Lox Genie, a fantasy football research assistant built with LangGraph and open source language models (gpt-oss:20b, llama3.1:8b, etc.), as well as the Lox MCP Server, to offer fantasy football tools and resources in a unified format.

## 🧠  Thesis

The use case for an agentic fantasy sports consultant is compelling: access to sports data is already democratized, player performances and news are burdensome to keep up with, and 'expert opinion' is bountiful thanks to social media, but difficult to apply. 

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

The agent is designed to be maximally truth-seeking, providing resolute and non-ambiguous answers by blending its knowledge base with ground-up analysis.

## 🏗️  Architecture

- **FastAPI Service** (Port 8000): RESTful API with streaming chat capabilities
- **MCP Server** (Port 8001): Model Context Protocol server for tool integration
- **LangGraph Agent**: Multi-node workflow orchestration for intelligent research
- **Docker Support**: Containerized deployment with docker-compose

## 🛠️  Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Docker (for containerized deployment)

## 🚀  Quick Start

### Using Docker (Recommended)

```bash
# Start both services
docker-compose up --build

# Access services
# FastAPI: http://localhost:8000
# MCP Server: http://localhost:8001
```

### Local Development

#### Using uv (Windows)

```bash
# Install uv if you haven't already
pip install uv

# Install dependencies
uv sync

# Run the FastAPI service
uv run services/genie/main.py

# In another terminal, run the MCP server
uv run services/mcp/main.py
```

#### Using pip/venv

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements/requirements-api.txt
pip install -r requirements/requirements-mcp.txt

# Run services
python services/genie/main.py
python services/mcp/main.py
