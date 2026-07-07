"""Answer Synthesis skill: converts SQL results + question into natural language."""

import logging

from langchain_openai import ChatOpenAI

from app.config import settings
from app.skills.base import Skill

logger = logging.getLogger(__name__)

ANSWER_PROMPT = """\
You are a helpful banking data analyst. Given the user's original question and the SQL query results, provide a clear, concise, natural language answer.

=== USER QUESTION ===
{question}

=== SQL QUERY ===
{sql}

=== QUERY RESULTS ===
Columns: {columns}
Data:
{rows}

=== RULES ===
1. Answer in natural language. Be specific — include actual numbers and names from the data.
2. If the result set is empty, say that no matching records were found.
3. Format large numbers with commas for readability (e.g. 5,000,000).
4. Keep the answer concise but informative.
5. Do NOT mention SQL, databases, or technical details in your answer.

Answer:
"""

ERROR_PROMPT = """\
You are a helpful banking data analyst. The user asked a question but the system could not retrieve an answer due to an error.

=== USER QUESTION ===
{question}

=== ERROR ===
{error}

Please explain in friendly, non-technical language that we were unable to answer their question, and suggest they rephrase or try again.

Answer:
"""


class AnswerSynthesisSkill(Skill):
    """Convert SQL query results into a natural language answer."""

    name = "answer_synthesis"
    description = "Synthesise a natural language answer from SQL results"

    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            temperature=settings.llm_temperature,
        )

    async def execute(self, context: dict) -> dict:
        """Synthesise an answer.

        Expected context keys
        ---------------------
        - ``question`` (str)
        - ``generated_sql`` (str)
        - ``query_result`` (dict): from ``database.execute_query()``

        Returns
        -------
        dict with ``answer`` (str)
        """
        question = context.get("question", "")
        sql = context.get("generated_sql", "")
        query_result = context.get("query_result", {})

        # Handle error case
        if "error" in query_result:
            prompt = ERROR_PROMPT.format(
                question=question,
                error=query_result["error"],
            )
        else:
            columns = query_result.get("columns", [])
            rows = query_result.get("rows", [])

            if not rows:
                rows_text = "(no rows returned)"
            else:
                rows_text = "\n".join(str(dict(zip(columns, row))) for row in rows[:20])
                if len(rows) > 20:
                    rows_text += f"\n... and {len(rows) - 20} more rows"

            prompt = ANSWER_PROMPT.format(
                question=question,
                sql=sql,
                columns=", ".join(columns),
                rows=rows_text,
            )

        try:
            response = await self._llm.ainvoke(prompt)
            answer = response.content.strip()
            return {**context, "answer": answer}
        except Exception as exc:
            logger.error("Answer synthesis failed: %s", exc)
            return {**context, "answer": f"Unable to generate an answer: {exc}"}
