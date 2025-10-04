## === Context ===
- Knowledge Graph limits topical scope and token costs for planner

- Planning tasks independent of calling tools and determining parameters:

  - Allows for scalable planning without planner being overwhelmed by parameter context
  - Avoids limitations of simple embeddings based retrieval on each task
  - May be risks associated with decoupling task & tool call

# === Reasoning ===:
- LLM attempts at generalization are correlational, not casual or grounded in reality
- Find the smallest set of high-signal tokens that maximize the likelihood of a desired outcome