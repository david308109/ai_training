"""Bulk-index SQL templates, schema descriptions, and business context into OpenSearch."""

import logging

from app.db.schema_description import SCHEMA_DESCRIPTIONS_FOR_INDEX
from app.knowledge.business_context import BUSINESS_CONTEXT
from app.knowledge.sql_templates import SQL_TEMPLATES
from app.retrieval.embeddings import embed_texts
from app.retrieval.opensearch_client import bulk_index, create_knn_index

logger = logging.getLogger(__name__)

INDEX_SQL_TEMPLATES = "sql_templates"
INDEX_SCHEMA_DESCRIPTIONS = "schema_descriptions"
INDEX_BUSINESS_CONTEXT = "business_context"


def index_sql_templates() -> int:
    """Index SQL templates into OpenSearch."""
    create_knn_index(
        INDEX_SQL_TEMPLATES,
        extra_mappings={
            "sql": {"type": "text"},
            "description": {"type": "text"},
            "tables": {"type": "keyword"},
        },
    )
    texts = [t["description"] for t in SQL_TEMPLATES]
    embeddings = embed_texts(texts)

    docs = []
    for tmpl, emb in zip(SQL_TEMPLATES, embeddings):
        docs.append({**tmpl, "embedding": emb})

    count = bulk_index(INDEX_SQL_TEMPLATES, docs)
    logger.info("Indexed %d SQL templates", count)
    return count


def index_schema_descriptions() -> int:
    """Index schema descriptions into OpenSearch."""
    create_knn_index(
        INDEX_SCHEMA_DESCRIPTIONS,
        extra_mappings={
            "table_name": {"type": "keyword"},
            "description": {"type": "text"},
            "columns": {"type": "text"},
        },
    )
    texts = [
        f"{s['table_name']}: {s['description']} Columns: {s['columns']}"
        for s in SCHEMA_DESCRIPTIONS_FOR_INDEX
    ]
    embeddings = embed_texts(texts)

    docs = []
    for schema, emb in zip(SCHEMA_DESCRIPTIONS_FOR_INDEX, embeddings):
        docs.append({**schema, "embedding": emb})

    count = bulk_index(INDEX_SCHEMA_DESCRIPTIONS, docs)
    logger.info("Indexed %d schema descriptions", count)
    return count


def index_business_context() -> int:
    """Index business context documents into OpenSearch."""
    create_knn_index(
        INDEX_BUSINESS_CONTEXT,
        extra_mappings={
            "topic": {"type": "keyword"},
            "content": {"type": "text"},
        },
    )
    texts = [f"{bc['topic']}: {bc['content']}" for bc in BUSINESS_CONTEXT]
    embeddings = embed_texts(texts)

    docs = []
    for bc, emb in zip(BUSINESS_CONTEXT, embeddings):
        docs.append({**bc, "embedding": emb})

    count = bulk_index(INDEX_BUSINESS_CONTEXT, docs)
    logger.info("Indexed %d business context docs", count)
    return count


def index_all() -> dict[str, int]:
    """Run all indexers. Returns counts per index."""
    logger.info("Starting full indexing...")
    results = {
        INDEX_SQL_TEMPLATES: index_sql_templates(),
        INDEX_SCHEMA_DESCRIPTIONS: index_schema_descriptions(),
        INDEX_BUSINESS_CONTEXT: index_business_context(),
    }
    logger.info("Indexing complete: %s", results)
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    index_all()
