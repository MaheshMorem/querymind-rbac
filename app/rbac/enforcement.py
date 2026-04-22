# app/rbac/enforcement.py

from app.rbac.validator import validate_policy
from .policy_loader import load_policy
from .sql_rewriter import rewrite_sql

policy = load_policy()
validate_policy(policy)


def enforce_rbac(sql: str, user_context: dict):
    return rewrite_sql(sql, policy, user_context)


# sql = "SELECT * FROM orders"
# sql = "SELECT * FROM users"
sql = "SELECT * FROM orders"

user = {"user_id": "123", "role": "customer"}

# print(enforce_rbac(sql, user))

if __name__ == "__main__":
    sql = "SELECT * FROM orders"
    user = {"role": "customer", "user_id": "123"}

    # print(enforce_rbac(sql, user))
