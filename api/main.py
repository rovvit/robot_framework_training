import os
from fastapi import FastAPI, Request, HTTPException, Query
from tortoise.contrib.fastapi import register_tortoise
from models import Item
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/test")
async def test_endpoint():
    return "Test"

@app.post("/item")
async def create_item(request: Request):
    data = await request.json()
    logger.info(f"Received data: {data}")

    if "name" not in data:
        raise HTTPException(status_code=400, detail="'name' field is required")

    existing = await Item.get_or_none(name=data["name"])
    if existing:
        raise HTTPException(status_code=400, detail=f'''Item with name '{data["name"]}' already exists''')

    item = await Item.create(
        name=data.get("name"),
        comment=data.get("comment"),
        category=data.get("category"),
    )

    return {
        "id": item.id,
        "name": item.name,
        "comment": item.comment,
        "category": item.category,
        "created": str(item.created),
    }


@app.get("/items")
async def get_items():
    query = Item.all()
    items = await query.limit(10).values
    count = await query.count()
    return  {
        "count": count,
        "data": items
    }


@app.get("/item")
async def get_item(
    id: int | None = Query(None),
    name: str | None = Query(None)
):
    query = Item.all()

    if id is not None:
        query = query.filter(id=id)
    if name is not None:
        query = query.filter(name__icontains=name)

    results = await query.values()

    if not results:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "count": len(results),
        "data": results
    }


@app.delete("/item/{item_id}")
async def delete_item(item_id: int):
    deleted_count = await Item.filter(id=item_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}
