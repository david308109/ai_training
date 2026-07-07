## Context

Greenfield project: build a local-first Text-to-SQL data agent for banking domain. Users (Relationship Managers) ask natural language questions about customer deposits; the system generates SQL, executes it against SQLite, and returns natural language answers.

Constraints: local laptop development, no cloud infra, free LLM models via OpenRouter, must use FastAPI + LangChain + OpenSearch.

## Goals / Non-Goals

**Goals:**
- Accurate SQL generation from natural language via RAG-augmented LLM
- Modular "skill" architecture that's easy to extend with new capabilities
- Automated evaluation pipeline comparing generated vs ground truth SQL
- Single-command local setup (Docker for OpenSearch, SQLite for data)

**Non-Goals:**
- Multi-turn conversation / chat memory
- Frontend UI
- Authentication / authorization
- Production-grade deployment or horizontal scaling
- Multi-database support (SQLite only)

## Decisions

### 1. Project Structure — Layered Package Layout

```
app/
├── main.py                  # FastAPI app + /query endpoint
├── config.py                # Settings (OpenRouter key, OpenSearch URL, DB path)
├── db/
│   ├── schema.sql           # DDL + seed data
│   ├── database.py          # SQLite connection + execute helper
│   └── schema_description.py  # Human-readable schema text for LLM
├── knowledge/
│   ├── sql_templates.py     # SQL template definitions with business descriptions
│   ├── business_context.py  # Domain-level context documents
│   └── indexer.py           # Bulk-index into OpenSearch
├── retrieval/
│   ├── embeddings.py        # Embedding model wrapper
│   ├── opensearch_client.py # OpenSearch vector search
│   └── retriever.py         # Top-K retrieval strategy
├── skills/
│   ├── base.py              # Skill ABC
│   ├── sql_generation.py    # LLM → SQL skill
│   ├── answer_synthesis.py  # SQL result → NL answer skill
│   └── registry.py          # Skill registry for orchestration
├── agent/
│   └── orchestrator.py      # Pipeline: retrieve → generate SQL → execute → answer
└── evaluation/
    ├── test_dataset.py      # Ground truth Q&A pairs
    ├── evaluator.py         # SQL comparison logic
    └── run_eval.py          # CLI script for batch evaluation
```

**Rationale**: Clear separation of concerns. Each layer is independently testable. The `skills/` package is the extensibility point.

### 2. Skill Framework — Abstract Base Class + Registry

```python
class Skill(ABC):
    name: str
    description: str
    
    @abstractmethod
    async def execute(self, context: dict) -> dict: ...
```

Skills: `SQLGenerationSkill`, `AnswerSynthesisSkill`. The `SkillRegistry` maps skill names to instances. The orchestrator calls skills by name, enabling future extension (e.g., `ChartGenerationSkill`, `DataValidationSkill`).

**Rationale**: Simple, Pythonic. No over-engineering with complex tool routing — just an ABC and a dict registry. LangChain tools can wrap skills if needed later.

### 3. LLM Provider — OpenRouter via LangChain's ChatOpenAI

Use `ChatOpenAI` with `openai_api_base="https://openrouter.ai/api/v1"`. Model: `google/gemini-2.0-flash-exp:free` (or similar free tier).

**Alternatives considered**:
- Direct OpenRouter HTTP calls → loses LangChain chain composability
- Azure OpenAI → not guaranteed available, keep as optional fallback

### 4. Embedding Strategy — sentence-transformers (local)

Use `sentence-transformers/all-MiniLM-L6-v2` for embedding SQL templates, schema descriptions, and business context. Runs locally, no API cost.

**Alternatives considered**:
- OpenRouter embeddings → no free embedding endpoints reliably available
- OpenAI embeddings → costs money

### 5. Vector DB Index Design — 3 Indices in OpenSearch

| Index | Content | Fields |
|-------|---------|--------|
| `sql_templates` | SQL + business description | `sql`, `description`, `tables`, `embedding` |
| `schema_descriptions` | Table/column descriptions | `table_name`, `description`, `columns`, `embedding` |
| `business_context` | Domain knowledge | `topic`, `content`, `embedding` |

Retrieval: embed user query → kNN search across all 3 indices → combine top-K results → inject into prompt.

### 6. Database — SQLite with Banking Schema

Tables: `customers`, `deposits`, `branches`, `relationship_managers`. Seed with ~50 rows of realistic banking data.

**Rationale**: SQLite requires zero setup. Schema is simple enough for LLM to reason about but complex enough to test joins and aggregations.

### 7. Evaluation — Structural + Result Comparison

Compare generated SQL vs ground truth via:
1. **Structural**: Normalize and compare SQL AST (using `sqlparse`)
2. **Result**: Execute both queries, compare result sets
3. **Manual review**: Log both for human inspection

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Free LLM models may be unreliable/slow | Implement retry logic, allow model swap via config |
| OpenSearch Docker may be heavy on laptops | Provide docker-compose with resource limits; document minimum specs |
| Embedding model quality on banking domain | Fine-tuning not in scope; rely on prompt engineering and good template descriptions |
| SQL injection via LLM-generated SQL | Execute in read-only SQLite connection; parameterize where possible |
| Template coverage gaps | Start with 15+ templates covering common RM queries; document how to add more |
