import os
import time
import random

from fastapi.testclient import TestClient
from jsonschema import Draft7Validator

from main import app
from test.schema.schema_generator import *

client = TestClient(app)

def test_generate_product():
    img_name = random.choice(os.listdir("./img/"))
    img_path = "./img/" + img_name

    response = client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
    )

    assert response.status_code == 200
    assert Draft7Validator(test_generate_product_schema).is_valid(response.json())

def test_generate_in_case_of_products_not_made_yet():
    # First, generate product
    img_name = random.choice(os.listdir("./img/"))
    img_path = "./img/" + img_name
    img = {"img": (img_name, open(img_path, "rb"), "image/jpeg")}

    response = client.post("/product/generate", files=img)

    # Second, check generating status before completion
    uid = response.json()["uid"]
    response = client.get(f"/product/generate/status/{uid}")

    assert response.status_code == 204
    assert Draft7Validator(test_generate_in_case_of_products_not_made_yet_schema).is_valid(response.json())

def test_generate_in_case_of_products_have_made():
    # First, generate product
    img_name = random.choice(os.listdir("./img/"))
    img_path = "./img/" + img_name

    response = client.post(
            "/product/generate",
            files={"img": (img_name, open(img_path, "rb"), "image/jpeg")}
    )

    # Second, wait for appropriate time to make products
    time.sleep(10)

    # Third, check generating status after completion
    uid = response.json()["uid"]
    response = client.get(f"/product/generate/status/{uid}")

    assert response.status_code == 200
    assert Draft7Validator(test_generate_in_case_of_products_have_made_schema).is_valid(response.json())
