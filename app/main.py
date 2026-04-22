# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.llm.orchestrator import generate_sql
from app.db.executor import execute_query
from app.rbac.enforcement import enforce_rbac

app = FastAPI()


# 🔥 Hardcoded schema (for now)
SCHEMA = """
users(id, email, role)
vendors(id, name)
products(id, name, price, cost_price, vendor_id)
orders(id, user_id, total_amount, status)
order_items(id, order_id, product_id, quantity, price)
payments(id, order_id, amount, method, card_last4, status)
"""


class QueryRequest(BaseModel):
    query: str
    user: dict


@app.post("/query")
async def run_query(req: QueryRequest):
    print("\n========================")
    print("USER QUERY:", req.query)
    print("USER CONTEXT:", req.user)

    # 🧠 Step 1 — LLM SQL generation
    sql_outputs = await generate_sql(req.query, SCHEMA)

    results = {}

    for model, sql in sql_outputs.items():
        print(f"\n🔹 MODEL: {model}")
        print("Generated SQL:", sql)

        try:
            # 🧠 Step 2 — RBAC enforcement
            safe_sql = enforce_rbac(sql, req.user)
            print("Rewritten SQL:", safe_sql)

            # 🧠 Step 3 — Execute
            data = execute_query(safe_sql)
            print("Result count:", len(data))

            results[model] = {"generated_sql": sql, "safe_sql": safe_sql, "data": data}

        except Exception as e:
            msg = str(e)

            if "RBAC violation" in msg:
                msg = (
                    "You are not allowed to access this data due to policy restrictions"
                )

            print("ERROR:", msg)
            results[model] = {"error": msg}

    return results
