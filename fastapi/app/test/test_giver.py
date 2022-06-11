import io
import os
import uuid
import random
import pytest

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator
from zipfile import ZipFile
from pathlib import Path

from main import app
from app.db.db_init import Base, ENGINE
from app.test.schema.schema_giver import (
    test_read_all_users_in_case_of_some_datas_schema,
    test_get_gallery_in_case_of_some_datas_in_db_data_schema,
    test_get_gallery_in_case_of_some_datas_in_db_headers_schema,
    test_download_products_in_case_of_products_have_made_headers_schema,
)

client = TestClient(app)

current_path = Path(__file__).resolve().parent


@pytest.mark.read_all_users
def test_read_all_users():
    # In case of Empty
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)

    response = client.get("/users/all/read")

    assert response.status_code == 200
    assert response.json() == {}

    # In case of Some Datas
    loop = random.randint(1, 3)
    for _ in range(loop):
        img_name = random.choice(os.listdir(str(Path(current_path, "img/"))))
        img_path = str(Path(current_path, "img/", img_name))

        client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")},
        )

    response = client.get("/users/all/read")

    assert response.status_code == 200
    assert Draft7Validator(test_read_all_users_in_case_of_some_datas_schema).is_valid(
        response.json()
    )


@pytest.mark.get_gallery
def test_get_gallery():
    # In case of Empty
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)

    num = random.randint(1, 12)

    response = client.get(f"/gallery/{num}/download")

    assert response.status_code == 204
    assert response.json() == "No Content"

    # In case of Some Datas
    loop = random.randint(1, 12)
    for _ in range(loop):
        img_name = random.choice(os.listdir(str(Path(current_path, "img/"))))
        img_path = str(Path(current_path, "img/", img_name))

        client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")},
        )

    num = random.randint(1, loop)
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


@pytest.mark.download_products
def test_download_products():
    # In case of Products Not Made Yet
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)

    uid = uuid.uuid4()
    response = client.get(f"/product/{uid}/download")

    assert response.status_code == 204
    assert response.json() == "Product is empty"

    # In case of Products Have Made
    img_name = random.choice(os.listdir(str(Path(current_path, "img/"))))
    img_path = str(Path(current_path, "img/", img_name))

    response = client.post(
        "/product/generate",
        files={"img": (img_name, open(img_path, "rb"), "image/jpeg")},
    )

    data = response.json()
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
