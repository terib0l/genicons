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

test_generate_in_case_of_products_have_made_schema = {
        "type": "object",
        "required": ["status", "url"],
        "additionalProperties": False,
        "properties": {
            "status": {
                "type": "string",
                "pattern": "^completed$"
            },
            "url": {
                "type": "string",
                "pattern": "^https?://testserver/product/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/download$"
            }
        }
}

test_generate_in_case_of_products_not_made_yet_schema = {
        "type": "object",
        "required": ["status", "progress"],
        "additionalProperties": False,
        "properties": {
            "status": {
                "type": "string",
                "pattern": "^in_progress$"
            },
            "progress": {
                "type": "number"
            }
        }
}
