"""OpenSearch client for vector search."""

import logging
from typing import Any

from opensearchpy import OpenSearch

from app.config import settings

logger = logging.getLogger(__name__)

# Initialize OpenSearch client
client = OpenSearch(
    hosts=[settings.opensearch_url],
    http_auth=(settings.opensearch_user, settings.opensearch_password),
    use_ssl=False,  # Set to True if using HTTPS
    verify_certs=False,
    ssl_show_warn=False,
)


def create_knn_index(index_name: str, extra_mappings: dict = None) -> None:
    """Create a kNN-enabled index in OpenSearch."""
    settings_body = {
        "settings": {
            "index": {
                "knn": True,
                "knn.algo_param.ef_search": 100,
            }
        },
        "mappings": {
            "properties": {
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384,  # Matches all-MiniLM-L6-v2
                    "method": {
                        "name": "hnsw",
                        "space_type": "cosinesimil",
                        "engine": "lucene",
                    },
                }
            }
        },
    }
    if extra_mappings:
        settings_body["mappings"]["properties"].update(extra_mappings)

    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
        logger.info("Deleted existing index: %s", index_name)

    client.indices.create(index=index_name, body=settings_body)
    logger.info("Created kNN index: %s", index_name)


def bulk_index(index_name: str, documents: list[dict[str, Any]]) -> int:
    """Index multiple documents into OpenSearch."""
    body = ""
    for doc in documents:
        body += '{"index": {"_index": "' + index_name + '"}}\n'
        import json

        body += json.dumps(doc) + "\n"

    if body:
        resp = client.bulk(body=body)
        if resp.get("errors"):
            logger.error("Bulk indexing errors: %s", resp)
        return len(documents)
    return 0


def knn_search(
    index_name: str,
    query_vector: list[float],
    k: int = 3,
    source_fields: list[str] = None,
) -> list[dict[str, Any]]:
    """Perform a kNN search in OpenSearch."""
    query = {
        "size": k,
        "query": {"knn": {"embedding": {"vector": query_vector, "k": k}}},
    }
    if source_fields:
        query["_source"] = source_fields

    try:
        resp = client.search(index=index_name, body=query)
        hits = resp["hits"]["hits"]
        results = []
        for hit in hits:
            res = hit["_source"]
            res["_score"] = hit["_score"]
            results.append(res)
        return results
    except Exception as e:
        logger.error("Search error in index %s: %s", index_name, e)
        return []
