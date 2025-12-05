from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio

from WeatherService import WeatherService
from WeatherService import WeatherPoint

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

@app.get("/weather/current")
def read_current_weather(latitude: float, longitude: float):
    return WeatherService().get_current_weather(latitude=latitude, longitude=longitude)

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}
