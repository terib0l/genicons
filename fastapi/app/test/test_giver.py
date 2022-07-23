import io
import random
import pytest

from fastapi import status
from httpx import AsyncClient
from zipfile import ZipFile
from jsonschema import Draft7Validator

from main import app
from app.test.schema.schema_giver import (
    schema_fetch_all_users,
    schema_fetch_product_headers,
    schema_fetch_gallery,
    schema_fetch_gallery_headers,
)

client = AsyncClient(app=app, base_url="http://127.0.0.1:8888/")


@pytest.mark.fetch_all_users
@pytest.mark.asyncio
async def test_fetch_all_users():
    response = await client.get(url="all/users/fetch")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_fetch_all_users).is_valid(data)


@pytest.mark.fetch_product
@pytest.mark.asyncio
async def test_download_products():
    product_id = None
    response = await client.get(f"product/fetch?product_id={product_id}")

    assert response.status_code == status.HTTP_200_OK

    with ZipFile(io.BytesIO(response._content), "r") as zipfile:
        name_list = zipfile.namelist()
        assert f"rs_{product_id}.jpg" == name_list[0]
        assert f"c_{product_id}.jpg" == name_list[1]

    assert Draft7Validator(schema_fetch_product_headers).is_valid(
        dict(response.headers)
    )


@pytest.mark.fetch_gallery
@pytest.mark.asyncio
async def test_get_gallery():
    num = random.randint(1, 10)
    response = await client.get(f"gallery/fetch?gallery_num={num}")

    assert response.status_code == status.HTTP_200_OK

    with ZipFile(io.BytesIO(response._content), "r") as zipfile:
        name_list = zipfile.namelist()
        assert Draft7Validator(schema_fetch_gallery).is_valid(name_list)

    assert Draft7Validator(schema_fetch_gallery_headers).is_valid(
        dict(response.headers)
    )
