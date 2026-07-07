## Why

The project specification mandates OpenSearch as the vector database, but the current implementation uses FAISS. This change refactors the retrieval system to use a local or cloud OpenSearch instance, ensuring compliance with architectural requirements and enabling features like OpenSearch Dashboards.

## What Changes

- Update configuration to support OpenSearch connection (URL, auth).
- Implement OpenSearch client for vector operations.
- Replace FAISS-based vector store with OpenSearch.
- Update data indexing pipeline to target OpenSearch.
- Update README and documentation to reflect the actual infrastructure.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `vector-knowledge-base`: Requirements now strictly enforce OpenSearch for vector indexing and storage.
- `rag-retrieval`: Retrieval logic is updated to interface with OpenSearch indices for SQL templates, schema, and business context.

## Impact

- **Dependencies**: Adds `opensearch-py`.
- **Infrastructure**: Requires an active OpenSearch instance (local installation or AWS).
- **Code**: Affects `app/config.py`, `app/retrieval/`, and `app/knowledge/`.
