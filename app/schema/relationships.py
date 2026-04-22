RELATIONSHIPS = {
    "orders": {"order_items": [("id", "order_id")]},
    "order_items": {"orders": [("order_id", "id")], "products": [("product_id", "id")]},
    "products": {
        "order_items": [("id", "product_id")],
        "vendors": [("vendor_id", "id")],
    },
    "payments": {"orders": [("order_id", "id")]},
    "users": {"orders": [("id", "user_id")]},
}
