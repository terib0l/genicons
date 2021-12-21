import os
import random

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator

from main import app
from test.schema.schema_giver import *

client = TestClient(app)

def test_read_all_users_in_case_of_empty():
    response = client.get("/users/all/read")

    assert response.status_code == 200
    assert response.json() == {}

def test_read_all_users_in_case_of_some_datas():
    loop = random.randint(1, 3)
    for _ in range(loop):
        img_name = random.choice(os.listdir("./img/"))
        img_path = "./img/" + img_name

        client.post(
                "/product/generate",
                files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
        )

    response = client.get("/users/all/read")

    assert response.status_code == 200
    assert Draft7Validator(test_read_all_users_in_case_of_some_datas_schema).is_valid(response.json())

def test_get_gallery_in_case_of_empty():
    num = random.randint(1, 12)

    response = client.get(f"/gallery/{num}/download")

    assert response.status_code == 204
    assert response.json() == "No Content"

def test_get_gallery_in_case_of_some_datas_in_db():
    loop = random.randint(1, 12)
    for _ in range(loop):
        img_name = random.choice(os.listdir("./img/"))
        img_path = "./img/" + img_name

        client.post(
                "/product/generate",
                files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
        )


    num = random.randint(1, loop)
    response = client.get(f"/gallery/{num}/download")

    assert response.status_code == 200
    assert Draft7Validator(test_get_gallery_in_case_of_some_datas_in_db_schema).is_valid(response.json())

def test_download_products_in_case_of_products_not_made_yet():
    # First, generate product
    img_name = random.choice(os.listdir("./img/"))
    img_path = "./img/" + img_name

    response = client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
    )

    # Second, request url for download product
    uid = response.json()["uid"]
    response = client.get(f"/product/{uid}/download")

    assert response.status_code == 204
    assert response.json() == "Product is empty"

def test_download_products_in_case_of_products_have_made():
    # First, generate product
    img_name = random.choice(os.listdir("./img/"))
    img_path = "./img/" + img_name

    response = client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
    )

    # Second, wait for appropriate time

    # Third, request url for download product
    uid = response.json()["uid"]
    response = client.get(f"/product/{uid}/download")

    assert response.status_code == 200
    assert Draft7Validator(test_download_products_in_case_of_products_have_made_schema).is_valid(response.json())
