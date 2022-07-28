schema_fetch_product_ids = {
    "type": "array",
    "items": {
        "type": "string",
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    },
}

schema_fetch_product_origins = {
    "type": "array",
    "items": {
        "type": "string",
        "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$\\.jpg$",
    },
}

schema_fetch_product_origins_headers = {
    "type": "object",
    "required": ["content-disposition", "content-type", "content-length"],
    "properties": {
        "content-disposition": {
            "type": "string",
            "pattern": "^attachment; filename=origins\\.zip$",
        },
        "content-type": {"type": "string", "pattern": "^application/x-zip-compressed$"},
        "content-length": {"type": "string", "pattern": "[0-9]*"},
        "last-modified": {"type": "string"},
        "etag": {"type": "string"},
    },
}

schema_fetch_product = {
    "type": "array",
    "items": {
        "type": "string",
        "pattern": "^(rs|c)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\.jpg$",
    },
}

schema_fetch_product_headers = {
    "type": "object",
    "required": ["content-disposition", "content-type", "content-length"],
    "properties": {
        "content-disposition": {
            "type": "string",
            "pattern": "^attachment; filename=[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\.zip$",
        },
        "content-type": {"type": "string", "pattern": "^application/x-zip-compressed$"},
        "content-length": {"type": "string", "pattern": "[0-9]*"},
        "last-modified": {"type": "string"},
        "etag": {"type": "string"},
    },
}

schema_fetch_gallery = {
    "type": "array",
    "items": {"type": "string", "pattern": "^random(\\d)+\\.jpg"},
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
