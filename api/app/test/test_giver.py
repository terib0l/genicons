import io
import os
import uuid
import random

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator
from zipfile import ZipFile
from pathlib import Path

from main import app
from db.db_init import Base, ENGINE
from test.schema.schema_giver import *

client = TestClient(app)

current_path = Path(__file__).resolve().parent

def test_read_all_users_in_case_of_empty():
    # Initialization DB for make DB empty
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)

    # Request users information
    response = client.get("/users/all/read")

    assert response.status_code == 200
    assert response.json() == {}

def test_read_all_users_in_case_of_some_datas():
    # Make some datas
    loop = random.randint(1, 3)
    for _ in range(loop):
        img_name = random.choice(os.listdir(str(Path(current_path, 'img/'))))
        img_path = str(Path(current_path, "img/", img_name))

        client.post(
                "/product/generate",
                files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
        )

    # Request users information
    response = client.get("/users/all/read")

    assert response.status_code == 200
    assert Draft7Validator(test_read_all_users_in_case_of_some_datas_schema).is_valid(response.json())

def test_get_gallery_in_case_of_empty():
    # Initialization DB for make DB empty
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)

    num = random.randint(1, 12)

    response = client.get(f"/gallery/{num}/download")

    assert response.status_code == 204
    assert response.json() == "No Content"

def test_get_gallery_in_case_of_some_datas_in_db():
    # Make some datas
    loop = random.randint(1, 12)
    for _ in range(loop):
        img_name = random.choice(os.listdir(str(Path(current_path, 'img/'))))
        img_path = str(Path(current_path, "img/", img_name))

        client.post(
                "/product/generate",
                files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
        )


    num = random.randint(1, loop)
    response = client.get(f"/gallery/{num}/download")

    assert response.status_code == 200

    with ZipFile(io.BytesIO(response._content), 'r') as zipfile:
        name_list = zipfile.namelist()
        assert Draft7Validator(test_get_gallery_in_case_of_some_datas_in_db_data_schema).is_valid(name_list)

    assert Draft7Validator(test_get_gallery_in_case_of_some_datas_in_db_headers_schema).is_valid(dict(response.headers))

def test_download_products_in_case_of_products_not_made_yet():
    # Initialization DB for make DB empty
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)

    # Request url for download product
    uid = uuid.uuid4()
    response = client.get(f"/product/{uid}/download")

    assert response.status_code == 204
    assert response.json() == "Product is empty"

def test_download_products_in_case_of_products_have_made():
    # First, generate product
    img_name = random.choice(os.listdir(str(Path(current_path, 'img/'))))
    img_path = str(Path(current_path, "img/", img_name))

    response = client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
    )

    # Second, request url for download product
    data = response.json()
    uid = data["uid"]
    response = client.get(f"/product/{uid}/download")

    assert response.status_code == 200

    with ZipFile(io.BytesIO(response._content), 'r') as zipfile:
        name_list = zipfile.namelist()
        assert f"rs_{uid[:8]}.jpg" == name_list[0]
        assert f"c_{uid[:8]}.jpg" == name_list[1]

    assert Draft7Validator(test_download_products_in_case_of_products_have_made_headers_schema).is_valid(dict(response.headers))
