"""Skill abstract base class."""

from abc import ABC, abstractmethod
from typing import Any

from langchain_core.runnables import Runnable


class Skill(Runnable[dict[str, Any], dict[str, Any]], ABC):
    """Base class for all agent skills.

    Subclasses must set ``name`` and ``description``, and implement ``execute``.
    Inheriting from Runnable allows skills to be used in LangChain LCEL chains.
    """

    name: str
    description: str

    @abstractmethod
    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the skill with the given context."""
        ...

    async def ainvoke(
        self,
        input_data: dict[str, Any],
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """LangChain compatible async invocation."""
        return await self.execute(input_data)

    def invoke(
        self,
        input_data: dict[str, Any],
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """LangChain compatible sync invocation (wraps async execute)."""
        import asyncio

        return asyncio.run(self.execute(input_data))
