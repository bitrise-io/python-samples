from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FastAPI Sample", version="1.0.0")

# In-memory store
_items: dict[int, dict] = {}
_next_id = 1


class ItemCreate(BaseModel):
    name: str
    description: str = ""


class Item(BaseModel):
    id: int
    name: str
    description: str


@app.get("/")
def root() -> dict:
    return {"message": "Hello from FastAPI"}


@app.get("/items", response_model=list[Item])
def list_items() -> list[dict]:
    return list(_items.values())


@app.post("/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate) -> dict:
    global _next_id
    item = {"id": _next_id, "name": payload.name, "description": payload.description}
    _items[_next_id] = item
    _next_id += 1
    return item


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> dict:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return _items[item_id]


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
