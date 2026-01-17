from enum import Enum
from Endpoint import Endpoint
from DataModels import weatherPoint

class OpenMeteoEndpoint(Enum, metaclass=Endpoint):
    FORECAST = 1
    HISTORICAL = 2

    @property
    def host(self): 
        if self.value == 1:
            return "api.open-meteo.com"
        if self.value == 2:
            return "archive-api.open-meteo.com"
        
    @property
    def path(self):
        if self.value == 1:
            return "/v1/forecast"
        if self.value == 2:
            return "/v1/archive"
        
    @property
    def url(self):
        return f"https://{self.host}{self.path}"
        
    @property
    def method(self):
        if self.value == 1:
            return 'GET'
        if self.value == 2:
            return 'GET'
        
class OpenMeteoForecastType(Enum):
    HOURLY = 1
    DAILY = 2

    @property
    def dict_key(self):
        if self.value == 1:
            return "hourly"
        if self.value == 2:
            return "daily"
        
    @property
    def query_params(self):
        if self.value == 1:
            return {
                "forecast_hours": 48,
                "hourly": 'temperature_2m,apparent_temperature,precipitation,precipitation_probability,relative_humidity_2m,cloud_cover,direct_radiation,wind_speed_10m,wind_direction_10m'
            }
        if self.value == 2:
            return {
                "forecast_days": 10,
                "daily": "temperature_2m_max,temperature_2m_min,cloud_cover_mean,temperature_2m_mean,apparent_temperature_mean,precipitation_sum,precipitation_probability_mean,relative_humidity_2m_mean,sunrise,sunset,shortwave_radiation_sum,wind_speed_10m_mean,winddirection_10m_dominant"
            }
    
    def get_weather_entry(self, date, index, data) -> weatherPoint.WeatherEntry:
        if self.value == 1:
            return weatherPoint.WeatherEntry(
                    date= date,
                    temperature= data[self.dict_key]["temperature_2m"][index],
                    apparent_temperature= data[self.dict_key]["apparent_temperature"][index],
                    temperature_min= None,
                    temperature_max= None,
                    precipitation= data[self.dict_key]["precipitation"][index],
                    precipitation_probability= data[self.dict_key]["precipitation_probability"][index],
                    humidity= data[self.dict_key]["relative_humidity_2m"][index],
                    cloud_cover= data[self.dict_key]["cloud_cover"][index],
                    direct_radiation= data[self.dict_key]["direct_radiation"][index],
                    wind_speed= data[self.dict_key]["wind_speed_10m"][index],
                    wind_direction= data[self.dict_key]["wind_direction_10m"][index],
                    sunrise= None,
                    sunset= None
                )
        if self.value == 2:
            return weatherPoint.WeatherEntry(
                    date= date,
                    temperature= data[self.dict_key]["temperature_2m_mean"][index],
                    apparent_temperature= data[self.dict_key]["apparent_temperature_mean"][index],
                    temperature_min= data[self.dict_key]["temperature_2m_min"][index],
                    temperature_max= data[self.dict_key]["temperature_2m_max"][index],
                    precipitation= data[self.dict_key]["precipitation_sum"][index],
                    precipitation_probability= data[self.dict_key]["precipitation_probability_mean"][index],
                    humidity= data[self.dict_key]["relative_humidity_2m_mean"][index],
                    cloud_cover= data[self.dict_key]["cloud_cover_mean"][index],
                    direct_radiation= data[self.dict_key]["shortwave_radiation_sum"][index],
                    wind_speed= data[self.dict_key]["wind_speed_10m_mean"][index],
                    wind_direction= data[self.dict_key]["winddirection_10m_dominant"][index],
                    sunrise= data[self.dict_key]["sunrise"][index],
                    sunset= data[self.dict_key]["sunset"][index]
                )


class WeatherServiceError(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"