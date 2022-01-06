from fastapi.testclient import TestClient
from uuid import uuid4
from jsonschema import Draft7Validator

from main import app
from test.schema.schema_giver import *
from test.schema.schema_generator import *

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Success!"

def test_generator_validator():
    uid = str(uuid4())
    data = {"uid": uid}
    assert Draft7Validator(test_generate_product_schema).is_valid(data)

def test_giver_validator():
    uid = str(uuid4())
    data = {uid: "test.jpg"}
    assert Draft7Validator(test_read_all_users_in_case_of_some_datas_schema).is_valid(data)
    assert Draft7Validator(test_get_gallery_in_case_of_some_datas_in_db_schema).is_valid(data)
    assert Draft7Validator(test_download_products_in_case_of_products_have_made_schema).is_valid(data)
