schema_fetch_all_users = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "premium": {"type": "boolean"},
        },
    },
}

schema_fetch_product_headers = {
    "type": "object",
    "required": ["content-disposition", "content-type", "content-length"],
    "properties": {
        "content-disposition": {
            "type": "string",
            "pattern": "^attachment; filename=[0-9a-f]{8}\\.zip$",
        },
        "content-type": {"type": "string", "pattern": "^application/x-zip-compressed$"},
        "content-length": {"type": "string", "pattern": "[0-9]*"},
        "last-modified": {"type": "string"},
        "etag": {"type": "string"},
    },
}

schema_fetch_gallery = {
    "type": "array",
    "items": {"type": "string", "pattern": "^(rs|c)_([1-9]|1[0-2])\\.(jpg|jpeg)"},
}

schema_fetch_gallery_headers = {
    "type": "object",
    "required": ["content-disposition", "content-type", "content-length"],
    "properties": {
        "content-disposition": {
            "type": "string",
            "pattern": "^attachment; filename=gallery\\.zip$",
        },
        "content-type": {"type": "string", "pattern": "^application/x-zip-compressed$"},
        "content-length": {"type": "string", "pattern": "[0-9]*"},
        "last-modified": {"type": "string"},
        "etag": {"type": "string"},
    },
}
