from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_generate_product():
    response = client.post("/product/generate")
    data = response.json()

    assert response.status_code == 200

def test_generate_in_case_of_products_have_made():
    response = client.get("/product/generate/status/{uid}")
    data = response.json()

    assert response.status_code == 200

def test_generate_in_case_of_products_not_made_yet():
    response = client.get("/product/generate/status/{uid}")
    data = response.json()

    assert response.status_code == 204
