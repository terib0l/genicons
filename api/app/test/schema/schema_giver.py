test_read_all_users_in_case_of_some_datas_schema = {
    "type": "object",
    "patternProperties": {
        "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$": {
            "type": "string",
            "pattern": "[0-9a-zA-Z]*\\.(jpg|jpeg)"
        }
    }
}

test_get_gallery_in_case_of_some_datas_in_db_data_schema = {
    "type": "array",
    "items": {
        "type": "string",
        "pattern": "^(rs|c)_([1-9]|1[0-2])\\.(jpg|jpeg)"
    }
}

test_get_gallery_in_case_of_some_datas_in_db_headers_schema = {
    "type": "object",
    "required": ["content-disposition", "content-type", "content-length"],
    "properties": {
        "content-disposition": {
            "type": "string",
            "pattern": "^attachment; filename=gallery\\.zip$"
        },
        "content-type": {
            "type": "string",
            "pattern": "^application/x-zip-compressed$"
        },
        "content-length": {
            "type": "string",
            "pattern": "[0-9]*"
        },
        "last-modified": {
            "type": "string"
        },
        "etag": {
            "type": "string"
        }
    }
}

test_download_products_in_case_of_products_have_made_headers_schema = {
    "type": "object",
    "required": ["content-disposition", "content-type", "content-length"],
    "properties": {
        "content-disposition": {
            "type": "string",
            "pattern": "^attachment; filename=[0-9a-f]{8}\\.zip$"
        },
        "content-type": {
            "type": "string",
            "pattern": "^application/x-zip-compressed$"
        },
        "content-length": {
            "type": "string",
            "pattern": "[0-9]*"
        },
        "last-modified": {
            "type": "string"
        },
        "etag": {
            "type": "string"
        }
    }
}
