# === Development Plans ===

Short Term
- Get local serving of chat endpoint to agent to work
- Integrate vllm to enhance local model inference times
- Build knowledge bases for all position classes and niches
- Upload knowledge base to AWS S3 bucket as MCP resources
- Deploy application to fleet of AWS EC2 instances
- Improve context gathering within gatekeeper

Medium Term
- Build LLM pipeline to extract lessons from fantasy football YouTube channels 
- Find and structure organized outputs for as many NFL APIs as possible
- Search for useful MCP servers we can use, instead of building custom
- Store all chat histories in AWS Dynamo DB for quick relational use

Long Term
- Enable up/downvote on specific responses to reduce context poison
- Personal preference memory bank by user in AWS vector store
- Integrate AWS ElasticCache for all MCP tools and sleeper endpoints
- Fine-tune open source model for better inference speed and performance