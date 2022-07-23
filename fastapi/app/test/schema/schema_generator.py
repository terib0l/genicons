schema_generate_user = {
    "type": "object",
    "required": ["user_id"],
    "additionalProperties": False,
    "properties": {
        "user_id": {
            "type": "number",
        }
    },
}

schema_generate_product = {
    "type": "object",
    "required": ["product_id"],
    "additionalProperties": False,
    "properties": {
        "product_id": {
            "type": "string",
            "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        }
    },
}
