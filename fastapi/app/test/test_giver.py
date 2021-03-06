import io
import pytest
from fastapi import status
from zipfile import ZipFile
from jsonschema import Draft7Validator

from app.test.schema.schema_giver import (
    schema_fetch_product_ids,
    schema_fetch_product_origins,
    schema_fetch_product_origins_headers,
    schema_fetch_product,
    schema_fetch_product_headers,
    schema_fetch_gallery,
    schema_fetch_gallery_headers,
)


@pytest.mark.fetch_product_ids
@pytest.mark.asyncio
async def test_fetch_product_ids(async_client, token_header):
    response = await async_client.get(
        url="fetch/product/ids",
        headers=token_header,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Draft7Validator(schema_fetch_product_ids).is_valid(data)


@pytest.mark.fetch_product_origins
@pytest.mark.asyncio
async def test_fetch_product_origins(async_client, token_header):
    response = await async_client.get(
        "fetch/product/origins",
        headers=token_header,
    )

    assert response.status_code == status.HTTP_200_OK

    with ZipFile(io.BytesIO(response._content), "r") as zipfile:
        name_list = zipfile.namelist()
        assert Draft7Validator(schema_fetch_product_origins).is_valid(name_list)

    assert Draft7Validator(schema_fetch_product_origins_headers).is_valid(
        dict(response.headers)
    )


@pytest.mark.fetch_product
@pytest.mark.asyncio
async def test_fetch_product(async_client, token_header, product_id):
    response = await async_client.get(
        f"fetch/product?product_id={product_id}",
        headers=token_header,
    )

    assert response.status_code == status.HTTP_200_OK

    with ZipFile(io.BytesIO(response._content), "r") as zipfile:
        name_list = zipfile.namelist()
        assert Draft7Validator(schema_fetch_product).is_valid(name_list)

    assert Draft7Validator(schema_fetch_product_headers).is_valid(
        dict(response.headers)
    )


@pytest.mark.fetch_gallery
@pytest.mark.asyncio
async def test_fetch_gallery(async_client):
    gallery_num = 3

    response = await async_client.get(f"fetch/gallery?gallery_num={gallery_num}")

    assert response.status_code == status.HTTP_200_OK

    with ZipFile(io.BytesIO(response._content), "r") as zipfile:
        name_list = zipfile.namelist()
        assert Draft7Validator(schema_fetch_gallery).is_valid(name_list)

    assert Draft7Validator(schema_fetch_gallery_headers).is_valid(
        dict(response.headers)
    )
