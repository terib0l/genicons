import pytest
import random
from fastapi import status
from jsonschema import Draft7Validator

from app.test.schema.schema_generator import (
    schema_generate_user,
    schema_generate_product,
)


@pytest.mark.generate_user
@pytest.mark.asyncio
async def test_generate_user(async_client, random_user):
    name = random_user["name"]
    email = random_user["email"]

    response = await async_client.post(url=f"generate/user?name={name}&email={email}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_generate_user).is_valid(data)


@pytest.mark.generate_product
@pytest.mark.asyncio
async def test_generate_product(async_client, random_image):
    user_id = random.choice([1, 2, 3])
    response = await async_client.post(
        url=f"generate/product?user_id={user_id}",
        files={"img": (random_image.name, open(random_image.path, "rb"), "image/jpeg")},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_generate_product).is_valid(data)
