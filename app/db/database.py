"""SQLite database connection and query execution helpers."""

import logging
import re
import sqlite3
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

_WRITE_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|REPLACE)\b",
    re.IGNORECASE,
)


def _db_path() -> Path:
    p = Path(settings.db_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def get_connection(readonly: bool = False) -> sqlite3.Connection:
    """Return a new SQLite connection. Set *readonly* for query execution."""
    path = _db_path()
    if readonly:
        uri = f"file:{path}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=settings.query_timeout_seconds)
    else:
        conn = sqlite3.connect(str(path), timeout=settings.query_timeout_seconds)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables and load seed data from schema.sql (idempotent)."""
    schema_file = Path(__file__).parent / "schema.sql"
    sql = schema_file.read_text(encoding="utf-8")

    conn = get_connection()
    try:
        conn.executescript(sql)
        conn.commit()
        logger.info("Database initialised at %s", _db_path())
    finally:
        conn.close()


def execute_query(sql: str) -> dict:
    """Execute a **read-only** SQL query and return structured results.

    Returns
    -------
    dict
        ``{"columns": [...], "rows": [[...], ...], "row_count": int}``
        or ``{"error": "..."}`` on failure.
    """
    # Guard against write operations
    if _WRITE_PATTERN.search(sql):
        return {"error": "Write operations are not allowed. Only SELECT queries are permitted."}

    conn = get_connection(readonly=True)
    try:
        cursor = conn.execute(sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = [list(row) for row in cursor.fetchall()]
        return {"columns": columns, "rows": rows, "row_count": len(rows)}
    except sqlite3.OperationalError as exc:
        logger.error("SQL execution error: %s", exc)
        return {"error": f"SQL execution failed: {exc}"}
    except Exception as exc:
        logger.error("Unexpected error executing SQL: %s", exc)
        return {"error": f"Unexpected error: {exc}"}
    finally:
        conn.close()
