# app/llm/gemini_client.py
from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_sql_gemini(user_query, schema):
    prompt = f"You are a SQL generator.\n\nSchema:\n{schema}\n\nUser Query:\n{user_query}\n\nReturn ONLY SQL query."

    # Updated call for google-genai 2.0+
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt  # or "gemini-1.5-pro"
    )
    return response.text.strip()
