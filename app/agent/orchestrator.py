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


CHITCHAT_RESPONSE = (
    "您好！我是銀行數據分析助手，專門回答與銀行資料相關的問題。\n\n"
    "您可以問我類似這樣的問題：\n"
    "- 目前共有多少客戶？\n"
    "- 各分行的存款總額是多少？\n"
    "- 哪位客戶經理管理最多客戶？\n\n"
    "請問您有什麼資料方面的問題想了解呢？"
)

RETRIEVAL_INTENT_THRESHOLD = 0.8


def _retrieval_step(query: str) -> dict[str, Any]:
    """Retrieve context from OpenSearch and check similarity score."""
    try:
        retrieved = retrieve(query)

        # 算最高分
        max_score = 0.0
        for docs in retrieved.values():
            for doc in docs:
                score = doc.get("_score", 0.0)
                max_score = max(max_score, score)

        logger.info("Max retrieval KNN score: %.4f", max_score)

        context = {"question": query, "retrieved": retrieved}

        # 如果最高分小於門檻，直接判定為閒聊/非資料庫問題
        if max_score < RETRIEVAL_INTENT_THRESHOLD:
            logger.info(
                "Retrieval score %.4f < threshold %.2f, marking as CHITCHAT",
                max_score,
                RETRIEVAL_INTENT_THRESHOLD,
            )
            context["intent"] = "CHITCHAT"
            context["answer"] = CHITCHAT_RESPONSE
            context["generated_sql"] = ""

        return context
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
            formatter_skill
            | (lambda x: x if x.get("format_success") else synthesis_skill),
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
