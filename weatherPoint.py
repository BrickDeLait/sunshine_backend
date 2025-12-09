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
    
@dataclass
class HistoricalWeatherPoint:
    latitude: float
    longitude: float
    temperature_min: float
    temperature_max: float
    precipitation_sum: float

    def to_json(self):
        data = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "temperature_min": self.temperature_min,
            "temperature_max": self.temperature_max,
            "precipitation_sum": self.precipitation_sum
        }
        return json.dumps(data)
