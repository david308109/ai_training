## Why

To reduce system latency and operational costs by minimizing redundant LLM calls for straightforward data lookups. Currently, every query requires two LLM calls (generation + synthesis). This change introduces a smart branching mechanism to handle simple queries with a single LLM call using local Python formatting, while maintaining full AI synthesis for complex analytical queries.

## What Changes

- **Structured SQL Generation**: Modify the `sql-generation` skill to output JSON containing the SQL query, a complexity classification (`simple` vs `complex`), and a natural language response template for simple cases.
- **Smart Branching Logic**: Implement a `RunnableBranch` in the orchestrator to route queries based on the AI's complexity judgment.
- **Local Response Formatting**: Add a Python-based formatter to populate templates with database results for simple queries, avoiding the second LLM call.
- **Auto-Fallback Mechanism**: Ensure the system gracefully falls back to full AI synthesis if local formatting fails or keys mismatch.
- **LangChain LCEL Refactor**: Rebuild the orchestrator using LangChain Expression Language (LCEL) to improve framework compliance and observability.

## Capabilities

### New Capabilities
- `smart-branching`: Orchestration logic that conditionally routes between local formatting and AI synthesis based on query complexity.

### Modified Capabilities
- `skill-framework`: Update the framework to support LangChain LCEL components and structured JSON outputs.
- `sql-generation`: Update requirement to include complexity judging and template generation in a single pass.
- `answer-synthesis`: Convert this into an optional branch in the pipeline rather than a mandatory step.

## Impact

- `app/agent/orchestrator.py`: Major refactor to LCEL.
- `app/skills/sql_generation.py`: Update prompt and output parsing.
- `app/skills/answer_synthesis.py`: Minor updates to integrate into the branch logic.
- `app/main.py`: Update to support the new pipeline structure.
