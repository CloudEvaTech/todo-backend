from fastapi import APIRouter, HTTPException
from app.models import Item
from app.storage import items

router = APIRouter()

# Create Operation
@router.post("/items/")
def create_item(item : Item):
    if item.id in items:
        # Forbidden Status Code
        raise HTTPException(status_code = 409, detail = "Item Already Exists")
    
    items[item.id] = item
    return items

# Read Operation
@router.get("/items/")
def get_all_items():
    return items

# Update Operation
@router.put("/items/{item_id}")
def update_items(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code = 404, detail = "Item Does Not Exists")
    if item.id in items:
        raise HTTPException(status_code = 409, detail = "Item Already Exist")

    items[item_id] = item
    return items

# Delete Operation
@router.delete("/items/{item_id}")
def delete_items(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code = 404, detail = "Item Does Not Exists")

    del items[item_id]
    return items