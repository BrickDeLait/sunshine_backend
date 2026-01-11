from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio

import weatherService

app = FastAPI()

@app.get("/")
async def read_root():
    print("Hello...")
    await asyncio.sleep(3)
    print("... world!")
    return {"Hello": "World"}

@app.get("/weather/current")
async def read_current_weather(latitude: float, longitude: float):
    return weatherService.get_weather(latitude=latitude, longitude=longitude)

@app.get("/weather/historical")
async def read_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    return weatherService.get_historical_weather(latitude=latitude, longitude=longitude, start_date=start_date, end_date=end_date)
