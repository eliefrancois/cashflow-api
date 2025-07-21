from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Cashflow API", version="1.0.0")

class Item(BaseModel):
    id: Optional[str] = None
    name: str
    amount: float
    category: str

items_db: List[Item] = []

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return items_db

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    item.id = str(uuid.uuid4())
    items_db.append(item)
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Item {deleted_item.name} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")