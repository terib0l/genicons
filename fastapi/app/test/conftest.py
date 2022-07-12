import os
import random
import pytest
from pathlib import Path
from dataclasses import dataclass

from fastapi.testclient import TestClient

from main import app
from app.db.session import Base, ENGINE

current_path = Path(__file__).resolve().parent


@dataclass
class Image:
    name: str
    path: str


@pytest.fixture()
def random_image():
    name = random.choice(os.listdir(str(Path(current_path, "img/"))))
    path = str(Path(current_path, "img/", name))

    image = Image(name=name, path=path)

    return image


@pytest.fixture(autouse=True)
def db_empty():
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(bind=ENGINE, checkfirst=False)


@pytest.fixture()
def some_data_setup(request):
    client = TestClient(app)
    loop = random.randint(1, request.param)

    for _ in range(loop):
        img = random_image()

        response = client.post(
            "/product/generate",
            files={"img": (img.name, open(img.path, "rb"), "image/jpeg")},
        )

    return response
