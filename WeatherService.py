
import networkService
import weatherPoint
from openMeteoEndpoint import OpenMeteoEndpoint

def get_current_weather(latitude: float, longitude: float) -> weatherPoint.WeatherPoint:
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "current": 'temperature_2m,wind_speed_10m'
    }
    try:
        data = networkService.request(OpenMeteoEndpoint.FORECAST, params)
        return weatherPoint.WeatherPoint(data["latitude"], data["longitude"], data["current"]["temperature_2m"], data["current"]["wind_speed_10m"])
    except Exception as error:
        print(f"An error occured: {error}")
        raise
