## 1. Project Setup

- [x] 1.1 Initialize Python project with `pyproject.toml` (or `requirements.txt`), set up `app/` package structure as defined in design.md
- [x] 1.2 Create `app/config.py` with settings: OpenRouter API key, OpenSearch URL, SQLite DB path, embedding model name, top-K config
- [x] 1.3 Create `docker-compose.yml` for OpenSearch (single-node, resource-limited for laptop)
- [x] 1.4 Create `README.md` with setup instructions, prerequisites, and quickstart

## 2. Database Schema & Seed Data

- [x] 2.1 Create `app/db/schema.sql` with DDL for `customers`, `deposits`, `branches`, `relationship_managers` tables with foreign keys
- [x] 2.2 Add seed data (~50 records) with realistic banking values to `schema.sql`
- [x] 2.3 Create `app/db/database.py` with SQLite connection helper, `execute_query()` (read-only, with timeout), and `init_db()` function
- [x] 2.4 Create `app/db/schema_description.py` with human-readable schema text optimized for LLM consumption
- [x] 2.5 Verify: run `init_db()` and execute a sample SELECT to confirm schema + seed data

## 3. Knowledge Base Content

- [x] 3.1 Create `app/knowledge/sql_templates.py` with 15+ SQL templates, each with `sql`, `description`, `tables` fields
- [x] 3.2 Create `app/knowledge/business_context.py` with domain-level context documents (RM role, deposit types, branch hierarchy, etc.)
- [x] 3.3 Verify: import modules and print template count + business context count

## 4. Embedding & OpenSearch Indexing

- [x] 4.1 Create `app/retrieval/embeddings.py` wrapping `sentence-transformers/all-MiniLM-L6-v2` with `embed_text(text) -> list[float]` and `embed_texts(texts) -> list[list[float]]`
- [x] 4.2 Create `app/retrieval/opensearch_client.py` with OpenSearch connection, index creation (kNN settings), and search helpers
- [x] 4.3 Create `app/knowledge/indexer.py` to bulk-index SQL templates, schema descriptions, and business context into 3 OpenSearch indices (idempotent: delete + recreate)
- [x] 4.4 Verify: start OpenSearch via Docker, run indexer, confirm documents indexed with `GET _cat/indices`

## 5. RAG Retrieval

- [x] 5.1 Create `app/retrieval/retriever.py` with `retrieve(query: str, top_k: int) -> dict` that searches all 3 indices and combines results
- [x] 5.2 Verify: test retriever with sample queries ("highest deposit", "top customers by branch") and inspect retrieved results

## 6. Skill Framework

- [x] 6.1 Create `app/skills/base.py` with `Skill` ABC (`name`, `description`, `execute(context) -> dict`)
- [x] 6.2 Create `app/skills/registry.py` with `SkillRegistry` (register, get, list_skills)
- [x] 6.3 Verify: create a dummy skill, register it, retrieve it by name

## 7. SQL Generation Skill

- [x] 7.1 Create `app/skills/sql_generation.py` implementing `SQLGenerationSkill` using LangChain `ChatOpenAI` (OpenRouter base URL) with prompt template that includes retrieved context + schema + user query
- [x] 7.2 Implement SQL extraction logic (strip markdown code blocks, validate basic SQL structure)
- [x] 7.3 Verify: test SQL generation with a hardcoded retrieved context and user query

## 8. Answer Synthesis Skill

- [x] 8.1 Create `app/skills/answer_synthesis.py` implementing `AnswerSynthesisSkill` that takes SQL results + original question and generates natural language answer via LLM
- [x] 8.2 Handle edge cases: empty results, error results
- [x] 8.3 Verify: test with sample SQL results and questions

## 9. Agent Orchestrator & API

- [x] 9.1 Create `app/agent/orchestrator.py` with `process_query(query: str) -> dict` that chains: retrieve ??SQL generation skill ??execute SQL ??answer synthesis skill
- [x] 9.2 Create `app/main.py` with FastAPI app, `POST /query` endpoint, startup event (init DB, register skills)
- [x] 9.3 Verify: start server, send a test query via curl/httpie, confirm full pipeline response

## 10. Test Dataset & Evaluation

- [x] 10.1 Create `app/evaluation/test_dataset.py` with 15+ test cases (question + expected SQL)
- [x] 10.2 Create `app/evaluation/evaluator.py` with SQL comparison logic (structural via sqlparse normalization, result-set comparison)
- [x] 10.3 Create `app/evaluation/run_eval.py` CLI script that runs all test cases against the API and prints accuracy metrics
- [x] 10.4 Create `tests/test_acceptance.py` with the simple acceptance test script (requests.post to /query)
- [x] 10.5 Run evaluation, document results in README

## 11. Polish & Documentation

- [x] 11.1 Add error handling and logging throughout the pipeline
- [x] 11.2 Update README with architecture diagram, design decisions, evaluation results
- [x] 11.3 Final end-to-end verification: docker-compose up, init DB, index knowledge, start API, run evaluation
