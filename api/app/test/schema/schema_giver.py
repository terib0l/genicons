test_read_all_users_in_case_of_some_datas_schema = {
        "type": "object",
        "patternProperties": {
            "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$": {
                "type": "string",
                "pattern": "[0-9a-zA-Z]*\\.(jpg|jpeg)"
            }
        }
}

test_get_gallery_in_case_of_some_datas_in_db_schema = {
}

test_download_products_in_case_of_products_have_made_schema = {
}
