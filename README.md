# Data Agent — Text-to-SQL

Banking domain data agent that converts natural language questions into SQL, executes them against a SQLite database, and returns human-readable answers. Built with **FastAPI**, **LangChain**, and **OpenSearch**.

## Architecture

```
    User Question
          │
          ▼
┌──────────────────┐     ┌──────────────────┐
│   POST /query    │───➤│  RAG Retrieval   │  ◀── OpenSearch (3 indices)
└──────────────────┘     └────────┬─────────┘
                                  │ max_score
                                  ▼
                          ┌──────────────────┐
                          │   Intent Guard   │  (KNN Score < 0.8?)
                          └────┬────────┬────┘
                               │        │
                            score<0.8 score>=0.8
                          (chitchat)    │
                               │        ▼
                               │  ┌──────────────────┐
                               │  │  SQL Generation  │  ◀── LLM (OpenRouter)
                               │  └────────┬─────────┘
                               │           │ SQL
                               │           ▼
                               │  ┌──────────────────┐
                               │  │ Query Execution  │  ◀── SQLite (read-only)
                               │  └────────┬─────────┘
                               │           │ results
                               ▼           ▼
                        ┌──────────┐ ┌──────────────────┐
                        │  Guided  │ │ Answer Synthesis │  ◀── LLM (OpenRouter)
                        │ Redirect │ │      Skill       │
                        └────┬─────┘ └────────┬─────────┘
                             │                │
                             ▼                ▼
                               JSON Response
```

## Prerequisites

- Python 3.11+
- OpenSearch 2.x / 3.x (Run via Docker OR local Windows/Linux installation)
- [OpenRouter API Key](https://openrouter.ai/) (free tier works)

## Quickstart

### 1. Clone & Install

```bash
# Create venv
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -e ".[dev]"
```

### 2. Configure

Create a `.env` file in the root directory (refer to the settings in `app/config.py`):

```bash
# LLM
OPENROUTER_API_KEY=your_key_here

# OpenSearch
OPENSEARCH_URL=http(s)://localhost:9200
OPENSEARCH_USER=admin
OPENSEARCH_PASSWORD=Admin@123
```

### 3. Start OpenSearch

- **Option A: Local (Windows)**
  Execute `bin\opensearch.bat` in your OpenSearch installation directory.
- **Option B: Docker**
  ```bash
  docker compose up -d
  ```

Wait until OpenSearch is ready (check `http(s)://localhost:9200`).


### 4. Index Knowledge Base

```bash
python -m app.knowledge.indexer
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

### 6. Test it

```bash
# Single query
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Who has the highest deposit?\"}"

# Acceptance test
python tests/test_acceptance.py

# Full evaluation
python -m app.evaluation.run_eval

### 7. Verify Data (Optional)

If you have **OpenSearch Dashboards** installed:
1. Run `opensearch-dashboards.bat`.
2. Access `http(s)://localhost:5601` (User/Pass: admin/admin).
3. Open the main menu (☰) on the top left and select **Discover**.
4. Select or create an Index Pattern matching your index (e.g., `sql_templates*`) to inspect the documents.
```

## Project Structure

```
app/
├── main.py                    # FastAPI app + /query endpoint
├── config.py                  # Settings (env vars)
├── db/
│   ├── schema.sql             # DDL + seed data
│   ├── database.py            # SQLite connection + execute helper
│   └── schema_description.py  # Human-readable schema for LLM
├── knowledge/
│   ├── sql_templates.py       # 18 SQL templates with descriptions
│   ├── business_context.py    # Banking domain context docs
│   └── indexer.py             # Bulk-index into OpenSearch
├── retrieval/
│   ├── embeddings.py          # Local sentence-transformers wrapper
│   ├── opensearch_client.py   # OpenSearch vector search
│   └── retriever.py           # Multi-index RAG retrieval
├── skills/
│   ├── base.py                # Skill ABC
│   ├── registry.py            # Skill registry
│   ├── sql_generation.py      # NL → SQL skill
│   └── answer_synthesis.py    # SQL result → NL answer skill
├── agent/
│   └── orchestrator.py        # Pipeline orchestration
└── evaluation/
    ├── test_dataset.py        # 18 ground truth test cases
    ├── evaluator.py           # SQL comparison logic
    └── run_eval.py            # CLI batch evaluation
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM Provider | OpenRouter (free tier) | Zero cost, model swappable via config |
| Embedding | sentence-transformers (local) | No API cost, fast, good enough for this domain |
| Vector DB | OpenSearch | Required by spec; kNN with HNSW via Lucene (Compatible with 3.x) |
| Database | SQLite | Zero setup, single file, read-only enforcement |
| Skill Pattern | ABC + Registry | Simple, extensible, no over-engineering |
| **Schema Handling** | **Dynamic RAG Selection** | **Reduces token usage, avoids LLM confusion with irrelevant tables, includes fallback logic for reliability.** |
| **Intent Guard** | **KNN Score Threshold in Retrieval Step** | **Zero LLM calls for chitchat/non-DB queries. If highest retrieval score < 0.5, pipeline directly returns guided response.** |

## API

### `POST /query`

**Request:**
```json
{"query": "Who has the highest total deposit?"}
```

**Response:**
```json
{
  "answer": "The customer with the highest total deposit is Michael Su with 19,500,000 TWD.",
  "generated_sql": "SELECT c.customer_name, SUM(d.amount) AS total_deposit FROM deposits d JOIN customers c ON d.customer_id = c.customer_id GROUP BY c.customer_id ORDER BY total_deposit DESC LIMIT 1",
  "query_result": {
    "columns": ["customer_name", "total_deposit"],
    "rows": [["Michael Su", 19500000.0]],
    "row_count": 1
  }
}
```

### `GET /health`

Returns `{"status": "ok"}`.
