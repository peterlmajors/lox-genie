## === Architecture ===

### Core Components

#### State Management (`schemas.py`)

- **AgentState**: Central state container managing conversation flow
  - `thread_id`: Unique identifier for conversation sessions
  - `messages`: Chronological list of HumanMessage/AIMessage objects
  - `message_counts`: Tracks human vs AI message distribution
  - `reduced_context`: Moderate-term memory for context compression
  - `relevant`: Boolean flag for relevance assessment
  - `plan`: List of PlanResponse objects containing subtasks
  - `tool_calls`: History of tool executions with reasoning

#### Configuration (`config.py`)

- **Configuration**: Pydantic-based config management
  - `planning_agent_model`: LLM for task planning (default: gemini-2.5-flash-lite)
  - `relevance_agent_model`: LLM for relevance assessment (default: gemini-2.5-flash-lite)
  - Environment variable integration via `from_runnable_config()`

#### Graph Architecture (`graph.py`)

- **StateGraph**: LangGraph-based workflow orchestration
  - **Nodes**: relevance → human_in_loop → planner → executor
  - **Edges**: Conditional routing based on relevance assessment
  - **Configuration**: Schema-driven config injection

### Node Implementations

#### Relevance Assessment

- Validates user query relevance against conversation context
- Returns boolean flag with reasoning for irrelevant queries
- Conditional edge routing to human_in_loop or planner

#### Human-in-the-Loop

- Dynamic prompt generation based on user question
- Handles clarification requests and context gathering
- Routes back to relevance for re-evaluation

#### Planning Engine

- Breaks down complex queries into actionable subtasks
- Generates unique plan IDs for tracking
- Creates structured task lists for tool execution

#### Plan Executor

- Maps subtasks to appropriate MCP tools
- Handles parameter extraction and tool invocation
- Maintains execution history with reasoning

### Utility Functions (`utils.py`)

- **Message Counting**: Tracks conversation statistics
- **Tool Registry**: Centralized tool definitions and schemas
- **Date Utilities**: Current date formatting for context

### Data Flow

1. **Input**: User message → AgentState.messages
2. **Relevance**: Context validation → conditional routing
3. **Planning**: Query decomposition → subtask generation
4. **Execution**: Tool mapping → async execution → state update
5. **Response**: Synthesis → AIMessage generation

### Configuration Integration

- Environment-based model selection
- RunnableConfig compatibility for LangChain integration
- Pydantic validation for type safety and documentation
