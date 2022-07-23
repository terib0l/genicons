import pytest

from fastapi import status
from jsonschema import Draft7Validator
from httpx import AsyncClient

from main import app
from app.test.schema.schema_generator import (
    schema_generate_user,
    schema_generate_product,
)

client = AsyncClient(app=app, base_url="http://127.0.0.1:8888/")


@pytest.mark.generate_user
@pytest.mark.asyncio
async def test_generate_user(random_user):
    name = random_user["name"]
    email = random_user["email"]

    response = await client.post(url=f"user/generate/?name={name}&email={email}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_generate_user).is_valid(data)


@pytest.mark.generate_product
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id",
    [
        1,
    ],
)
async def test_generate_product(random_image, user_id):
    response = await client.post(
        url=f"product/generate?user_id={user_id}",
        files={"img": (random_image.name, open(random_image.path, "rb"), "image/jpeg")},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_generate_product).is_valid(data)
