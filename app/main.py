"""FastAPI application — POST /query endpoint."""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.orchestrator import process_query
from app.db.database import init_db
from app.skills.answer_synthesis import AnswerSynthesisSkill
from app.skills.registry import SkillRegistry
from app.skills.response_formatter import ResponseFormatterSkill
from app.skills.sql_generation import SQLGenerationSkill

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Global registry
registry = SkillRegistry()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB + register skills."""
    logger.info("Initialising database...")
    init_db()

    logger.info("Registering skills...")
    registry.register(SQLGenerationSkill())
    registry.register(AnswerSynthesisSkill())
    registry.register(ResponseFormatterSkill())
    logger.info("Skills registered: %s", [s["name"] for s in registry.list_skills()])

    yield  # app runs here

    logger.info("Shutting down.")


app = FastAPI(
    title="Data Agent — Text-to-SQL",
    description="Natural language → SQL → Answer for banking data",
    version="0.1.0",
    lifespan=lifespan,
)


# --- Request / Response models ---

class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    generated_sql: str
    query_result: dict | None = None
    error: str | None = None


# --- Endpoints ---

@app.post("/query", response_model=QueryResponse)
async def handle_query(req: QueryRequest):
    """Accept a natural language question and return an answer with generated SQL."""
    logger.info("Received query: %s", req.query)
    result = await process_query(req.query, registry)
    return QueryResponse(**result)


@app.get("/health")
async def health():
    print("Health check")
    return {"status": "ok"}


if __name__ == "__main__":
    # This allows running the app directly via `python app/main.py`
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
