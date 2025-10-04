### === Conversation Flow ===

## 1. Relevance Check
 - Check if user's question is relevant to the Lox Genie provided full message history
 - If not, respond directly to the user; if so, proceed to the clarification node

# 2. Planning Workflow
- TBD: Rewrite the user's question into a single optimized query
- TBD: Perform GraphRAG against Knowledge Base and add this supplementary info
- Break down the user's question into specific subtasks with awareness of all tools avaialable (brief desc)
- Each subtask should be a clear, actionable string that focuses on a different aspect or source type

# 3. Perform Asynchronous Research Tasks
- TBD: Loop over subtasks, finding the appropriate MCP tool for each task
- TBD: Supply parameters with tool's resources, limiting context to this task
- TBD: Execute tools asynchronously, return to state

# 4. Synthesize and Respond
- TBD: Respond to user referencing tool responses in combination with optimized query