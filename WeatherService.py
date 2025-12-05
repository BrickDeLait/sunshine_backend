
from dataclasses import dataclass
import json

@dataclass
class WeatherPoint:
    latitude: float
    longitude: float
    temperature: float
    wind_speed: float

    def to_json(self):
        data = {"latitude": self.latitude, "longitude": self.longitude, "temperature": self.temperature, "wind_speed": self.wind_speed}
        return json.dumps(data)


from NetworkService import NetworkService
from OpenMeteoEndpoint import OpenMeteoEndpoint

class WeatherService:
    def __init__(self):
        pass

    def get_current_weather(self, latitude: float, longitude: float) -> WeatherPoint:
        params = {
            "latitude": latitude, 
            "longitude": longitude,
            "current": 'temperature_2m,wind_speed_10m'
        }
        data = NetworkService.request(OpenMeteoEndpoint.FORECAST, params)
        
        return WeatherPoint(data["latitude"], data["longitude"], data["current"]["temperature_2m"], data["current"]["wind_speed_10m"])

