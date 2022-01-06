test_generate_product_schema = {
        "type": "object",
        "required": ["uid"],
        "additionalProperties": False,
        "properties": {
            "uid": {
                "type": "string",
                "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
            }
        }
}
