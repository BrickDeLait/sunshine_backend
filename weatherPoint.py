from dataclasses import dataclass
import json
from typing import List

@dataclass
class WeatherEntry:
    date: str
    temperature: float
    apparent_temperature: float
    temperature_min: float
    temperature_max: float
    precipitation: float
    precipitation_probability: int
    humidity: int
    cloud_cover: int
    direct_radiation: int
    wind_speed: float
    wind_direction: str
    sunrise: str
    sunset: str

@dataclass
class WeatherPoint:
    latitude: float
    longitude: float
    timezone_abbreviation: str
    current_weather: WeatherEntry
    hourly_forecast: List[WeatherEntry]
    daily_forecast: List[WeatherEntry]
