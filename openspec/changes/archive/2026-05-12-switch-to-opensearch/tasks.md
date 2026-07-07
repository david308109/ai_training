## 1. Configuration & Dependencies

- [x] 1.1 Add `opensearch-py` to `requirements.txt`.
- [x] 1.2 Update `app/config.py` to include OpenSearch settings (URL, User, Password, Verify SSL).
- [x] 1.3 Add OpenSearch connection placeholders to `.env`.

## 2. OpenSearch Client Implementation

- [x] 2.1 Create `app/retrieval/opensearch_client.py` with connection logic and kNN index mapping helpers.
- [x] 2.2 Implement `bulk_index` and `knn_search` in `app/retrieval/opensearch_client.py`.

## 3. Retrieval Refactoring

- [x] 3.1 Refactor `app/retrieval/vector_store.py` to use `opensearch_client.py` (removing FAISS dependencies).
- [x] 3.2 Verify `app/retrieval/retriever.py` compatibility with the new vector store implementation.

## 4. Data Indexing & Validation

- [x] 4.1 Update `app/knowledge/indexer.py` to use the new OpenSearch-based indexing functions.
- [x] 4.2 Run `python -m app.knowledge.indexer` to populate OpenSearch indices.
- [x] 4.3 Verify the end-to-end flow by running `pytest tests/test_acceptance.py`.
