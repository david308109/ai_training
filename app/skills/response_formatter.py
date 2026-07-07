"""Response Formatter skill: fills templates locally without AI."""

import logging
from typing import Any

from app.skills.base import Skill

logger = logging.getLogger(__name__)


class ResponseFormatterSkill(Skill):
    """Attempt to format a natural language answer locally using Python .format()."""

    name = "response_formatter"
    description = "Format answers locally using templates and SQL results"

    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Try to format the answer.

        Expected context keys
        ---------------------
        - ``response_template`` (str)
        - ``query_result`` (dict): from ``database.execute_query()``

        Returns
        -------
        dict with ``answer`` (str) and ``format_success`` (bool)
        """
        template = context.get("response_template")
        query_result = context.get("query_result", {})

        if not template:
            return {"format_success": False, "error": "No template provided"}

        rows = query_result.get("rows", [])
        cols = query_result.get("columns", [])

        if not rows:
            return {
                "answer": "在目前的資料庫中查無符合條件的資料。",
                "format_success": True,
            }

        try:
            # Map the first row to a dictionary for formatting
            data_map = dict(zip(cols, rows[0]))
            # Format the template
            clean_template = template.replace("{{", "{").replace("}}", "}")

            answer = clean_template.format(**data_map)
            logger.info("Successfully formatted answer locally: %s", answer)
            return {**context, "answer": answer, "format_success": True}

        except (KeyError, IndexError, ValueError) as e:
            logger.warning("Local formatting failed, falling back to AI: %s", e)
            return {**context, "format_success": False, "error": str(e)}
