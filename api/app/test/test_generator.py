import os
import random

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator

from main import app
from test.schema.schema_generator import *

client = TestClient(app)

def test_generate_product():
    img_name = random.choice(os.listdir("./img/"))
    img_path = "./img/" + img_name

    response = client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
    )

    assert response.status_code == 200
    assert Draft7Validator(test_generate_product_schema).is_valid(response.json())
