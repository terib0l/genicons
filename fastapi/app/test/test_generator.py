import os
import random
import pytest

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator
from pathlib import Path

from main import app
from app.test.schema.schema_generator import test_generate_product_schema

client = TestClient(app)

current_path = Path(__file__).resolve().parent


@pytest.mark.generate_product
def test_generate_product():
    img_name = random.choice(os.listdir(str(Path(current_path, "img/"))))
    img_path = str(Path(current_path, "img/", img_name))

    response = client.post(
        "/product/generate",
        files={"img": (img_name, open(img_path, "rb"), "image/jpeg")},
    )

    assert response.status_code == 200
    assert Draft7Validator(test_generate_product_schema).is_valid(response.json())
