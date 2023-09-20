from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI()

class Item(BaseModel):
    _id: str
    _owner: str
    title: str
    email: str
    password: str

@app.post("/create-item/")
async def create_item(item: Item):
    # For demonstration purposes, we'll simulate a delay
    await asyncio.sleep(2)  # Simulate a 2-second delay

    return {"message": "Item created successfully", "data": item.model_dump()}
