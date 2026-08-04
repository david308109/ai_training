"""SQL Generation skill: uses LangChain + OpenRouter LLM to produce SQL from natural language."""

import logging
import re

from langchain_openai import ChatOpenAI

from app.config import settings
from app.db.schema_description import SCHEMA_DESCRIPTION
from app.skills.base import Skill

import json

logger = logging.getLogger(__name__)

CHITCHAT_RESPONSE = (
    "Hello! I'm the Banking Data Analysis Assistant, here to help answer questions about banking data.\n\n"
    "You can ask questions like:\n"
    "- How many customers are there?\n"
    "- What is the total deposit amount for each branch?\n"
    "- Which relationship manager oversees the most customers?\n\n"
    "What would you like to know about the banking data?"
)

SQL_GENERATION_PROMPT = """\
You are an expert SQL analyst for a banking database. Your job is to generate a structured response containing an executable SQLite SELECT query and a complexity classification.

=== DATABASE SCHEMA ===
{schema}

=== RELEVANT SQL TEMPLATES (for reference) ===
{sql_templates}

=== BUSINESS CONTEXT ===
{business_context}

=== RESPONSE FORMAT (Strict JSON) ===
You must return a JSON object with the following keys:
1. "sql": The executable SQLite query, OR null if the question is NOT related to banking data.
2. "complexity": Either "simple" or "complex".
   - "simple": Use this for basic lookups of a single value, date, or specific record (e.g., check balance, find branch).
   - "complex": Use this for analytical queries, top-N reports, group-by statistics, or multi-row summaries.
3. "response_template": (Only if simple) A natural language template for the answer. Use {{column_name}} for placeholders matching your SQL aliases.
   - Example: "Your current balance is {{total}} TWD." (where SQL is "SELECT sum(amount) as total FROM ...")
4. "thoughts": A brief explanation of your logic.
5. "rejected_reason": (Only if sql is null) A short explanation of why no SQL was generated.

=== RULES ===
1. **IMPORTANT — Intent Guard**: If the user's message is NOT a question about banking data (e.g., greetings like "hello", "how are you", chitchat, or topics unrelated to the database), you MUST return {{"sql": null, "complexity": null, "rejected_reason": "<reason>", "thoughts": "Not a database query."}}. Do NOT fabricate a SQL query for non-data questions.
2. Use only SELECT statements. Never use INSERT, UPDATE, DELETE, DROP, or ALTER.
3. Use the exact table and column names from the schema.
4. Use table aliases (e.g. d, c) ONLY for queries involving JOINS. For single-table queries, do NOT use table aliases or prefixes (e.g., use "SUM(amount)" instead of "SUM(d.amount)").
5. If the question is ambiguous, make a reasonable assumption.
6. Ensure the placeholders in "response_template" exactly match the column aliases in your "sql".
7. Prefer selecting specific columns over "SELECT *". Use "SELECT *" only when listing full records or when specifically asked for all details.
8. Use strict alias naming for consistency:
   - "avg_age" for average age.
   - "avg_deposit" for average deposit amount.
   - "total_deposits" for SUM(amount) of ALL bank deposits.
   - "total_deposit" for SUM(amount) when grouped (e.g., by customer, branch, region).
   - "total_customers" for total count of ALL customers.
   - "customer_count" for counts of customers per category (e.g., per RM, per branch).
   - "count", "total", "average" ONLY for deposit type breakdown reports.
9. Prefer LEFT JOIN over JOIN when counting items per category (e.g., customers per RM) to ensure zero counts are included.
10. Follow the style of the provided SQL templates exactly.
{question}

JSON Output:
"""


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM response, stripping markdown code blocks if present."""
    # Try to extract from ```json ... ``` block
    match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1).strip()
    else:
        # Fallback: look for the first '{' and last '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            content = text[start : end + 1]
        else:
            content = text.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse LLM JSON: %s. Raw text: %s", e, text)
        return {}


def _format_sql_templates(templates: list[dict]) -> str:
    """Format retrieved SQL templates into a string for the prompt."""
    if not templates:
        return "(no relevant templates found)"
    parts = []
    for i, t in enumerate(templates, 1):
        parts.append(f"{i}. {t.get('description', '')}\n   SQL: {t.get('sql', '')}")
    return "\n".join(parts)


def _format_business_context(contexts: list[dict]) -> str:
    """Format retrieved business context into a string for the prompt."""
    if not contexts:
        return "(no relevant context found)"
    parts = []
    for ctx in contexts:
        parts.append(f"- {ctx.get('topic', '')}: {ctx.get('content', '')}")
    return "\n".join(parts)


def _build_dynamic_schema(retrieved_schemas: list[dict]) -> str:
    """Build a dynamic schema string based on retrieved tables and fallback logic.

    Rules:
    1. If no tables or max score < 0.5, return the full SCHEMA_DESCRIPTION (Fallback).
    2. Always include 'Core Tables' (branches, customers, deposits).
    3. Include any other tables with score >= 0.5.
    """
    if not retrieved_schemas:
        logger.info("No schemas retrieved, falling back to full schema.")
        return SCHEMA_DESCRIPTION

    max_score = max((s.get("_score", 0) for s in retrieved_schemas), default=0)
    if max_score < 0.5:
        logger.info("Max schema score %.2f < 0.5, falling back to full schema.", max_score)
        return SCHEMA_DESCRIPTION

    core_tables = {"branches", "customers", "deposits"}
    selected_tables = {s["table_name"] for s in retrieved_schemas if s.get("_score", 0) >= 0.5}
    all_selected = core_tables.union(selected_tables)

    # Extract descriptions from SCHEMA_DESCRIPTION (the static full text)
    # or reconstruct from the indexed data.
    # For simplicity and reliability, we reconstruct from the indexed format
    # which mirrors the style AI likes.
    schema_parts = ["=== Banking Database Schema (Dynamic Selection) ==="]

    from app.db.schema_description import SCHEMA_DESCRIPTIONS_FOR_INDEX

    for schema_info in SCHEMA_DESCRIPTIONS_FOR_INDEX:
        if schema_info["table_name"] in all_selected:
            part = f"\nTABLE: {schema_info['table_name']}\n"
            part += f"  - Description: {schema_info['description']}\n"
            part += f"  - Columns: {schema_info['columns']}"
            schema_parts.append(part)

    # Always include common join paths for context
    schema_parts.append("\n=== Common Join Paths ===\n  deposits → customers          ON deposits.customer_id = customers.customer_id\n  customers → relationship_managers ON customers.rm_id = relationship_managers.rm_id\n  relationship_managers → branches  ON relationship_managers.branch_id = branches.branch_id")

    return "\n".join(schema_parts)


class SQLGenerationSkill(Skill):
    """Generate executable SQL from a user question + retrieved context."""

    name = "sql_generation"
    description = "Generate SQL and classify complexity using LLM with RAG context"

    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            temperature=settings.llm_temperature,
        )

    async def execute(self, context: dict) -> dict:
        """Generate SQL and metadata.

        Expected context keys
        ---------------------
        - ``question`` (str): user's natural language question
        - ``retrieved`` (dict): output from ``retriever.retrieve()``

        Returns
        -------
        dict with ``generated_sql``, ``complexity``, ``response_template``, or ``error``.
        """
        question = context.get("question", "")
        retrieved = context.get("retrieved", {})

        # If already marked as CHITCHAT by KNN score check in retrieval step, skip LLM call
        if context.get("intent") == "CHITCHAT":
            logger.info("Query already marked as CHITCHAT, skipping SQL generation LLM call.")
            return context

        sql_templates_text = _format_sql_templates(
            retrieved.get("sql_templates", [])
        )
        business_context_text = _format_business_context(
            retrieved.get("business_context", [])
        )

        dynamic_schema = _build_dynamic_schema(
            retrieved.get("schema_descriptions", [])
        )

        prompt = SQL_GENERATION_PROMPT.format(
            schema=dynamic_schema,
            sql_templates=sql_templates_text,
            business_context=business_context_text,
            question=question,
        )
        # print(f"Prompt: {prompt}")  # Debug: print the final prompt sent to LLM

        try:
            response = await self._llm.ainvoke(prompt)
            data = _extract_json(response.content)
            #print(f"LLM Response: {response.content}")  # Debug: print raw LLM response

            if not data:
                return {"error": "LLM failed to produce valid JSON"}

            # Intent Guard: LLM returned sql=null → not a database question
            if data.get("sql") is None:
                logger.info("Query rejected by intent guard: %s", data.get("rejected_reason"))
                return {
                    "intent": "CHITCHAT",
                    "answer": CHITCHAT_RESPONSE,
                    "generated_sql": "",
                    "thoughts": data.get("thoughts"),
                }

            return {
                "generated_sql": data["sql"],
                "complexity": data.get("complexity", "complex"),
                "response_template": data.get("response_template"),
                "thoughts": data.get("thoughts"),
            }
        except Exception as exc:
            logger.error("SQL generation failed: %s", exc)
            return {"error": f"SQL generation failed: {exc}"}
