# app/rbac/sql_parser.py

import sqlglot

def parse_sql(sql: str):
    try:
        return sqlglot.parse_one(sql)
    except Exception as e:
        raise ValueError(f"Invalid SQL: {e}")