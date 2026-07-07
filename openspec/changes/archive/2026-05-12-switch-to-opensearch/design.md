## Context

The current vector storage relies on FAISS files stored locally. While functional, this diverges from the project's core requirement to use OpenSearch. The user has set up a local OpenSearch environment on Windows, and we need to migrate the retrieval logic to this new infrastructure.

## Goals / Non-Goals

**Goals:**
- Replace FAISS with OpenSearch as the primary vector database.
- Support kNN vector search using the HNSW algorithm (Lucene engine).
- Maintain compatibility with the existing `Skill` and `Orchestrator` framework.
- Enable easy configuration for both local and cloud OpenSearch instances.

**Non-Goals:**
- Implementing advanced OpenSearch features like cross-cluster search or fine-grained access control.
- Migrating historical query logs (out of scope for this RAG fix).

## Decisions

### 1. Vector Database Client
- **Choice**: `opensearch-py`.
- **Rationale**: Official Python client, supports both standard and vector search operations.
- **Alternative**: `langchain-opensearch` community package. Chosen `opensearch-py` directly for more granular control over index mappings (essential for kNN/HNSW).

### 2. Index Design
- **Indices**: Three separate indices: `sql_templates`, `schema_descriptions`, and `business_context`.
- **Engine**: kNN with HNSW.
- **Distance Metric**: `l2` (standard for many embedding models, but will be configurable).

### 3. Configuration Management
- **Changes**: Add `opensearch_url`, `opensearch_user`, and `opensearch_password` to `app/config.py`.
- **Default**: Point to `http://localhost:9200` for local developer convenience.

## Risks / Trade-offs

- **[Risk]** OpenSearch may fail to start or have high memory overhead on some machines.
  - **Mitigation**: Provide clear connection error messages and document minimum memory requirements.
- **[Trade-off]** OpenSearch is more complex to manage than local FAISS files.
  - **Rationale**: Required by project specs; enables standard search tool integration.
