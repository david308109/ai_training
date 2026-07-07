## Why

We need a Data Agent that lets business users (e.g., Relationship Managers) query banking data using natural language instead of writing SQL. This eliminates the gap between domain expertise and data access, enabling self-service analytics on customer deposit data without requiring SQL knowledge.

## What Changes

- New FastAPI service with a single `POST /query` endpoint accepting natural language, returning natural language answers + generated SQL
- RAG pipeline: retrieve SQL templates, database schema, and business context from OpenSearch vector DB to augment LLM prompts
- LangChain-based LLM orchestration with OpenRouter (free models) as primary provider
- SQLite banking database with seed data (CustomerDeposit, branches, RMs)
- "Skills" architecture for extensible, modular agent capabilities (SQL generation, retrieval, answer synthesis)
- Test dataset with ground truth SQL and automated evaluation script

## Capabilities

### New Capabilities
- `database-schema`: Banking domain SQLite schema design, seed data, and schema-as-text for LLM consumption
- `vector-knowledge-base`: OpenSearch index construction for SQL templates, schema descriptions, and business context embeddings
- `rag-retrieval`: Embedding-based retrieval strategy mapping user queries to relevant SQL templates, schema, and business context
- `sql-generation`: LangChain-powered LLM skill that takes retrieved context + user query and generates executable SQL
- `query-execution`: SQL execution against SQLite and result formatting
- `answer-synthesis`: LLM skill that converts SQL results + original question into natural language answers
- `api-endpoint`: FastAPI POST /query endpoint orchestrating the full pipeline
- `skill-framework`: Extensible skill/tool abstraction for modular agent design
- `test-evaluation`: Test dataset with ground truth SQL, evaluation script comparing structural/logical/result correctness

### Modified Capabilities
_(none — greenfield project)_

## Impact

- **New dependencies**: FastAPI, LangChain, OpenSearch Python client, sentence-transformers (or OpenRouter embeddings), SQLite3
- **Infrastructure**: Local OpenSearch instance required (Docker recommended)
- **APIs**: Single new endpoint `POST /query`
- **No breaking changes**: Greenfield project
