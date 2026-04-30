import pytest
from fastapi.testclient import TestClient

from app.main import app, _items, _next_id


@pytest.fixture(autouse=True)
def reset_store():
    """Reset in-memory store before each test."""
    global _next_id
    _items.clear()
    import app.main as m
    m._next_id = 1
    yield
    _items.clear()
    m._next_id = 1


@pytest.fixture
def client():
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI"}


def test_list_items_empty(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item(client):
    response = client.post("/items", json={"name": "Widget", "description": "A widget"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Widget"
    assert data["description"] == "A widget"


def test_get_item(client):
    client.post("/items", json={"name": "Gadget"})
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Gadget"


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404


def test_list_items_after_create(client):
    client.post("/items", json={"name": "A"})
    client.post("/items", json={"name": "B"})
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_item(client):
    client.post("/items", json={"name": "Temp"})
    response = client.delete("/items/1")
    assert response.status_code == 204
    assert client.get("/items/1").status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
