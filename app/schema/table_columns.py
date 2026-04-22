TABLE_COLUMNS = {
    "users": {"id", "email", "role"},
    "vendors": {"id", "name"},
    "products": {"id", "name", "price", "cost_price", "vendor_id"},
    "orders": {"id", "user_id", "total_amount", "status"},
    "order_items": {"id", "order_id", "product_id", "quantity", "price"},
    "payments": {"id", "order_id", "amount", "method", "card_last4", "status"},
}
