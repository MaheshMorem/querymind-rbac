import sqlglot
from sqlglot import exp
from app.schema.relationships import RELATIONSHIPS
from app.schema.table_columns import TABLE_COLUMNS

# =========================================================
# 🔹 BASIC HELPERS
# =========================================================


def get_tables(expression):
    return [t.name for t in expression.find_all(exp.Table)]


def table_exists(expression, table_name):
    # 🔥 FIXED: reliable detection
    for t in expression.find_all(exp.Table):
        if t.name == table_name:
            return True
    return False


def get_table_alias_map(expression):
    alias_map = {}
    for t in expression.find_all(exp.Table):
        alias_map[t.name] = t.alias or t.name
    return alias_map


# =========================================================
# 🔹 FILTER BUILDER
# =========================================================


def build_condition(table_ref, column, operator, value):
    col = exp.Column(
        this=exp.Identifier(this=column),
        table=exp.Identifier(this=table_ref),
    )

    if isinstance(value, str) and "," in value:
        values = [exp.Literal.string(v.strip()) for v in value.split(",")]
        return exp.In(this=col, expressions=values)

    val = exp.Literal.string(value)

    return {
        "=": exp.EQ,
        "!=": exp.NEQ,
        ">": exp.GT,
        "<": exp.LT,
        ">=": exp.GTE,
        "<=": exp.LTE,
    }[operator](this=col, expression=val)


# =========================================================
# 🔹 APPLY FILTER
# =========================================================


def apply_row_filter(expression, table, rf, user_context):
    column = rf["column"]
    operator = rf.get("operator", "=")

    value = user_context.get(rf.get("type")) if "type" in rf else rf.get("value")

    if value is None:
        return expression

    # 🔥 HARD VALIDATION (no silent skip)
    if column not in TABLE_COLUMNS.get(table, set()):
        raise Exception(f"Invalid column {column} for table {table}")

    alias_map = get_table_alias_map(expression)
    table_ref = alias_map.get(table, table)

    condition = build_condition(table_ref, column, operator, value)

    print(f"✅ Applying filter: {table}.{column} = {value}")

    where = expression.args.get("where")

    if where:
        expression.set(
            "where",
            exp.Where(this=exp.And(this=where.this, expression=condition)),
        )
    else:
        expression.set("where", exp.Where(this=condition))

    return expression


# =========================================================
# 🔹 JOIN INJECTION (MULTI-KEY SUPPORT)
# =========================================================


def inject_join(expression, from_table, to_table):
    if table_exists(expression, to_table):
        return expression

    relations = RELATIONSHIPS.get(from_table, {}).get(to_table)

    if not relations:
        raise Exception(f"No relationship between {from_table} and {to_table}")

    if not isinstance(relations, list):
        relations = [relations]

    alias_map = get_table_alias_map(expression)
    from_ref = alias_map.get(from_table, from_table)
    to_ref = to_table  # new join

    condition = None

    for from_col, to_col in relations:
        eq = exp.EQ(
            this=exp.Column(
                this=exp.Identifier(this=from_col),
                table=exp.Identifier(this=from_ref),
            ),
            expression=exp.Column(
                this=exp.Identifier(this=to_col),
                table=exp.Identifier(this=to_ref),
            ),
        )
        condition = eq if condition is None else exp.And(this=condition, expression=eq)

    join = exp.Join(
        this=exp.Table(this=exp.Identifier(this=to_table)),
        on=condition,
    )

    expression.set("joins", expression.args.get("joins", []) + [join])

    print(f"🔗 Injected JOIN: {from_table} → {to_table}")

    return expression


# =========================================================
# 🔹 MAIN REWRITE FUNCTION
# =========================================================


def rewrite_sql(sql, policy, user_context):
    if ";" in sql.strip().rstrip(";"):
        raise Exception("Multiple statements not allowed")

    expression = sqlglot.parse_one(sql)

    role = user_context["role"]
    role_policy = policy.get(role, {})
    tables_policy = role_policy.get("tables", {})

    tables = set(get_tables(expression))

    for table in tables:

        table_policy = tables_policy.get(table)

        if not table_policy:
            if "*" in tables_policy:
                table_policy = tables_policy["*"]
            else:
                raise Exception(f"Access denied to {table}")

        if table_policy.get("allow") is False:
            raise Exception(f"Blocked table: {table}")

        # =====================================================
        # 🔥 VIA LOGIC
        # =====================================================
        if "via" in table_policy:
            via_tables = table_policy["via"]
            if isinstance(via_tables, str):
                via_tables = [via_tables]

            current = table

            for vt in via_tables:
                expression = inject_join(expression, current, vt)
                current = vt

            # Apply filters on LAST table (anchor)
            target_policy = tables_policy.get(current)

            if target_policy:
                for rf in target_policy.get("row_filters", []):
                    expression = apply_row_filter(expression, current, rf, user_context)

        # =====================================================
        # 🔥 DIRECT FILTER
        # =====================================================
        else:
            for rf in table_policy.get("row_filters", []):
                expression = apply_row_filter(expression, table, rf, user_context)

    # =====================================================
    # FINAL
    # =====================================================

    if not expression.args.get("limit"):
        expression.set("limit", exp.Limit(expression=exp.Literal.number(100)))

    return expression.sql()
