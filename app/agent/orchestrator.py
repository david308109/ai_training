"""Agent orchestrator: chains retrieve → SQL generation → execute → answer synthesis via LCEL."""

import logging
from typing import Any

from langchain_core.runnables import RunnableBranch, RunnableLambda

from app.db.database import execute_query
from app.retrieval.retriever import retrieve
from app.skills.registry import SkillRegistry

logger = logging.getLogger(__name__)


def _database_step(context: dict[str, Any]) -> dict[str, Any]:
    """Execute the generated SQL and return updated context."""
    # If intent guard rejected the query, skip DB execution
    if context.get("intent") == "CHITCHAT":
        return context

    sql = context.get("generated_sql")
    if not sql:
        return {**context, "query_result": {"error": "No SQL generated"}}

    query_result = execute_query(sql)
    return {**context, "query_result": query_result}


def _retrieval_step(query: str) -> dict[str, Any]:
    """Retrieve context from OpenSearch."""
    try:
        retrieved = retrieve(query)
        return {"question": query, "retrieved": retrieved}
    except Exception as exc:
        logger.error("Retrieval failed: %s", exc)
        return {"question": query, "error": f"Retrieval failed: {exc}"}


def _chitchat_passthrough(context: dict[str, Any]) -> dict[str, Any]:
    """Pass through chitchat responses without synthesis."""
    return context


async def process_query(query: str, registry: SkillRegistry) -> dict[str, Any]:
    """Run the full pipeline for a natural language query using LCEL.

    Steps
    -----
    1. Retrieval (RAG)
    2. SQL Generation & Intent Guard (rejects non-data questions with sql=null)
    3. Database Execution (skipped for chitchat)
    4. Smart Branching (Local Formatter OR AI Synthesis, skipped for chitchat)
    """

    # Skills as Runnables
    sql_skill = registry.get("sql_generation")
    formatter_skill = registry.get("response_formatter")
    synthesis_skill = registry.get("answer_synthesis")

    # Smart Branching logic
    # Branch A: Chitchat — intent guard rejected, pass through directly
    # Branch B: Local Python Formatter (if simple AND successful)
    # Branch C: AI Synthesis (default/fallback)
    branch = RunnableBranch(
        (
            lambda x: x.get("intent") == "CHITCHAT",
            RunnableLambda(_chitchat_passthrough),
        ),
        (
            lambda x: x.get("complexity") == "simple" and x.get("response_template"),
            formatter_skill | (lambda x: x if x.get("format_success") else synthesis_skill),
        ),
        synthesis_skill,
    )

    # Full Chain
    chain = (
        RunnableLambda(_retrieval_step)
        | sql_skill
        | RunnableLambda(_database_step)
        | branch
    )

    try:
        # Execute the chain
        final_output = await chain.ainvoke(query)

        # Build the standard response format
        return {
            "answer": final_output.get("answer", "No answer generated."),
            "generated_sql": final_output.get("generated_sql", ""),
            "query_result": final_output.get("query_result"),
            "error": final_output.get("error"),
        }
    except Exception as exc:
        logger.exception("Chain execution failed")
        return {
            "answer": "系統執行發生錯誤，請稍後再試。",
            "generated_sql": "",
            "query_result": None,
            "error": str(exc),
        }
