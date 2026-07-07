"""RAG retriever: searches all 3 OpenSearch indices and combines results."""

import logging

from app.config import settings
from app.knowledge.indexer import (
    INDEX_BUSINESS_CONTEXT,
    INDEX_SCHEMA_DESCRIPTIONS,
    INDEX_SQL_TEMPLATES,
)
from app.retrieval.embeddings import embed_text
from app.retrieval.opensearch_client import knn_search

logger = logging.getLogger(__name__)


def retrieve(query: str, top_k: int | None = None) -> dict:
    """Retrieve relevant context from all 3 indices for a user query.

    Parameters
    ----------
    query : str
        Natural language user query.
    top_k : int, optional
        Number of results per index. Defaults to ``settings.retrieval_top_k``.

    Returns
    -------
    dict
        Keys: ``sql_templates``, ``schema_descriptions``, ``business_context``.
        Each value is a list of matching documents (without embeddings).
    """
    k = top_k or settings.retrieval_top_k
    query_vector = embed_text(query)

    sql_results = knn_search(
        INDEX_SQL_TEMPLATES,
        query_vector,
        k=k,
        source_fields=["sql", "description", "tables"],
    )

    schema_results = knn_search(
        INDEX_SCHEMA_DESCRIPTIONS,
        query_vector,
        k=k,
        source_fields=["table_name", "description", "columns"],
    )

    biz_results = knn_search(
        INDEX_BUSINESS_CONTEXT,
        query_vector,
        k=k,
        source_fields=["topic", "content"],
    )

    logger.debug(
        "Retrieved %d templates, %d schemas, %d biz docs for query: %s",
        len(sql_results),
        len(schema_results),
        len(biz_results),
        query[:80],
    )

    return {
        "sql_templates": sql_results,
        "schema_descriptions": schema_results,
        "business_context": biz_results,
    }
