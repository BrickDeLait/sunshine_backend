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