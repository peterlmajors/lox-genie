# API Routes Documentation

## Chat Routes with Gemini AI Integration

The chat routes provide AI-powered conversation capabilities using Google's Gemini API.

### Setup

1. **Install Dependencies**: The `google-generativeai` package is included in `requirements-api.txt`

2. **Environment Configuration**: Add your Gemini API key to your `.env` file:

   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-1.5-flash  # Optional, defaults to gemini-1.5-flash
   ```

3. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to obtain your Gemini API key

### Available Endpoints

#### 1. POST `/chat/chat`

Full-featured chat endpoint with conversation history and advanced parameters.

**Request Body:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What are the top 5 fantasy football running backs for 2025?",
      "timestamp": "2025-01-15T10:00:00Z"
    }
  ],
  "stream": false,
  "temperature": 0.7,
  "max_tokens": 1000,
  "system_prompt": "You are a helpful AI assistant for fantasy football analysis."
}
```

**Response:**

```json
{
  "response": "Based on current projections for the 2025 season...",
  "usage": {
    "prompt_tokens": 45,
    "completion_tokens": 234
  },
  "model": "gemini-1.5-flash"
}
```

#### 2. POST `/chat/chat/stream`

Streaming chat endpoint for real-time responses.

**Request Body:** Same as regular chat endpoint, but set `"stream": true`

**Response:** Server-Sent Events (SSE) stream with chunks of text

#### 3. POST `/chat/chat/simple`

Simple chat endpoint for basic queries without conversation history.

**Request Body:**

```json
{
  "message": "Who is the best quarterback in fantasy football?"
}
```

**Response:**

```json
{
  "response": "Patrick Mahomes is widely considered..."
}
```

#### 4. GET `/chat/models`

Get information about available Gemini models and configuration status.

**Response:**

```json
{
  "configured": true,
  "current_model": "gemini-1.5-flash",
  "available_models": ["gemini-1.5-flash", "gemini-1.5-pro"],
  "api_key_configured": true
}
```

#### 5. GET `/chat/health`

Health check for the chat service.

**Response:**

```json
{
  "status": "healthy",
  "gemini_configured": true,
  "model": "gemini-1.5-flash",
  "service": "chat"
}
```

### Features

- **Conversation History**: Maintains context across multiple messages
- **Streaming Responses**: Real-time streaming for better user experience
- **Configurable Parameters**: Temperature, max tokens, and system prompts
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Health Monitoring**: Service health checks and configuration validation
- **Type Safety**: Full Pydantic model validation for requests and responses

### Error Handling

The API returns appropriate HTTP status codes:

- `200`: Successful response
- `400`: Bad request (invalid parameters)
- `500`: Internal server error
- `503`: Service unavailable (Gemini not configured)

### Example Usage

```python
import httpx

# Simple chat
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/chat/chat/simple",
        json={"message": "Tell me about fantasy football strategy"}
    )
    print(response.json()["response"])

# Full chat with history
messages = [
    {"role": "user", "content": "What is PPR in fantasy football?"},
    {"role": "assistant", "content": "PPR stands for Points Per Reception..."},
    {"role": "user", "content": "How does it affect running back values?"}
]

response = await client.post(
    "http://localhost:8000/chat/chat",
    json={"messages": messages, "temperature": 0.8}
)
print(response.json()["response"])
```

### Security Notes

- Keep your Gemini API key secure and never commit it to version control
- Use environment variables for configuration
- Consider implementing rate limiting for production use
- Monitor API usage to manage costs
