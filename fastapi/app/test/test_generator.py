import pytest

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator

from main import app
from app.test.schema.schema_generator import test_generate_product_schema

client = TestClient(app)


@pytest.mark.generate_product
@pytest.mark.parametrize("some_data_setup", [1], indirect=True)
def test_generate_product(random_image):
    response = client.post(
        "/product/generate",
        files={"img": (random_image.name, open(random_image.path, "rb"), "image/jpeg")},
    )

    assert response.status_code == 200
    assert Draft7Validator(test_generate_product_schema).is_valid(response.json())
