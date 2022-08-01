import pytest
from fastapi import status
from jsonschema import Draft7Validator

from app.test.schema.schema_generator import (
    schema_generate_user,
    schema_generate_product,
    schema_send_contact,
)


@pytest.mark.generate_user
@pytest.mark.asyncio
async def test_generate_user(async_client, random_user):
    response = await async_client.post(
        url="generate/user",
        data={
            "username": random_user["name"],
            "email": random_user["email"],
            "password": random_user["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_generate_user).is_valid(data)


@pytest.mark.generate_product
@pytest.mark.asyncio
async def test_generate_product(async_client, token_header, random_image):
    response = await async_client.post(
        url="generate/product",
        headers=token_header,
        files={"image": (random_image.name, random_image.img, "image/jpeg")},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_generate_product).is_valid(data)


@pytest.mark.send_contact
@pytest.mark.asyncio
async def test_send_contact(async_client, token_header, random_contents):
    response = await async_client.post(
        url="send/contact", headers=token_header, data={"contents": random_contents}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_send_contact).is_valid(data)
