from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio

import weatherService

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    print("Hello...")
    await asyncio.sleep(3)
    print("... world!")
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}

@app.get("/weather/current")
async def read_current_weather(latitude: float, longitude: float):
    return weatherService.get_current_weather(latitude=latitude, longitude=longitude)

@app.get("/weather/historical")
async def read_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    return weatherService.get_historical_weather(latitude=latitude, longitude=longitude, start_date=start_date, end_date=end_date)