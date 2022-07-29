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
    "properties": {"product_id": {"type": "string", "format": "uuid"}},
}

schema_send_contact = {
    "type": "object",
    "required": ["username", "email"],
    "additionalProperties": False,
    "properties": {
        "username": {
            "type": "string",
        },
        "email": {"type": "string", "format": "email"},
    },
}
