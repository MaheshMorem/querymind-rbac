ALLOWED_TABLES = {"users", "vendors", "products", "orders", "order_items", "payments"}


def validate_tables(tables):
    for table in tables:
        if table not in ALLOWED_TABLES:
            raise Exception(f"Unknown table: {table}")
