# app/llm/openai_client.py
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_sql_openai(user_query, schema):
    prompt = f"""
    You are an expert MySQL SQL generator.

    Your task is to convert a natural language query into a correct and executable SQL query.

    =====================
    DATABASE SCHEMA:
    {schema}
    =====================

    USER QUERY:
    {user_query}

    =====================
    STRICT OUTPUT RULES:
    =====================

    - Return ONLY raw SQL
    - No markdown, no backticks, no explanation
    - Output must be directly executable MySQL
    - Do NOT use placeholders (?, $1, :param)
    - Always inline values
    - Do NOT generate multiple statements

    =====================
    QUERY RULES:
    =====================

    1. Use only tables and columns present in the schema
    2. If query involves multiple tables → use proper JOINs
    3. Prefer simple queries when possible
    4. Do NOT assume columns or tables not defined in schema
    5. Do NOT hallucinate relationships

    =====================
    GENERATE SQL NOW
    =====================
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    sql = response.choices[0].message.content.strip()

    # Remove markdown if model still adds it
    if sql.startswith("```"):
        sql = sql.split("```")[1]
        if sql.startswith("sql"):
            sql = sql[3:]

    return sql.strip().rstrip(";")
