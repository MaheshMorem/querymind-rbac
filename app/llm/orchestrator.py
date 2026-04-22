# app/llm/orchestrator.py
from app.config import MODE, PROVIDER
from .openai_client import generate_sql_openai
from .gemini_client import generate_sql_gemini
import asyncio


async def run_parallel(user_query, schema):
    loop = asyncio.get_event_loop()

    openai_task = loop.run_in_executor(None, generate_sql_openai, user_query, schema)
    gemini_task = loop.run_in_executor(None, generate_sql_gemini, user_query, schema)

    openai_sql, gemini_sql = await asyncio.gather(openai_task, gemini_task)

    return {"openai": openai_sql, "gemini": gemini_sql}


async def generate_sql(user_query, schema):
    if MODE == "parallel":
        return await run_parallel(user_query, schema)

    if PROVIDER == "openai":
        return {"openai": generate_sql_openai(user_query, schema)}

    if PROVIDER == "gemini":
        return {"gemini": generate_sql_gemini(user_query, schema)}

    raise Exception("Invalid provider")
