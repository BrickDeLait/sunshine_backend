
from fastapi import FastAPI, HTTPException

import asyncio

from openMeteoEndpoint import OpenMeteoForecastType, WeatherServiceError
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
    try:
        return weatherService.get_current_weather(latitude=latitude, longitude=longitude)
    except WeatherServiceError as error: 
        raise HTTPException(error.error_code, error.message) from error

@app.get("/weather/forecast")
async def read_forecast(latitude: float, longitude: float, forecast_type: str):
    try:
        if forecast_type == OpenMeteoForecastType.HOURLY.dict_key:
            return weatherService.get_forecast(OpenMeteoForecastType.HOURLY, latitude, longitude)
        if forecast_type == OpenMeteoForecastType.DAILY.dict_key:
            return weatherService.get_forecast(OpenMeteoForecastType.DAILY, latitude, longitude)
        raise WeatherServiceError(406, "The forecast type is not supported. Only HOURLY and DAILY are supported.")
    except WeatherServiceError as error:
        raise HTTPException(error.error_code, error.message) from error

@app.get("/weather/climateNormals")
async def read_climate_normals(latitude: float, longitude: float):
    try:
        return weatherService.get_climate_normals(latitude, longitude)
    except WeatherServiceError as error:
        raise HTTPException(error.error_code, error.message) from error


@app.get("/weather/historical")
async def read_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    return weatherService.get_historical_weather(latitude=latitude, longitude=longitude, start_date=start_date, end_date=end_date)
