import io
import uuid
import random
import pytest

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator
from zipfile import ZipFile

from main import app
from app.test.schema.schema_giver import (
    test_read_all_users_in_case_of_some_datas_schema,
    test_get_gallery_in_case_of_some_datas_in_db_data_schema,
    test_get_gallery_in_case_of_some_datas_in_db_headers_schema,
    test_download_products_in_case_of_products_have_made_headers_schema,
)

client = TestClient(app)


@pytest.mark.read_all_users
@pytest.mark.parametrize("some_data_setup", [3], indirect=True)
def test_read_all_users(some_data_setup):
    response = client.get("/users/all/read")

    assert response.status_code == 200
    assert Draft7Validator(test_read_all_users_in_case_of_some_datas_schema).is_valid(
        response.json()
    )


@pytest.mark.get_gallery_empty
def test_get_gallery_from_empty():
    num = random.randint(1, 12)

    response = client.get(f"/gallery/{num}/download")

    assert response.status_code == 204
    assert response.json() == "No Content"


@pytest.mark.get_gallery
@pytest.mark.parametrize("some_data_setup", [10], indirect=True)
def test_get_gallery(some_data_setup):
    num = random.randint(1, 10)
    response = client.get(f"/gallery/{num}/download")

    assert response.status_code == 200

    with ZipFile(io.BytesIO(response._content), "r") as zipfile:
        name_list = zipfile.namelist()
        assert Draft7Validator(
            test_get_gallery_in_case_of_some_datas_in_db_data_schema
        ).is_valid(name_list)

    assert Draft7Validator(
        test_get_gallery_in_case_of_some_datas_in_db_headers_schema
    ).is_valid(dict(response.headers))


@pytest.mark.download_products_empty
def test_download_products_from_empty():
    uid = uuid.uuid4()
    response = client.get(f"/product/{uid}/download")

    assert response.status_code == 204
    assert response.json() == "Product is empty"


@pytest.mark.download_products
@pytest.mark.parametrize("some_data_setup", [1], indirect=True)
def test_download_products(some_data_setup):
    data = some_data_setup.json()
    uid = data["uid"]
    response = client.get(f"/product/{uid}/download")

    assert response.status_code == 200

    with ZipFile(io.BytesIO(response._content), "r") as zipfile:
        name_list = zipfile.namelist()
        assert f"rs_{uid[:8]}.jpg" == name_list[0]
        assert f"c_{uid[:8]}.jpg" == name_list[1]

    assert Draft7Validator(
        test_download_products_in_case_of_products_have_made_headers_schema
    ).is_valid(dict(response.headers))
