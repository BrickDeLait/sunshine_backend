from dataclasses import dataclass
import json
from typing import List

@dataclass
class WeatherEntry:
    date: str
    temperature: float
    wind_speed: float
    temperature_min: float
    temperature_max: float
    precipitation_sum: float

@dataclass
class WeatherPoint:
    latitude: float
    longitude: float
    min_temp_climate_ref: float
    max_temp_climate_ref: float
    precipitation_climate_ref: float
    weather_entries: List[WeatherEntry]

    def to_json(self):
        data = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "weather_entries": self.weather_entries
        }
        return json.dumps(data)
