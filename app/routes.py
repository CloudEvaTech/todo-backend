from fastapi import APIRouter, HTTPException
from app.models import Item
from app.storage import items


router = APIRouter()

# Create Functionality (POST Method)
@router.post("/items/")
def create_item(item : Item):
    if item.id in items:
        # Forbidden Status Code
        raise HTTPException(status_code = 403, detail = "Item Already Exists")
    items[item.id] = item
    return items

# Read Functionality (GET Method)
@router.get("/items/")
def get_all_items():
    return {item_id: item.dict() for item_id, item in items.items()}