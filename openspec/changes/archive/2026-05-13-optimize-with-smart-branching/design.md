## Context

The current orchestrator implementation is a sequential Python function that always executes two LLM calls: one for SQL generation and one for answer synthesis. This leads to unnecessary latency and cost for simple queries where the answer can be directly derived from the SQL result (e.g., "What is the balance of account X?").

## Goals / Non-Goals

**Goals:**
- Implement a LangChain LCEL-based orchestrator.
- Reduce LLM calls to 1x for "simple" queries.
- Maintain high-quality AI synthesis for "complex" queries.
- Ensure system robustness via an automatic fallback mechanism.

**Non-Goals:**
- Changing the underlying database (SQLite).
- Changing the RAG retrieval logic (OpenSearch).
- Implementing multi-turn conversation.

## Decisions

### 1. AI-Driven Complexity Classification
We will modify the `SQLGenerationSkill` prompt to return a structured JSON response instead of raw SQL. This JSON will include a `complexity` field (`simple` or `complex`).
- **Rationale**: The LLM generating the SQL has the best context to determine if the result will be a simple value or a complex dataset requiring analysis.
- **Alternatives**: Rule-based classification based on SQL keywords (unreliable) or result set size (too late in the pipeline).

### 2. Response Templating for Simple Queries
For queries marked as `simple`, the LLM will also provide a `response_template` (e.g., "The balance is {balance} TWD.").
- **Rationale**: Allows for immediate natural language generation in Python without a second LLM call.

### 3. Orchestration via LangChain LCEL `RunnableBranch`
The orchestrator will be refactored using LCEL. A `RunnableBranch` will route the execution:
- **Condition**: `complexity == "simple"` AND `format_success == True`.
- **Branch A**: Local Python formatting.
- **Branch B (Default)**: AI Answer Synthesis.

### 4. Robust Fallback Mechanism
If the Python formatting fails (e.g., due to key mismatch in the template), the system will automatically route the data to the `AnswerSynthesisSkill`.
- **Rationale**: Prioritizes correctness over optimization.

## Risks / Trade-offs

- **[Risk]** LLM provides a template with keys that don't match the SQL aliases.
  - **Mitigation**: Use a try-except block in the local formatter; if a `KeyError` occurs, fallback to full AI synthesis.
- **[Risk]** Increased prompt complexity for SQL generation.
  - **Mitigation**: Provide clear examples in the prompt for the JSON structure and alias naming conventions.
- **[Trade-off]** LCEL can be harder to debug than standard Python.
  - **Mitigation**: Use descriptive names for Runnables and consider enabling LangSmith for tracing during development.
