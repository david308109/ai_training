"""Local embedding model wrapper using sentence-transformers."""

import logging
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    logger.info("Loading embedding model: %s", settings.embedding_model)
    return SentenceTransformer(settings.embedding_model)


def get_embedding_dim() -> int:
    """Return the dimensionality of the embedding vectors."""
    model = _get_model()
    return model.get_sentence_embedding_dimension()


def embed_text(text: str) -> list[float]:
    """Embed a single text string and return a dense vector."""
    model = _get_model()
    vec = model.encode(text, normalize_embeddings=True)
    return vec.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed multiple texts in a single batch."""
    model = _get_model()
    vecs = model.encode(texts, normalize_embeddings=True, batch_size=32)
    return vecs.tolist()
