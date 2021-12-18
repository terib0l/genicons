import random

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_all_users_in_case_of_empty():
    response = client.get("/users/all/read")
    data = response.json()

    assert response.status_code == 200
    assert data == {}

def test_read_all_users_in_case_of_some_datas():
    response = client.get("/users/all/read")
    data = response.json()

    assert response.status_code == 200

def test_get_gallery_in_case_of_empty():
    num = random.randint(1, 12)

    response = client.get(f"/gallery/{num}/download")
    data = response.json()

    assert response.status_code == 204

def test_get_gallery_in_case_of_some_datas_in_db():
    num = random.randint(1, 12)

    # Generate a few data

    response = client.get(f"/gallery/{num}/download")
    data = response.json()

    assert response.status_code == 200

def test_download_products():
    # Generate data

    response = client.get(f"/product/{uid}/download")
    data = response.json()

    assert response.status_code == 204
