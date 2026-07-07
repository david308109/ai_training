from langchain_openai import ChatOpenAI
from app.config import settings

llm = ChatOpenAI(
    model=settings.llm_model,
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_base_url,
    temperature=settings.llm_temperature,
)

resp = llm.invoke("Hello, can you test if OpenRouter works?")
print(resp)
