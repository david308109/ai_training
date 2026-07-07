# Design: Update OpenSearch Engine to Lucene

## Implementation Detail
Modify `app/retrieval/opensearch_client.py`'s `create_knn_index` function.

Change:
```python
"method": {
    "name": "hnsw",
    "space_type": "cosinesimil",
    "engine": "nmslib",
}
```
to:
```python
"method": {
    "name": "hnsw",
    "space_type": "cosinesimil",
    "engine": "lucene",
}
```
