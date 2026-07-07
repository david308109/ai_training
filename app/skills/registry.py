"""Skill registry for dynamic lookup and invocation."""

from app.skills.base import Skill


class SkillRegistry:
    """Maps skill names to skill instances."""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        """Register a skill instance."""
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill:
        """Retrieve a skill by name.

        Raises
        ------
        KeyError
            If the skill name is not registered.
        """
        if name not in self._skills:
            available = ", ".join(self._skills.keys()) or "(none)"
            raise KeyError(f"Skill '{name}' not found. Available skills: {available}")
        return self._skills[name]

    def list_skills(self) -> list[dict[str, str]]:
        """Return a list of registered skill summaries."""
        return [
            {"name": s.name, "description": s.description}
            for s in self._skills.values()
        ]
