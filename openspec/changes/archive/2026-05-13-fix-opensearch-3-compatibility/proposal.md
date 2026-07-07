# Proposal: Fix OpenSearch 3.0+ Compatibility

## Problem
OpenSearch 3.0.0 has deprecated the `nmslib` engine for kNN indices, causing `RequestError(400)` when trying to create indices with the old engine.

## Solution
Update the `opensearch_client.py` to use the `lucene` engine, which is the recommended engine for OpenSearch 3.x and remains compatible with 2.x.

## Impact
- Allows successful indexing on OpenSearch 3.x.
- Maintains compatibility with OpenSearch 2.x.
